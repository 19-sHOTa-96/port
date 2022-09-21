import smtplib
from twilio.rest import Client
from datetime import datetime as dt
import os


time_foramted = dt.today().strftime("%d/%m/%Y | %H:%S")


##Email Creds
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("M_PASSWORD")
to_email = os.environ.get("TO_EMAIL")

##Sms Creds
account_sid = "AC65123814c1e7a73756a3fdcb8af20a8d" #os.environ.get('TW_SID')
auth_token = "15388e639a810ba328419ec71e739e4b" #os.environ.get('TW_TOKEN')

class Contactor:

    def send_email(self, name, mail, message):
    
        message = f"Name:{name}\nMail:{mail}\n\n{message}\n"

        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="smksosn1@gmail.com", msg=message)
        connection.close()


    def send_sms(self, name, phonenumber, text):

        sms = f"SENDER-NAME: {name}\nPHONE: {phonenumber}\n{text}"

        client = Client(account_sid, auth_token)

        message = client.messages \
                        .create(
                            body=sms,
                            from_= "+18176460896", #os.environ.get('SENDER_PHONE'),
                            to= "+995571770421", #os.environ.get('RECEIVER_NUMBER')
                        )

        


if __name__ == "__main__":
    print(account_sid, auth_token, os.environ.get('SENDER_PHONE'))
    print(my_email, password, to_email)
    print(os.environ.get('RECEIVER_NUMBER'))


# print(account_sid, auth_token)