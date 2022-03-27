# SETTINGS for parser. Change class and tag of HTML elements according to actual website`s state

from html_element import HtmlElement

# General
PARSER = 'html.parser'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36',
    'accept' : '*/*'
}
HOST = 'https://auto.ria.com'
COLS = ['Title', 'Transmission', 'Fuel', 'Engine', 'Drive', 'USD', 'UAH', 'City', 'Link']
FILE = 'cars.csv'

# HTML
pagination = HtmlElement('span', 'mhide')

proposition = HtmlElement('section', 'proposition')
title = HtmlElement('span', 'link')
link = HtmlElement('a', 'proposition_link')
price_usd = HtmlElement('span', 'size22')
price_uah = HtmlElement('span', 'size16')

proposition_information = HtmlElement('span', 'item')
city = HtmlElement('span', 'region')
drive = HtmlElement('i', 'i16_drive_stroke')
fuel_data = HtmlElement('i', 'i16_engine')
transmission = HtmlElement('i', 'i16_transmission')
automatic_transmission = HtmlElement('i', 'i16_automat')