# aonsrd-equipment-randomizer
An experiment using Selenium to grab random samples of equipment from Archives of Nethys.

## What is this?
I've been wanting to teach myself Selenium but couldn't really think of a project to use it on. I've been running a Starfinder RPG for awhile and one thing I've needed was a way to quickly get a sampling of equipment to load into the shops. A much easier way of doing this would be to put all of the equipment into a JSON or XML file to pull from, but this gave me the perfect excuse to use Selenium to automate accessing the Archives of Nethys, which has a constantly updating set of tables with all the equipment from the various Starfinder books.

I would not recommend this script for general purpose. Again, this was just a way for me to teach myself Selenium and it might be a good learning tool for others as well.

## Installation
The script assumes that you already have the gecko webdriver, Python 3, and the Python libraries for Selenium installed. Copy the aonsrd_equipment_randomizer.py and equipment_definitions.json files to a directory of your choice.

## Usage
usage: Get a random sampling of Starfinder items [-h] [--armor]
                                                 [--light-armor]
                                                 [--heavy-armor]
                                                 [--armor-upgrades]
                                                 [--weapons]
                                                 [--advanced-melee]
                                                 [--ammunition]
                                                 [--basic-melee] [--grenade]
                                                 [--heavy-weapon] [--longarms]
                                                 [--small-arms] [--sniper]
                                                 [--solarian] [--special]
                                                 [--weapon-accessories]
                                                 [--number-of-items NUMBER_OF_ITEMS]
                                                 [--lowest-level LOWEST_LEVEL]
                                                 [--highest-level HIGHEST_LEVEL]
                                                 [--seed SEED] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --armor               Select from light armor, heavy armor, and armor
                        upgrades.
  --light-armor         Select from light armor.
  --heavy-armor         Select from heavy armor.
  --armor-upgrades      Select from armor upgrades.
  --weapons             Select from all weapon types, ammo, and accessories.
  --advanced-melee      Select from advanced melee weapons.
  --ammunition          Select from ammunition.
  --basic-melee         Select from basic melee weapons.
  --grenade             Select from grenades.
  --heavy-weapon        Select from heavy weapons.
  --longarms            Select from longarm weapons.
  --small-arms          Select from small arm weapons.
  --sniper              Select from sniper weapons.
  --solarian            Select from solarian weapon crytals.
  --special             Select from special weapons.
  --weapon-accessories  Select from weapon accessories.
  --number-of-items NUMBER_OF_ITEMS, -n NUMBER_OF_ITEMS
                        Number of items to select.
  --lowest-level LOWEST_LEVEL
                        Lowest level of item to select from. Default is 1.
  --highest-level HIGHEST_LEVEL
                        Highest level of item to select from. Default is 20.
  --seed SEED           Seed for the random number generator.
  --debug, -d           Enables debug messaging.
