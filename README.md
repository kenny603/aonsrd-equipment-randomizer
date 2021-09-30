# aonsrd-equipment-randomizer
An experiment using Selenium to grab random samples of equipment from Archives of Nethys.

## What is this?
I've been wanting to teach myself Selenium but couldn't really think of a project to use it on. I've been running a Starfinder RPG for awhile and one thing I've needed was a way to quickly get a sampling of equipment to load into the shops. A much easier way of doing this would be to put all of the equipment into a JSON or XML file to pull from, but this gave me the perfect excuse to use Selenium to automate accessing the Archives of Nethys, which has a constantly updating set of tables with all the equipment from the various Starfinder books.

I would not recommend this script for general purpose. Again, this was just a way for me to teach myself Selenium and it might be a good learning tool for others as well.

## Installation
The script assumes that you already have the gecko webdriver, Python 3, and the Python libraries for Selenium installed. Copy the aonsrd_equipment_randomizer.py and equipment_definitions.json files to a directory of your choice.

## Usage
optional arguments:
<br/>
  **-h, --help**            show this help message and exit
<br/>
  **--armor**               Select from light armor, heavy armor, and armor
                        upgrades.
<br/>
  **--light-armor**         Select from light armor.
<br/>
  **--heavy-armor**         Select from heavy armor.
<br/>
  **--armor-upgrades**      Select from armor upgrades.
<br/>
  **--weapons**             Select from all weapon types, ammo, and accessories.
<br/>
  **--advanced-melee**      Select from advanced melee weapons.
<br/>
  **--ammunition**          Select from ammunition.
<br/>
  **--basic-melee**         Select from basic melee weapons.
<br/>
  **--grenade**             Select from grenades.
<br/>
  **--heavy-weapon**        Select from heavy weapons.
<br/>
  **--longarms**            Select from longarm weapons.
<br/>
  **--small-arms**          Select from small arm weapons.
<br/>
  **--sniper**              Select from sniper weapons.
<br/>
  **--solarian**            Select from solarian weapon crytals.
<br/>
  **--special**             Select from special weapons.
<br/>
  **--weapon-accessories**  Select from weapon accessories.
<br/>
  **--number-of-items NUMBER_OF_ITEMS, -n NUMBER_OF_ITEMS**
                        Number of items to select. Default is 10.
<br/>
  **--lowest-level LOWEST_LEVEL**
                        Lowest level of item to select from. Default is 1.
<br/>
  **--highest-level HIGHEST_LEVEL**
                        Highest level of item to select from. Default is 20.
<br/>
  **--seed SEED**           Seed for the random number generator.
<br/>
  **--debug, -d**           Enables debug messaging.
