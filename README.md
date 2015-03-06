# README

Currently just contains a script to reconcile the generic "Amazon" payee in 
your credit card ledger with a more descriptive name.

Ideally I will add more support for parsing Amazon emails,  including getting
the shipping notifications functional.


## azn_reconcile.py

I keep financial records in Quicken and like to have my transactions 
categorized by thing like "household", "pets", "computer/electronics", 
etc. so I can see where I spend my money.

For retailers like Amazon who sell things that span categories, 
only having an "Amazon" payee in the ledger for my credit card makes it 
harder to categorize what I bought.

This script will go through your amazon order confirmation messages and 
attempt to match them with ledger lines.


### Install

```sh
python setup.py install
```

### Description

```
usage: azn_reconcile.py [-h] [-f FOLDER] username QFX

Match transactions from an QFX file to your Amazon order confirmations

positional arguments:
  username              Email account username
  QFX                   QFX file to compare

optional arguments:
  -h, --help            show this help message and exit
  -f FOLDER, --folder FOLDER
                        Email folder to search. default: inbox
```

Works best for messages before 1/1/2015.  Amazon tweaks their confirmation 
messages and they may differ if you buy from an Amazon seller or Amazon 
themselves.

The script outputs a list of matched transactions.

```
2014-12-07 12:00:00:	AMAZON MKTPLACE PMTS:	29.44
	Your Amazon.com order of "Hubsan H107L X4 Mini RTF RC..." and 1 more item.
2014-11-30 12:00:00:	AMAZON MKTPLACE PMTS:	22.99
	Nike 371642 Legend Dri-Fit Tee - Orange
2014-11-28 12:00:00:	Amazon.com:	12.37
No match found
2014-11-28 12:00:00:	Amazon.com:	20.56
No match found
2014-11-28 12:00:00:	AMAZON MKTPLACE PMTS:	25.10
No match found
2014-11-27 12:00:00:	AMAZON MKTPLACE PMTS:	19.45
	Scotch-Brite Lint Roller, 5 Count, 95 Sheets
2014-11-28 12:00:00:	Amazon.com:	37.99
	Cellucor C4 Extreme Workout Supplement, Icy Blue Razz, 342 Gram
2014-11-18 12:00:00:	Amazon.com:	39.99
	Menu Winebreather Carafe
```

There is a bunch of work that can make this better:
  * Account for different Amazon email types: shipping and order confirmation
  * Account for variations in Amazon messages
  * Pay more attention to things like shipping costs and tax.
