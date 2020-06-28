# Butter

## What is this?

The script gets listing data from an Excel spreadsheet following the template shown on http://www.landolphia.com/butter and creates a listing online on the specified ad posting platform.

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
- documentation and website
- finish multiple floorplan flow
- remove lxml
- GUI and/or command line options
- offer instructions on what's left to do when the script is done running
- be careful with value formatting validation
- photos
- contact
- move in date
- ad posting spreadsheet template
- refactor checkbox/dropdown/click/etc checkbox("page", "element") for readability

## History

Current version: 0.1.8.3
Tweaks for first release

<details>
  <summary>Click to expand!</summary>
  
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
