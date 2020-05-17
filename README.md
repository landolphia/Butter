#Butter
#v0.1.2

##What is this?

This script goes through the HTML of the listings page and generates a spreadsheet with the information needed.

##Usage

You need Python installed to run/compile this.
You also need Selenium's Chromedriver running from the directory you're running Butter from, depending on what you're trying to do.
You also-also need the login info in a file called private.slr, username/password one two consecutive lines.
This will only work if you download and save the "Showing sheet" page as showing.html in the same directory as this.

'''Shell
 pip install phonenumbers
 pip install lxml
 pip install xlswriter
 py HTMLScrape.py
'''

##To-do
- customization through files and command line
- reorganize code base
- add documentation
- GUI and/or command line options

##History
v0.1.2
Login
v0.1.1
Basic static keyword detection and highlighting.
v0.1
Basic info scraping and spreadheet output.
