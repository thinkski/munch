# munch
Command line interface to Munchery (https://munchery.com)


## Installation

Munch is written in Python (developed with Python 2.7). It depends on BeautifulSoup. To install the dependencies:

    pip install -r requirements.txt
    
Then to install munch:

    python setup.py install


## Quickstart

To retrieve today's menu for your zip code, for example for San Francisco:

    munch --zipcode 94110 > menu.json

This will return JSON data with the menu. You can then parse this with your own script. For example, to show the number of calories per dollar for each item:

    with open("menu.json", "r") as f:
        data = json.load(f)
    
    for section in data['menu']['sections']:
        for item in section['items']:
            price = float(item['price']['dollars']) + float(item['price']['cents']) / 100
            name = item['name']
            if item.has_key('nutrition_facts'):
                calories = item['nutrition_facts']['calories']
                print calories / price, name
