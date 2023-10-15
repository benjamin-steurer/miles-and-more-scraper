import requests
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
from dotenv import load_dotenv
import os
from config import FLIGHT_METHOD, DEPARTURE_DATE, SLACK_CHANNEL_OR_USER, ORIGIN_CURRENCY, DESTINATIONS, SEND_SLACK_MESSAGES


load_dotenv()
slack_client = WebClient(token=os.getenv('slack_api_token'))
headers = {
    'Content-Type': 'application/json', 
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'X-Api-Key': 'agGBZmuTGwFXWzVDg8ckGKGBytemE1nS', 
    'Referer': 'https://www.miles-and-more.com/',
    'Origin': 'https://www.miles-and-more.com'
}
session = requests.Session()
previous_responses = []
slack_client = WebClient(token=os.getenv('slack_api_token'))
previous_responses = []

def load_previous_responses():
    global previous_responses
    try:
        with open('previous_responses.json', 'r') as f:
            previous_responses.append(json.load(f))
    except FileNotFoundError:
        previous_responses.append([])

def save_previous_responses():
    with open('previous_responses.json', 'w') as f:
        json.dump(previous_responses[0], f)

def parse_data_and_post_slack(data, origin, dest):
    departure_date_str = data.get('departureDate')
    try:
        departure_date = datetime.strptime(departure_date_str, "%Y-%m-%d")
    except ValueError:
        print(f"Could not parse departure date: {departure_date_str}")
        return  

    if departure_date > datetime(2023, 11, 8):
        return 

    prices = data.get('prices', {})
    total_prices = prices.get('totalPrices', [])
    total_taxes = 0
    for price in total_prices:
        total_taxes = price.get('totalTaxes', 0) / 100  
    miles_conversion = prices.get('milesConversion', {})
    converted_miles = miles_conversion.get('convertedMiles', {})
    base_miles = converted_miles.get('base', 0)

    fareInfos = data.get('fareInfos', [])
    for fareInfo in fareInfos:
        flightIds = fareInfo.get('flightIds', [])

    new_entry = f'{origin} -> {dest}, {departure_date_str}, {base_miles}, {total_taxes:,.2f}, {flightIds}'
    print(new_entry)
    if new_entry not in previous_responses[0]:
         previous_responses[0].append(new_entry)
         if SEND_SLACK_MESSAGES:
             try:
                 response = slack_client.chat_postMessage(channel=SLACK_CHANNEL_OR_USER, text=f'New flight found: {new_entry}')
             except SlackApiError as e:
                 print(f"Error sending message: {e}")
         else:
            print(f'Duplicate entry found, not sending message: {new_entry}')

def process_response(response_json, origin, dest, status_code):
    if status_code == 400:
        return

    data = response_json.get('data', [])
    for entry in data:
        parse_data_and_post_slack(entry, origin, dest)

def post_flights_data(url, origins, destinations):
    for origin, currency in origins.items():
        for destination in destinations:
            json_body = {
                "commercialFareFamilies": [FLIGHT_METHOD],
                "corporateCodes": ["223293"],
                "currencyCode": currency,
                "frequentFlyer": {"companyCode": "LH", "priorityCode": 0},
                "itineraries": [
                    {
                        "departureDateTime": DEPARTURE_DATE,
                        "destinationLocationCode": destination,
                        "originLocationCode": origin
                    }
                ],
                "searchPreferences": {"mode": "bestByDay", "showMilesPrice": True},
                "travelers": [{"passengerTypeCode": "ADT"}]
            }

            post_response = session.post(url, headers=headers, json=json_body)        
            process_response(post_response.json(), origin, destination, post_response.status_code)

def fetch_flights_data():
    session.get("https://www.miles-and-more.com/de/de/spend/flights.html")
    api_url = "https://api.miles-and-more.com/flights/v1/bestbymonth"
    post_flights_data(api_url, ORIGIN_CURRENCY, DESTINATIONS)

if __name__ == "__main__":
    load_previous_responses()
    fetch_flights_data()
    save_previous_responses()