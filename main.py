import base64
import os
import email
import imaplib
import getpass
import time
from datetime import datetime
import requests
import json
import base64
requests.packages.urllib3.disable_warnings() # suppress SSL certificate warnings when ssl_verify=False

print("See README for usage instructions")
print("\n")
## Preconfiguration steps
print("Mail Server Settings")
print('_' * 10)
mail_host = input("Mail Server: ")
mail_login = input("Username: ")
mail_pass = getpass.getpass()
mail_syncfrquency = int(input("Mail Sync Frequency (s): "))
mail_folder = input("Mail Server Folder Name: ")
mail_subjectCriteria = input("Subject Criteria: ")
print("\n")
print("API Settings")
print('_' * 10)
api_endpoint = input("API Host: ") + '/api/inventory/import.php'
api_sessionKey = input("API Session Key: ")
api_inventoryCategoryId = int(input("Inventory Category ID: "))


## Creation of cookie for auth
api_Cookie_json = []
api_Cookie_json.append({"SessionId":api_sessionKey})
api_Cookie = base64.b64encode(str(json.dumps(api_Cookie_json[0])).encode('ascii'))

print("\n")
print("Logs")
print('_' * 10)
## Mail fetch and download
while 1: ## repeat every x seconds
    now = datetime.now()
    mail = imaplib.IMAP4_SSL(mail_host)
    print(now.strftime("%d/%m/%Y %H:%M:%S") + ": " + str(mail.welcome.decode('utf-8')))
    mail.login(mail_login, mail_pass)
    mail.select(mail_folder)
    type, data = mail.search(None, '(UNSEEN SUBJECT "' + mail_subjectCriteria +'")')
    mail_ids = data[0]
    id_list = mail_ids.split()

    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)' )
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('utf-8') # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)
            
        for part in email_message.walk(): # downloading attachments
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            fileName = part.get_filename()
            if '.csv' in fileName:
                subject = str(email_message).split("Subject: ", 1)[1].split("\n", 1)[0]
                dateReceived = str(email_message).split("Date: ", 1)[1].split("\n", 1)[0]
                print(now.strftime("%d/%m/%Y %H:%M:%S") + ": " + 'Downloaded "{file}" from email titled "{subject}" received on the "{dateReceived}".'.format(file=fileName, subject=subject, dateReceived=dateReceived))
 
                request_cookie = {'UserSession': (api_Cookie.decode('utf-8'))}
                request_file = {'file': part.get_payload(decode=True)}
                request_value = {'category': api_inventoryCategoryId}

                response = requests.post(api_endpoint, cookies=request_cookie, files=request_file, data=request_value, verify=False)
                print (now.strftime("%d/%m/%Y %H:%M:%S") + ": Data Imported " + str(response.content.decode('utf-8')))


    mail.logout()
    time.sleep(mail_syncfrquency)