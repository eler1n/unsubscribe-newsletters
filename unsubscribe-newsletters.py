import imaplib
import email
import datetime
from email.header import decode_header
import webbrowser
import os
import re

# Your email credentials
EMAIL = 'lerinmax@gmail.com'
PASSWORD = 'sqfy jwrb htvx rugz'
SERVER = 'imap.gmail.com'  # For Gmail, it's 'imap.gmail.com'

# Connect to the email server
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Calculate the date 2 months ago from today
two_months_ago = datetime.datetime.now() - datetime.timedelta(days=60)
two_months_ago_str = two_months_ago.strftime('%d-%b-%Y')  # Format the date as 01-Jan-2000

# Search for emails from the last 2 months containing 'unsubscribe' in the body
criteria = '(SINCE "{}" BODY "unsubscribe")'.format(two_months_ago_str)
status, messages = mail.search(None, criteria)
if status != 'OK':
    print("No emails found!")
    exit()

# Initialize a set to store unique unsubscribe links
unique_links = set()

# Convert the result to a list of email IDs
messages = messages[0].split(b' ')

for mail_id in messages:
    status, data = mail.fetch(mail_id, '(RFC822)')
    if status != 'OK':
        print("Error reading message", mail_id)
        continue
    
    # Parse email content
    msg = email.message_from_bytes(data[0][1])
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    body = part.get_payload(decode=True).decode('utf-8')
                except UnicodeDecodeError:
                    body = part.get_payload(decode=True).decode('latin-1')  # Fallback to 'latin-1'
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
                for link in links:
                    if 'unsubscribe' in link.lower() and link not in unique_links and link.strip():
                        unique_links.add(link.strip())
                        print(link.strip())
                # Here you can decide to automatically open the links or just print them out for manual processing
                # for link in unsubscribe_links:
                #     webbrowser.open(link)
    else:
        # Process single-part messages...
        pass

# Don't forget to logout
mail.logout()
