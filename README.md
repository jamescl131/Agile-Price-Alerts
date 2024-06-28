This script should be scheduled on a crontab for around 5PM each day. Octopus make the current evening and next day's prices available shortly after 4PM each day. 

To use this script you need to choose/add the following. 

Price threshold - set this to your desired value, any prices below this will be emailed to you with the times and 30-min price blocks

API key - you get this from Octopus by clicking on your profile once logged in, paste the key into the script where shown

DNO / region code - the API URL is set for West Midlands, just look up your Octopus API URL based on your region letter and tarrif, these are publicly searchable

SMTP email settings - the script is setup to use gmail, although you could change this to any SMTP server. To use gmail you need to set a per app password (google this) to get your password for your gmail account. 
This is necessary if you have 2FA on your gmail account, if not you may be able to just put your gmail password in. 
Set the from and to address where you would like the emails to be sent from and to. 

Set up a crontab by typing crontab -e and pasting the following

00 17 * * * root <path>/agile-price-alerts.py

Please note: 
* The script won't send you an email if there's nothing below the set threshold.
* The script only lists 30-min blocks where prices are below your threshold

This means you could say you're only insterested in alerts at 5 pence or below and you'll only get alerts on days when the prices are at or below the threshold. 
