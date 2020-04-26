EMAIL_ADDRESS = "SteamItemDataBot@gmail.com"
EMAIL_PASSWORD = "vdjqlulzpbggkskz"
#hide these
def get_Percent_change(old, new):
    return((float(new)-old)/abs(old))*100

contacts = ["bailey.padovan@hotmail.com"]

def sif(e):
    return[e[1]]

pricelist.sort(reverse=False,key=sif)
import smtplib


from email.message import EmailMessage

msg = EmailMessage()
msg['SUBJECT'] = 'Basic Text Item Analysis'
msg['FROM'] = EMAIL_ADDRESS
msg['TO'] = contacts
msg.set_content(f"")
################################################################################
# msg.add_alternative("""
# <html lang="en" dir="ltr">
#   <head>
#     <meta charset="utf-8">
#     <title></title>
#   </head>
#   <body style="background-color: #01152e">
#     <h1>Very Cool Test</h1>
#   </body>
# </html>
# """, subtype='html')
#############################################################################
# files = ['sw.png', 'p2.png']
#
# for file in files:
#     with open(file, 'rb') as f:
#         file_data = f.read()
#         file_type = imghdr.what(f.name)
#         file_name = f.name
#
#     msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
################################################################################

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    smtp.send_message(msg)
