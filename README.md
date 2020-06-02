While thingy

1. Start logging.
2. Get credentials.
3. Get data from .xlsx file.
4. Navigate and post listing.
- FOR p in pages:
	FOR s in steps:
		do step

DEFINE LOGIN PAGE
-add step: wait for id login form
-add step: get+click element login link
-add step: wait for user id input
-add step: fill in username
-add step: fill in password
-add step: click to login

DEFINE ADD LISTING PAGE
-add step: go to add listing url
-add step: wait for full address input
-add step: fill in full address
-add step: press enter
-add step: wait for address input
-add step: fill in exact address
-add step: fill in city
-add step: fill in zip
-add step: fill in state
-add step: set display exact address flag
-add step: submit form




Main
- slurps credentials
- contains xpaths and ids, and link to pages

NOW:
Get info from spreadsheet
navigate site and populate with info
THEN:
- get args from command line
- use logging

Spreadsheet
- contains regexs
- uses geohelper and pandas
- contains object with the spreadsheet's data
THEN:
- separate Pandas', gMaps, and my own data
- consider bettering get-key
- should be able to scrape multiple listings from a single spreadsheet with arguments, or different files, or sheets

Navigation
- contains and uses Selenium's webdriver
THEN:
- create wrappers
- better data checking

DATA:
- name to link all of those
- listing data (address, flags, options)
- CSS locationdata
- spreadsheet offsets

MainV2
cell info -> spreadsheet -> data
- FOR EACH i IN seed:
	add cell info to data
data and css locators -> navigator -> post
- FOR EACH p IN pages:
	populate forms with data

#Butter
#v0.1.x

##What is this?

This script goes through the HTML of the listings page and generates a spreadsheet with the information needed.
Or, the script gets listing data from an Excel spreadsheet and creates a listing online.

##Usage

You need Python installed to run/compile this.
You also need Selenium's Chromedriver in the directory you're running Butter from, depending on what you're trying to do.
You also-also need the login info in a file called private.slr, username/password one two consecutive lines.
Guess what, more needs... Google API key, third entry in the private.slr file. This is used for Geocoding API access.
This will only work if you download and save the "Showing sheet" page as showing.html in the same directory as this.
Uses the following modules.

'''Shell
 pip install phonenumbers
 pip install lxml
 pip install xlswriter
 pip install pandas
 pip install selenium
 pip install googlemaps
 py main.py
'''

##To-do
- remove lxml
- customization through files and command line
- reorganize code base
- add documentation
- GUI and/or command line options
- spread payload in appropriate modules

##History
v0.1.6
Finished preliminary scraping and posting.
v0.1.5
Retrieving postal code
Navigation progress
v0.1.4
Excel slurping
v0.1.3
Basic navigation
Refactoring
v0.1.2
Login
v0.1.1
Basic static keyword detection and highlighting.
v0.1
Basic info scraping and spreadheet output.
