"""
Messages
========
Contains classes representing different message types.
"""
import email
import logging
import re
import bs4
import dateutil.parser

__author__ = 'cniedzwiedz'


class AmazonOrderConfirmationEmail(object):
    """ Class for an Amazon order confirmation email message.

    Example usage::
        >> email = AmazonOrderConfirmationEmail(email_str)
        >> email.order_total
        102.90
        >> email.order_details[0]
        {'name': 'crystal ball', 'price': 102.90}
    """
    def __init__(self, contents):
        super(AmazonOrderConfirmationEmail, self).__init__()
        self._raw_text = contents
        self._email = email.message_from_string(self._raw_text)
        self._order_details = []
        self._order_total = 0.

        self._parse_amazon_email()

    @staticmethod
    def get_price_string(string):
        return string.strip().replace("$", "")

    @property
    def subject(self):
        return self._email['subject'].strip().replace("\r\n", "")

    @property
    def recipient(self):
        return self._email['to']

    @property
    def date(self):
        return dateutil.parser.parse(self._email['date'])

    @property
    def order_total(self):
        return self._order_total

    @property
    def order_details(self):
        return self._order_details

    def _get_html_content(self):
        html_content = [part.get_payload(decode=True) for part in
                        self._email.walk() if part.get_content_type() ==
                        "text/html"]
        return "\n".join(html_content)

    def _parse_amazon_email(self):
        """ Get the HTML content and extract useful information """
        soup = bs4.BeautifulSoup(self._get_html_content())

        # First, get all the item names
        for name_field in soup.find_all(class_="name"):
            name = name_field.a.get_text().strip()
            price = self.get_price_string(name_field.find_next_sibling(class_="price").get_text())
            detail = {'name': name,
                      'price': float(price),
                      }
            self._order_details.append(detail)

        # Get the order total
        total_fields = soup.find_all(class_="total")
        if len(total_fields) > 0:
            self._order_total = float(self.get_price_string(total_fields[1].get_text()))

    def __str__(self):
        string = "Amazon Order Confirmation %s\n" % str(self.date.date())
        string += "%s\n" % self.subject
        for detail in self._order_details:
            string += "\t%s:\t$%.2f\n" % (detail['name'].encode('ascii',
                                                                'ignore'),
                                          detail['price'])
        string += "Order total:\t%.2f" % self.order_total

        return string


class AmazonShippingConfirmationEmail(AmazonOrderConfirmationEmail):
    """ Class for Amazon shipping confirmation messages

    Amazon shipping messages don't always have an itemized breakdown of what
    was shipped, but do seem to contain shipping totals.  They instead link
    to the order on Amazon.com.

    In the future, this can be looked up for more detail.
    """
    def _parse_amazon_email(self):
        """ Extract the shipping information

        Currently only grabs the order total.

        The order total can be found in a table with id "totals".  It's in
        the third cell of the first row.

        :return:
        """
        try:
            soup = bs4.BeautifulSoup(self._get_html_content())
            total_table = soup.find_all(id="totals")[0]

            try:
                total_cell = total_table.tr.find_all("td")[2]

                try:
                    values = re.split("\s+", total_cell.p.get_text())
                    self._order_total = float(self.get_price_string(values[3]))

                except IndexError:
                    logging.error("No total value found in message '%s'" % self.subject)

            except IndexError:
                logging.error("No total cell found in message '%s'" % self.subject)

        except IndexError:
            logging.error("No total table found in message '%s'" % self.subject)

    def __str__(self):
        string = "Amazon shipping Confirmation %s\n" % str(self.date.date())
        string += "%s\n" % self.subject
        for detail in self.order_details:
            string += "\t%s:\t$%.2f\n" % (detail['name'].encode('ascii',
                                                                'ignore'),
                                          detail['price'])
        string += "Order total:\t%.2f" % self.order_total

        return string

