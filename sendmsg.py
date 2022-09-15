from multiprocessing import connection
import smtplib
import os

#Sender email
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")

#Receiver email
to_email = os.environ.get("TO_EMAIL")

class SendMail:

    def send(self, name, mail, message):
        
        msg = f"Name:{name}\nMail:{mail}\n\n{message}\n"

        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs="smksosn1@gmail.com", msg=message)
        connection.close()









# from multiprocessing import connection
# import smtplib

# my_email = "appmsg88@gmail.com"
# password = "gmformypy/-10"

# class SendMail:

#     def send(self, name, mail, message):
        
#         msg = f"Name:{name}\nMail:{mail}\n\n{message}\n"

#         connection = smtplib.SMTP("smtp.gmail.com", 587)
#         connection.starttls()
#         connection.login(user=my_email, password=password)
#         connection.sendmail(from_addr=my_email, to_addrs="smksosn1@gmail.com", msg=message)
#         connection.close()        