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
 pip install pandas
 pip install phonenumbers
 pip install selenium
 pip install xlrd
```

## Usage

1. Download the listing spreadsheet to the running directory
2. Open your terminal
3. Navigate to the directory containing the script and spreadsheet
4. Run the script with "py main.py"

```shell
py main.py
```

## To-do

<details>
	<summary> Click to expand </summary>

- double check pets
Other:
- photos page
- contact page
- value formatting and validation
- value type in payload
- consider webDriver wait delay, might improve speed
- remove lxml (see next item)
- consolidate with HTML scraper
</details>

## History

Current version: 0.2.2[HOTFIX]\
- credentials obfuscated
- fixed type in payload, leading to duplicate page/name entry

<details>
  <summary> Older versions </summary>

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
