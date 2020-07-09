# Butter
## Roadmap to V1

### In progress

Payload should be able to load incomplete units of data.
Should also contain type of value and actions, and flow?


### Notes

PAYLOAD:
This module slurps and formats site navigation data.
- Split Payload and Flow(navigation instruction) ]OR[ add Flow actions to Payload config file
- Add data validation and processing actions in Payload (date/etc)
- Should contain data type for validation and formatting

Navigator/Scraper:
This modules navigates through the site according to the Flow and gets/sets values according to the Payload. Uses elements for DOM manipulation.
- for e in elements: for a in e.actions: do a

Elements:
DOM Manipulation [IN/OUT]


Spreadsheet/Scrapings: [IN/OUT]
Maybe those should remain seperated. They are both relatively short and there isn't much overlap.

Keywords/Geohelper/Credentials:
Those modules are independent.

## To-do

- put as much as possible in config files (websites, credentials, elements, field properties (type/etc)
- for now the work is based on getting listings online and processing them
- get data from json for elements, payload, and navigator (flow of input)
- merge SCRAPE/POST code
- restructured file and folder hierarchy for better configuration/automation

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

Current version: 0.3\
- scrapes online leads
- creates spreadsheet, highlighting keywords

<details>
  <summary> Older versions </summary>

v0.2.5\
- remaining taks list is more user friendly
v0.2.4\
- faster (instant) description filling for tinyMCE
v0.2.3
- loops through photos in ./images/ and uploads them
v0.2.2[HOTFIX]
- waits for user to press enter after running the script to close the browser window
- credentials obfuscated
- fixed type in payload, leading to duplicate page/name entr
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
