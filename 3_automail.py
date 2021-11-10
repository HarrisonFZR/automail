# -*- coding: utf-8 -*
import schedule
import time
import smtplib
from email.message import EmailMessage
import datetime

def getYesterday():
      today = datetime.date.today()
      oneday = datetime.timedelta(days = 1)
      yesterday = today - oneday
      return yesterday

def job():
    #from email.message import EmailMessage
    EMAIL_ADDRESS = "data.nmb@singtaonewscorp.com" # your email address
    EMAIL_PASSWORD = "Ht8SVEtx" 

    contacts = ['wingws.chan@singtaonewscorp.com', 'kenrik.chan@singtaonewscorp.com']
    #contacts = ['harrison.fu@singtaonewscorp.com']

    msg = EmailMessage()
    if getYesterday().day<10:
        msg['Subject'] = 'Headline Daily - Top 500 article report (0%s/%s/%s)'%(getYesterday().day, getYesterday().month, getYesterday().year)
    else:
        msg['Subject'] = 'Headline Daily - Top 500 article report (%s/%s/%s)'%(getYesterday().day, getYesterday().month, getYesterday().year) 
    #msg['Subject'] = 'Today data report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = contacts
    msg.set_content('Please check the \'Headline Daily - Top 500 article report\' for today. Thank you very much.')
    if getYesterday().day<10:
        files = ['HD_Data_Report_%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day)]
        #files = ['UTF-8\'\'HD_iOS_Daily_Auto_Final_r1%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'UTF-8\'\'HD_And_Auto_Final_r1%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'HD_Web_Daily_Auto_Final%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'sum_%s%s0%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day)]
    else:
        files = ['HD_Data_Report_%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day)]
        #files = ['UTF-8\'\'HD_iOS_Daily_Auto_Final_r1%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'UTF-8\'\'HD_And_Auto_Final_r1%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'HD_Web_Daily_Auto_Final%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day), 'sum_%s%s%s.csv'%(getYesterday().year, getYesterday().month, getYesterday().day)]

    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        msg.add_attachment(file_data, maintype = 'application', subtype = 'octet-stream', filename = file_name)
    with smtplib.SMTP_SSL('mail.singtaonewscorp.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
    print('I am working...')
#schedule.every(1).minutes.do(job)
# schedule.every().hour.do(job)
#schedule.every().day.at("14:20").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at(“13:15").do(job)
# schedule.every().minute.at(“:17”).do(job)
if __name__=='__main__':
    job()
#while True:
#    schedule.run_pending()
#    time.sleep(1)








