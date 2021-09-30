#!/usr/bin/python
# Copyright (C) 2021  Ken Benoit
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

"""
This script uses Selenium to scrape the Archives of Nethys
(https://www.aonsrd.com) for item information such that a random set of items
can be selected and presented to the user. Numerous arguments are provided to
narrow down the potential pool of items to select.

This script is overkill for its intended purpose, but is just meant to be
a practice exercise using Selenium for the first time.

"""

__author__ = 'Ken Benoit'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import argparse
import random
import time
import numpy
import json

class EquipmentRandomizer():
    def __init__(self):
        self._arg_parser = self.setup_argparse()
        self._settings = None
        self._possible_items = []

    def get_definitions(self):
        definitions = None
        with open("equipment_definitions.json", 'r') as def_file:
            definitions = json.load(def_file)
        return definitions
    # end get_definitions

    def load_page(self, link_text, url, categories = {}):
        # First try clicking the link text
        try:
            if self._settings['debug']:
                print("Clicking link {}".format(link_text))
            element = self._driver.find_element_by_link_text(link_text)
            element.click()
        except:
            if self._settings['debug']:
                print(
                    "Unable to find link {0} on page {1}".format(
                        link_text, self._driver.current_url
                    )
                )
            self._driver.quit()

        # At this point the link should have redirected us to the intended page.
        # Do an explicit wait to ensure the expected URL is correct.
        try:
            if self._settings['debug']:
                print("Checking to make sure the url changed to {}".format(url))
            WebDriverWait(self._driver, 10).until(
                expected_conditions.url_to_be(url)
            )
        except:
            if self._settings['debug']:
                print(
                    "Clicking the link {0} never caused the url to change to {1}".format(
                        link_text, url
                    )
                )
            self._driver.quit()

        # Lastly, if there are any categories associated with the page, do an
        # explicit wait on each of the category links to make sure they are all
        # present on the page.
        for value in categories.values():
            try:
                if self._settings['debug']:
                    print("Checking for link {}".format(value["link_text"]))
                WebDriverWait(self._driver, 5).until(
                    expected_conditions.presence_of_element_located((By.LINK_TEXT, value["link_text"]))
                )
                if self._settings['debug']:
                    print("Link {} found".format(value["link_text"]))
            except:
                if self._settings['debug']:
                    print(
                        "Unable to find expected category link {0} on page {1}".format(
                            value["link_text"], self._driver.current_url
                        )
                    )
                self._driver.quit()

        # If there are no categories associated with this page then we expect
        # to be on the lowest level page where equipment should be present to
        # select from
        if categories == {}:
            self.get_equipment_list()
    # end load_page

    def load_categories(self, categories):
        # Iterate through the supplied categories
        for key, value in categories.items():
            # If the category being iterated over itself has a list of
            # categories then use this path, since we will recursive follow
            # the lower categories until we no longer find any more, which
            # would indicate that we have hit an equipment table.
            if "categories" in value:
                # Check if this category matches one supplied on the command
                # line. If the category doesn't match then skip it as we don't
                # want to have a page load where the data is not needed.
                if self._settings["categories"][key]:
                    self.load_page(
                        link_text = value["link_text"],
                        url = value["url"],
                        categories = value["categories"],
                    )
                    self.load_categories(
                        categories = value["categories"],
                    )
            else:
                # Check if this category matches one supplied on the command
                # line. If the category doesn't match then skip it as we don't
                # want to have a page load where the data is not needed.
                if self._settings["categories"][key]:
                    self.load_page(
                        link_text = value["link_text"],
                        url = value["url"],
                    )
    # end load_categories

    def get_equipment_list(self):
        tables = self._driver.find_elements_by_tag_name("table")

        for table in tables:
            name_column_index = None
            level_column_index = None
            # Find the column names of the table
            column_names = table.find_elements_by_tag_name("th")
            # We only need to know the Name and Level column indices, so iterate
            # until we find both
            for index in range(0, len(column_names)):
                column_name = column_names[index]
                # Note the index of Name and Level so that we can use it later for
                # grabbing the correct cells when we grab the whole row.
                if column_name.text == 'Name':
                    name_column_index = index
                elif column_name.text == 'Level':
                    level_column_index = index
            # Now iterate through the rows
            rows = table.find_elements_by_tag_name("tr")
            for row in rows:
                if row.find_elements_by_tag_name("td"):
                    # Grab all the cells from the row
                    cells = row.find_elements_by_tag_name("td")
                    item_level = cells[level_column_index].text
                    item_name = cells[name_column_index].text
                    try:
                        if int(item_level) >= self._settings['lowest_level'] and int(item_level) <= self._settings['highest_level']:
                            self._possible_items.append(
                                {
                                    'name': item_name,
                                    'level': item_level,
                                }
                            )
                            #print("Item name: {0}; Item level: {1}".format(item_name, item_level))
                    except:
                        if self._settings['debug']:
                            print("Skipping {0} as a possible item".format(item_name))
    # end get_equipment_list

    def setup_argparse(self):
        parser = argparse.ArgumentParser('Get a random sampling of Starfinder items')
        parser.add_argument(
            '--armor',
            action = 'store_true',
            default = False,
            dest = 'armor',
            help = 'Select from light armor, heavy armor, and armor upgrades.',
        )
        parser.add_argument(
            '--light-armor',
            action = 'store_true',
            default = False,
            dest = 'light_armor',
            help = 'Select from light armor.',
        )
        parser.add_argument(
            '--heavy-armor',
            action = 'store_true',
            default = False,
            dest = 'heavy_armor',
            help = 'Select from heavy armor.',
        )
        parser.add_argument(
            '--armor-upgrades',
            action = 'store_true',
            default = False,
            dest = 'armor_upgrades',
            help = 'Select from armor upgrades.',
        )
        parser.add_argument(
            '--weapons',
            action = 'store_true',
            default = False,
            dest = 'weapons',
            help = 'Select from all weapon types, ammo, and accessories.',
        )
        parser.add_argument(
            '--advanced-melee',
            action = 'store_true',
            default = False,
            dest = 'advanced_melee',
            help = 'Select from advanced melee weapons.',
        )
        parser.add_argument(
            '--ammunition',
            action = 'store_true',
            default = False,
            dest = 'ammunition',
            help = 'Select from ammunition.',
        )
        parser.add_argument(
            '--basic-melee',
            action = 'store_true',
            default = False,
            dest = 'basic_melee',
            help = 'Select from basic melee weapons.',
        )
        parser.add_argument(
            '--grenade',
            action = 'store_true',
            default = False,
            dest = 'grenade',
            help = 'Select from grenades.',
        )
        parser.add_argument(
            '--heavy-weapon',
            action = 'store_true',
            default = False,
            dest = 'heavy',
            help = 'Select from heavy weapons.',
        )
        parser.add_argument(
            '--longarms',
            action = 'store_true',
            default = False,
            dest = 'longarms',
            help = 'Select from longarm weapons.',
        )
        parser.add_argument(
            '--small-arms',
            action = 'store_true',
            default = False,
            dest = 'small_arms',
            help = 'Select from small arm weapons.',
        )
        parser.add_argument(
            '--sniper',
            action = 'store_true',
            default = False,
            dest = 'sniper',
            help = 'Select from sniper weapons.',
        )
        parser.add_argument(
            '--solarian',
            action = 'store_true',
            default = False,
            dest = 'solarian',
            help = 'Select from solarian weapon crytals.',
        )
        parser.add_argument(
            '--special',
            action = 'store_true',
            default = False,
            dest = 'special',
            help = 'Select from special weapons.',
        )
        parser.add_argument(
            '--weapon-accessories',
            action = 'store_true',
            default = False,
            dest = 'weapon_accessories',
            help = 'Select from weapon accessories.',
        )
        parser.add_argument(
            '--number-of-items',
            '-n',
            action = 'store',
            type = int,
            default = 10,
            dest = 'number_of_items',
            help = 'Number of items to select.',
        )
        parser.add_argument(
            '--lowest-level',
            action = 'store',
            default = 1,
            type = int,
            dest = 'lowest_level',
            help = 'Lowest level of item to select from. Default is 1.'
        )
        parser.add_argument(
            '--highest-level',
            action = 'store',
            default = 20,
            type = int,
            dest = 'highest_level',
            help = 'Highest level of item to select from. Default is 20.'
        )
        parser.add_argument(
            '--seed',
            action = 'store',
            default = int(time.time()),
            type = int,
            dest = 'seed',
            help = "Seed for the random number generator."
        )
        parser.add_argument(
            '--debug',
            '-d',
            action = 'store_true',
            default = False,
            dest = 'debug',
            help = "Enables debug messaging."
        )
        return parser
    # end setup_argparse

    def parse_args(self):
        # Grab all the arguments off the command line
        args = self._arg_parser.parse_args()
        settings = {
            'number_of_items': args.number_of_items,
            'lowest_level': args.lowest_level,
            'highest_level': args.highest_level,
            'seed': args.seed,
            'debug': args.debug,
            'categories': {
                'armor': args.armor,
                'light_armor': args.light_armor,
                'heavy_armor': args.heavy_armor,
                'armor_upgrades': args.armor_upgrades,
                'weapons': args.weapons,
                'advanced_melee': args.advanced_melee,
                'ammunition': args.ammunition,
                'basic_melee': args.basic_melee,
                'grenade': args.grenade,
                'heavy': args.heavy,
                'longarms': args.longarms,
                'small_arms': args.small_arms,
                'sniper': args.sniper,
                'solarian': args.solarian,
                'special': args.special,
                'weapon_accessories': args.weapon_accessories,
            }
        }

        armor_types = [
            'light_armor',
            'heavy_armor',
            'armor_upgrades',
        ]

        weapon_types = [
            'advanced_melee',
            'ammunition',
            'basic_melee',
            'grenade',
            'heavy',
            'longarms',
            'small_arms',
            'sniper',
            'solarian',
            'special',
            'weapon_accessories',
        ]

        # If --armor was specified, set all the armor types to True
        # so that we can iterate through all of them
        if settings['categories']['armor']:
            for armor_type in armor_types:
                settings['categories'][armor_type] = True
        
        # If any of the individual armor categories were True then set the 
        # top level armor category to True to ensure the individual category
        # will be iterated over
        for armor_type in armor_types:
            if settings['categories'][armor_type]:
                settings['categories']['armor'] = True
                break

        # If --weapons was specified, set all the weapon types to True
        # so that we can iterate through all of them
        if settings['categories']['weapons']:
            for weapon_type in weapon_types:
                settings['categories'][weapon_type] = True

        # If any of the individual weapon categories were True then set the 
        # top level weapons category to True to ensure the individual category
        # will be iterated over
        for weapon_type in weapon_types:
            if settings['categories'][weapon_type]:
                settings['categories']['weapons'] = True
                break

        # Do a check to see if no item types were specified on the command line.
        # If this is the case then we want to treat this as the user wanting to
        # iterate through every category rather than none.
        all_categories = True
        for category_name in settings['categories'].keys():
            if settings['categories'][category_name]:
                all_categories = False
                break
        
        if all_categories:
            for category_name in settings['categories'].keys():
                settings['categories'][category_name] = True

        # Do bounds checking on the lowest and highest levels, and adjust as
        # needed
        if settings['lowest_level'] < 1:
            settings['lowest_level'] = 1
        if settings['highest_level'] > 20:
            settings['highest_level'] = 20
        if settings['lowest_level'] > settings['highest_level']:
            settings['lowest_level'] = settings['highest_level']

        return settings
    # end parse_args

    def select_items(self, item_list, number_of_items):
        if number_of_items > len(item_list):
            return item_list
        random.shuffle(item_list)
        sliceable_array = numpy.array(item_list)
        return sliceable_array[:number_of_items]
    # end select_items

    def run_randomizer(self):
        self._settings = self.parse_args()

        definitions = self.get_definitions()
        
        # Set the seed
        print("Random seed: {0}".format(self._settings['seed']))
        random.seed(self._settings['seed'])

        # Start up the browser
        self._driver = webdriver.Firefox()

        # Load the main page
        self._driver.get(definitions["main_page"]["url"])

        # Navigate to the Equipment page
        self.load_page(
            link_text = "Equipment",
            url = definitions["equipment_page"]["url"],
            categories = definitions["equipment_page"]["categories"],
        )

        # Now iterate through the categories
        self.load_categories(
            categories = definitions["equipment_page"]["categories"],
        )

        # Grab the required number of random items
        selected_items = self.select_items(
            self._possible_items,
            self._settings['number_of_items'],
        )

        # Report the selected items
        print("Selected items ({0}):".format(len(selected_items)))
        for item in selected_items:
            print("{0} (Lvl {1})".format(item['name'], item['level']))

        # Lastly, quit the driver so the browser closes cleanly
        self._driver.quit()

if __name__ == '__main__':
    exit(EquipmentRandomizer().run_randomizer())