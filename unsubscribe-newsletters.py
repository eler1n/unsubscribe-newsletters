import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re

# Your email credentials
EMAIL = 'your_email@example.com'
PASSWORD = 'yourpassword'
SERVER = 'imap.example.com'  # For Gmail, it's 'imap.gmail.com'

# Connect to the email server
mail = imaplib.IMAP4_SSL(SERVER)
mail.login(EMAIL, PASSWORD)
mail.select('inbox')

# Search for emails containing 'unsubscribe' in the body
status, messages = mail.search(None, '(BODY "unsubscribe")')
if status != 'OK':
    print("No emails found!")
    exit()

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
                body = part.get_payload(decode=True).decode()
                links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', body)
                unsubscribe_links = [link for link in links if 'unsubscribe' in link.lower()]
                print("Unsubscribe links found:", unsubscribe_links)
                # Here you can decide to automatically open the links or just print them out for manual processing
                # for link in unsubscribe_links:
                #     webbrowser.open(link)
    else:
        # Process single-part messages...
        pass

# Don't forget to logout
mail.logout()
