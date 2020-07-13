# Butter

## What is this?

The script gets listing data from an Excel spreadsheet following the template shown on http://www.landolphia.com/butter and creates a listing online on the specified platform.

## Requirements

- Python installed
- Chromedriver executable in the running directory
- the login info and Google API key must be specified in a a file called private.slr, in the running directory

Uses the following modules.

```shell
 pip install base64
 pip install googlemaps 
 pip install jinja2
 pip install pandas
 pip install phonenumbers
 pip install pyautogui
 pip install selenium
 pip install xlrd
```

## Usage

### POST
 POST: posts an ad based on listing.xlsx (check template).
1. Download the listing spreadsheet to the running directory
2. Download ChromeDriver and private.slr to the running directory
3. Add any images to post in a directory called "images" in the running directory, naming them sequentially from 1 to X(number of photos.)\
The files need to be either .jpg, .jpeg, .gif or .png.
4. Open your terminal
5. Navigate to the directory containing the script and spreadsheet
6. Run the script with:
```shell
py main.py POST [INFO, DEBUG]
```

Notes:
- INFO is the default logging level.
- DEBUG messages will be printed to debug.log by default anyway.

### SCRAPE 
 SCRAPE: scrapes online leads and creates a spreadsheet highlighting keywords defined in colors.json
1. Download ChromeDriver and private.slr to the running directory
2. Open your terminal
3. Navigate to the directory containing the script and spreadsheet
4. Run the script with:
```shell
py main.py SCRAPE [OFFLINE] [INFO, DEBUG]
```

Notes:
- INFO is the default logging level.
- DEBUG messages will be printed to debug.log by default anyway.
- OFFLINE will download the leads data to a local file and use it upon subsequent runs with the OFFLINE argument

## To-do

- Directory structure for configuration files
- Ponder data validation ( Better errors for xlsx scraping? )
- Ponder keywords improvement
- GUI

<details>
	<summary> Click to expand </summary>

Other:
- contact page
- value formatting and validation
- value type in payload
- remove lxml (see next item)
- consolidate with HTML scraper
</details>

## History

Current version: 0.9.1\
- using cx_freeze to compile to exe

<details>
  <summary> Older versions </summary>

v.9\
- new JSON format, actions are tied to elements
- SCRAPE/POST merged (POST isn't implemented)
v0.3\
- scrapes online leads
- creates spreadsheet, highlighting keywords
v0.2.5\
- remaining tasks list is more user friendly
v0.2.4\
- faster (instant) description filling for tinyMCE
v0.2.3
- loops through photos in ./images/ and uploads them
v0.2.2[HOTFIX]
- waits for user to press enter after running the script to close the browser window
- credentials obfuscated
- fixed typo in payload, leading to duplicate page/name entr
v0.2
- date and pets
- multiple floorplans
v0.1.8.5
- refactor, split navigator and element manipulation.
- assumes identifier type
- location, rent, floorplans, specifics, amenities
v0.1.8.5
- rotates log files
- console log level can be customized by passing an argument to the script (DEBUG, WARNING, INFO)
- documentation and website
- [HOTFIX] fixed duplicate logging and re-enabled implemented functionalities 
v0.1.8.3
Tweaks for first release
v0.1.8.2
Scrapes multiple floorplans from the spreadsheet
v0.1.8.1
Filling description/tinyMCE
v0.1.8
Refactoring done
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
</details>
