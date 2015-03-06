from dateutil.tz import tzutc

__author__ = 'cniedzwiedz'

import unittest
import datetime
from email_predict.Messages import AmazonOrderConfirmationEmail, \
    AmazonShippingConfirmationEmail


class MessagesTestCase(unittest.TestCase):

    def test_AmazonConfirmationEmail(self):
        """ Unit test for the email message class """
        with open("data/test.email", "r") as f:
            test_email_contents = f.read()
        azn = AmazonOrderConfirmationEmail(test_email_contents)
        self.assertEqual(azn.order_total, 30.71)
        self.assertEqual(azn.subject, "Amazon.com order of Melannco Espresso Square... and 1 more item(s).")
        self.assertEqual(azn.recipient, "Test User <test@gmail.com>")

        self.assertEqual(len(azn._order_details), 2)
        self.assertEqual(azn._order_details[0]['name'],
                         'Melannco Espresso Square Shelves, Set of 3')
        self.assertEqual(azn._order_details[0]['price'], 19.22)
        self.assertEqual(azn._order_details[1]['name'],
                         'Modern Art Candle Holder Wall Sconce Plaque Set Of Two')
        self.assertEqual(azn._order_details[1]['price'], 9.90)
        self.assertEqual(azn.date, datetime.datetime(2013, 11, 6, 22, 27, 42,
                                                     tzinfo=tzutc()))

        with open("data/test2.email", "r") as f:
            test_email_contents = f.read()
        azn = AmazonOrderConfirmationEmail(test_email_contents)
        self.assertEqual(azn.order_total, 29.44)
        self.assertEqual(azn.subject, "Your Amazon.com order of \"Hubsan H107L X4 Mini RTF RC...\" and 1 more item.")
        self.assertEqual(azn.recipient, "Test User <test@gmail.com>")

        self.assertEqual(len(azn._order_details), 2)
        self.assertEqual(azn._order_details[0]['name'],
                         'Hubsan H107L X4 Mini RTF RC Quadcopter')
        self.assertEqual(azn._order_details[0]['price'], 44.99)
        self.assertEqual(azn._order_details[1]['name'],
                         'Yizzam- OMG Welsh Corgi -Tagless- Mens Shirt-X-Large')
        self.assertEqual(azn._order_details[1]['price'], 29.99)
        self.assertEqual(azn.date, datetime.datetime(2014, 12, 5, 20, 20, 35,
                                                     tzinfo=tzutc()))

    def test_AmazonShippingEmail(self):
        """ Unit test for the email message class """
        with open("data/shipping.email", "r") as f:
            test_email_contents = f.read()
        azn = AmazonShippingConfirmationEmail(test_email_contents)
        self.assertEqual(azn.order_total, 14.72)
        self.assertEqual("Your Amazon.com order of \"Zero: The Biography of "
                         "a...\" has shipped!", azn.subject)
        self.assertEqual("Test User <test@gmail.com>", azn.recipient)

if __name__ == '__main__':
    unittest.main()
