#!/usr/bin/env python
"""
Amazon Transaction Reconciliation
=================================
Given access to your email account and a QFX/OFX file, figure out how to
categorize your Amazon transactions.

Example: azn_reconcile.py -f "[Gmail]/All Mail" cniedzwiedz tests/data/test.qfx
"""
import logging
import re
from ofxparse import OfxParser
from email_predict.EmailServices import GMailService
import argparse
import getpass
from imaplib import IMAP4

__author__ = 'cniedzwiedz'

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)

parser = argparse.ArgumentParser(description="Match transactions from an QFX "
                                             "file to your Amazon order "
                                             "confirmations")
parser.add_argument("username", help="Email account username")
parser.add_argument("QFX", help="QFX file to compare")
parser.add_argument("-f", "--folder", help="Email folder to search. default: "
                                           "inbox",
                    default="inbox")
args = parser.parse_args()

#
# First, get the user credentials
#
email_username = args.username
email_password = getpass.getpass("Email Password: ")

#
# Connect to GMail
#
logging.debug("Getting emails...")
gmail = GMailService()

try:
    gmail.login(username=email_username, password=email_password)
except IMAP4.error:
    print "Invalid credentials.  Please try again."
    exit(1)

azn_confs = gmail.get_amazon_confirmations(args.folder)

if len(azn_confs) == 0:
    print "No Amazon transactions found in email"
    exit(1)

#
# Import the transactions
#
logging.debug("Getting transactions...")
azn_re = re.compile("amazon")
ofx = OfxParser.parse(file(args.QFX))
azn_txns = [t for t in ofx.account.statement.transactions
            if azn_re.match(t.payee.lower())]

if len(azn_txns) == 0:
    print "No Amazon transactions found in QFX file"
    exit(1)

#
# For each amazon transaction, find a matching item from emails.  This can be
# either the detail or order total
#
logging.debug("Finding matches...")
for txn in azn_txns:
    amount = abs(float(txn.amount))
    print "%s:\t%s:\t%.2f" % (txn.date, txn.payee, amount)
    for conf in azn_confs:
        msg = None
        for detail in conf.order_details:
            if amount == detail['price']:
                msg = "\t%s" % detail['name']
                break

        if not msg is None:
            break

        if amount == conf.order_total:
            msg = "\t%s" % conf.subject
            break

    if msg is None:
        print "No match found"
    else:
        print msg
