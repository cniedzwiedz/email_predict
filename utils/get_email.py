__author__ = 'cniedzwiedz'

import imaplib
import getpass
from email_predict.Messages import AmazonOrderConfirmationEmail

gmail_address = raw_input("GMail User Name: ")
password = getpass.getpass("Password: ")


mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('%s@gmail.com' % gmail_address, password)

# Out: list of "folders" aka labels in gmail.
mail.select("[Gmail]/All Mail")

#result, data = mail.search(None, '(HEADER FROM "auto-confirm@amazon.com")')
result, data = mail.search(None, '(HEADER FROM "ship-confirm@amazon.com")')

ids = data[0]
id_list = ids.split()

latest_email_id = id_list[-1]
_, data = mail.fetch(latest_email_id, "(RFC822)")
raw_email = data[0][1]
print raw_email

for i in xrange(-100, 0, 1):
    latest_email_id = id_list[i]
    _, data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = data[0][1]
    print str(AmazonOrderConfirmationEmail(raw_email))

