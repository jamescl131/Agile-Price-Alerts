#!/usr/bin/env python3

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone
import pytz

# Octopus API URL and key
# Add your API key and change the letter for the DNO region you are in, you can look this up only. The letter is after the date in the URL below, in this case "E" for West Midlands
api_url = "https://api.octopus.energy/v1/products/AGILE-18-02-21/electricity-tariffs/E-1R-AGILE-18-02-21-E/standard-unit-rates/"
api_key = "API Key"

# Threshold price in pence (customizable)
threshold_price = 15

# Function to fetch Agile prices
def fetch_agile_prices():
    response = requests.get(api_url, auth=(api_key, ""))
    data = response.json()
    return data['results']

# Function to convert UTC time to BST if applicable
def convert_to_bst(time_utc):
    # Define the UTC and BST time zones
    utc = pytz.utc
    bst = pytz.timezone('Europe/London')

    # Ensure time is in UTC
    if time_utc.tzinfo is None:
        time_utc = time_utc.replace(tzinfo=timezone.utc)

    # Convert UTC time to BST
    bst_time = time_utc.astimezone(bst)
    return bst_time

# Function to format email content with prices below threshold
def format_email_content(prices):
    now = datetime.now(timezone.utc)
    future_prices = [price for price in prices if datetime.strptime(price['valid_from'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc) > now]
    future_prices.sort(key=lambda x: x['valid_from'])

    message_body = """

    <html>
    <head>
        <style>
            body {
                background-color: #000;
                font-family: Arial, sans-serif;
                color: #ddd;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 80%;
                margin: auto;
                background-color: #222;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            }
            h2 {
                color: #00bfff;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 10px;
                text-align: left;
                border-bottom: 1px solid #444;
            }
            th {
                background-color: #00bfff;
                color: #000;
            }
            td {
                font-weight: bold;
                color: #ddd;
            }
            .price {
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Octopus Agile Price List</h2>
            <table>
                <tr>
                    <th>Time (BST)</th>
                    <th>Price (p)</th>
                </tr>
    """

    prices_below_threshold = False

    for price in future_prices:
        value_inc_vat = price['value_inc_vat']
        if value_inc_vat < threshold_price:
            prices_below_threshold = True
            time_utc = datetime.strptime(price['valid_from'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
            bst_time = convert_to_bst(time_utc)
            time_str = bst_time.strftime('%Y-%m-%d %H:%M:%S %Z')

            # Determine color based on price bands and ensure readability
            if value_inc_vat < 0:
                color = "#add8e6"  # light blue for prices below 0p
            elif value_inc_vat < 5:
                color = "#00ff00"  # green for prices below 5p
            elif value_inc_vat < 10:
                color = "#1e90ff"  # dodger blue for prices below 10p
            elif value_inc_vat < 15:
                color = "#ffd700"  # gold for prices below 15p
            elif value_inc_vat < 20:
                color = "#ffa500"  # orange for prices below 20p
            else:
                color = "#ff4500"  # orange-red for prices 20p and above


            message_body += f"<tr><td style='color: #ddd;'>{time_str}</td><td class='price' style='color:{color};'>{value_inc_vat}p</td></tr>"


    message_body += """
            </table>
        </div>
    </body>
    </html>
    """

    return message_body, prices_below_threshold

# Function to send HTML email notification

def send_email_notification(prices):
    msg = MIMEMultipart()
    msg['Subject'] = "Octopus Agile Price Alert"
    msg['From'] = "insert email 
    msg['To'] = "insert email"

    # Format the email content as HTML
    message_body, prices_below_threshold = format_email_content(prices)

  
    # Only send email if there are prices below the threshold
    if prices_below_threshold:
        # Attach the HTML message to the email
        msg.attach(MIMEText(message_body, 'html'))
      
        # Connect to the Gmail SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login("insert email", "insert app password")
            server.sendmail(msg['From'], msg['To'], msg.as_string())

# Main function to execute the script

def main():
    prices = fetch_agile_prices()
    send_email_notification(prices)

if __name__ == "__main__":
    main()
