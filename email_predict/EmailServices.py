from email_predict.Messages import AmazonOrderConfirmationEmail, \
    AmazonShippingConfirmationEmail

__author__ = 'cniedzwiedz'

import imaplib


class EmailService(object):
    """ Base class for email services """
    imap_url = ""

    def __init__(self):
        self._mail = None

    def login(self, username, password):
        """ Authenticate to the email service """
        self._mail = imaplib.IMAP4_SSL(self.imap_url)
        self._mail.login(username, password)

    def get_amazon_confirmations(self, folder="inbox", count=1000):
        """ Retrieve messages from a folder

        :param folder:      Folder to get messages from.  Default: 'inbox'
        :type folder:       str
        :param count:       Max number of messages to return
        :type count:        int
        :return:            List of messages
        :rtype:             list
        """
        self._mail.select(folder)

        _, data = self._mail.search(None, '(HEADER FROM '
                                          '"auto-confirm@amazon.com")')

        ids = data[0]
        id_list = ids.split()

        limit = min(count, len(id_list))

        emails = []
        for i in xrange(limit):
            latest_email_id = id_list[i]
            _, data = self._mail.fetch(latest_email_id, "(RFC822)")
            raw_email = data[0][1]

            emails.append(AmazonOrderConfirmationEmail(raw_email))

        return emails


class GMailService(EmailService):
    """ GMail Email Service """
    imap_url = 'imap.gmail.com'

