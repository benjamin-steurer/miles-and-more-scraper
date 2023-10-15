from datetime import datetime 
FLIGHT_METHOD = "CFFBUSINST" # CFFBUSINST for Business Class, CFFECOINST for Economy Class
DEPARTURE_DATE = "2023-10-21T00:00:00" # YYYY-MM-DDTHH:MM:SS

SLACK_CHANNEL_OR_USER = "U049RB147QE" # Your Slack User ID or your Channel Name

SEND_SLACK_MESSAGES = False  # or False if you don't want to send Slack messages

LATEST_DEPARTURE_DATE = datetime(2023, 11, 5)

ORIGIN_CURRENCY = { # value pair or Origin Aiport with the Currency of the individual country
    "STR": "EUR", 
    "FRA": "EUR", 
    "MUC": "EUR",
    "DUS": "EUR", 
    "VIE": "EUR", 
    "LON": "GBP", 
    "AMS": "EUR", 
    "ZRH": "CHF", 
    "STO": "SEK", 
    "PAR": "EUR", 
    "MIL": "EUR", 
    "ROM": "EUR", 
    "BER": "EUR", 
    "DTM": "EUR", 
    "HAM": "EUR", 
    "FKB": "EUR", 
    "BCN": "EUR", 
    "MAD": "EUR", 
    "LIS": "EUR", 
    "GVA": "CHF", 
    "CDG": "EUR"}

DESTINATIONS = [
    "PVG", 
    "BKK", 
    "HKT", 
    "SIN", 
    "KUL", 
    "HKG", 
    "TPE", 
    "DMK", 
    "CAN", 
    "CTU", 
    "SGN"]