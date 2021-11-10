# -*- coding: utf-8 -*
import os
from imbox import Imbox # pip install imbox
import traceback
import datetime

# enable less secure apps on your google account
# https://myaccount.google.com/lesssecureapps

host = "mail.singtaonewscorp.com"
username = "data.nmb@singtaonewscorp.com" # your email address
password = "Ht8SVEtx" # your password
download_folder = "/Users/fuziru/Files/singtao/25_10_2021/Automail/Headline" # downloading path

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
    
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
#messages = mail.messages() # defaults to inbox
messages = mail.messages(sent_from='no-reply@omniture.com', date__on = datetime.date.today())
#messages = mail.messages(sent_from=stdt.test852@gmail.com'kenrik.chan@singtaonewscorp.com', no-reply@omniture.comdate__on=datetime.date(2021, 10, 28), datetime.date.today())

for (uid, message) in messages:
    mail.mark_seen(uid) # optional, mark message as read

    for idx, attachment in enumerate(message.attachments):
        try:
            att_fn = attachment.get('filename')
            download_path = f'{download_folder}/{att_fn}' # {download_folder}/
            print(download_path)
            with open(download_path, "wb") as fp:
                fp.write(attachment.get('content').read())
        except:
            print(traceback.print_exc())

mail.logout()


"""
Available Message filters: 

# Gets all messages from the inbox
messages = mail.messages()

# Unread messages
messages = mail.messages(unread=True)

# Flagged messages
messages = mail.messages(flagged=True)

# Un-flagged messages
messages = mail.messages(unflagged=True)

# Messages sent FROM
messages = mail.messages(sent_from='sender@example.org')

# Messages sent TO
messages = mail.messages(sent_to='receiver@example.org')

# Messages received before specific date
messages = mail.messages(date__lt=datetime.date(2018, 7, 31))

# Messages received after specific date
messages = mail.messages(date__gt=datetime.date(2018, 7, 30))

# Messages received on a specific date
messages = mail.messages(date__on=datetime.date(2018, 7, 30))

# Messages whose subjects contain a string
messages = mail.messages(subject='Christmas')

# Messages from a specific folder
messages = mail.messages(folder='Social')
"""