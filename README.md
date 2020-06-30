# Butter

## What is this?

The script gets listing data from an Excel spreadsheet following the template shown on http://www.landolphia.com/butter and creates a listing online on the specified platform.

## Requirements

- Python installed
- Chromedriver executable in the running directory
- the login info and Google API key must be specified in a a file called private.slr, in the running directory
```
First line: username
Second line: password
Third line: Google API key
```
Uses the following modules.

```shell
 pip install googlemaps
 pip install pandas
 pip install phonenumbers
 pip install selenium
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

- finish multiple floorplan flow
- photos page
- contact page
- move in date
- double check pets
- value formatting and validation
- refactor checkbox/dropdown/click/etc checkbox("page", "element") for readability
- consider webDriver wait delay, might improve speed
- remove lxml (see next item)
- consolidate with HTML scraper
</details>

## History

Current version: 0.1.8.4
Better logging:
- rotates log files
- console log level can be customized by passing an argument to the script (DEBUG, WARNING, INFO)
- documentation and website

<details>
  <summary> Older versions </summary>
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
