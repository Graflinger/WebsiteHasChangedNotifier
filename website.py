import time
import hashlib
from urllib.request import urlopen, Request
import pandas as pd
import smtplib
import ssl
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# setting the URL you want to monitor

website = "website to monitor"

url = Request(website, headers={'User-Agent': 'Mozilla/5.0'})

# to perform a GET request and load the
# content of the website and store it in a var
response = urlopen(url).read()

df = pd.read_csv("hash.csv")

# to read the initial hash
currentHash = df.iloc[0].values[0]

print("running")

while True:
    try:
        # perform the get request and store it in a var
        response = urlopen(url).read()

        # create a hash
        currentHash = df.iloc[0].values[0]

        # wait for 60 seconds
        time.sleep(60)

        # perform the get request
        response = urlopen(url).read()

        # create a new hash
        newHash = hashlib.sha224(response).hexdigest()

        # check if new hash is same as the previous hash
        if newHash == currentHash:
            print("nothing changed")
            continue

        # if something changed in the hashes
        else:
            # create mail
            senderEmail = "sendermail"
            senderEmailPassword = "yourPassword"
            toEmail = ""
            msg = MIMEMultipart()
            msg['From'] = senderEmail
            msg['To'] = toEmail
            msg['Subject'] = "subject"

            emailText = "mailtext"
            msg.attach(MIMEText(emailText, 'html'))

            context = ssl.create_default_context()
            with smtplib.SMTP("mail.gmx.net", 587) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(senderEmail, senderEmailPassword)
                text = msg.as_string()
                server.sendmail(senderEmail, toEmail, text)

            df.iloc[0] = newHash

            # save new hash to file
            df.to_csv("hash.csv", index=False)

            # sleep 30 seconds
            time.sleep(30)
            continue

    # To handle exceptions
    except Exception as e:
        print("error")
