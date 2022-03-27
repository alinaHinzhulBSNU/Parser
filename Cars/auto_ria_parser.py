# PARSER

import requests
from bs4 import BeautifulSoup
import csv
from beautifultable import BeautifulTable
from datetime import datetime
from car import Car
import config


# Load HTML page
def get_html_page(url, params=None):
    r = requests.get(url, headers=config.HEADERS, params=params)
    return r


# Get certain HTML element
def get_html_element(parent, tag, class_, only_one_class=False):
    if only_one_class:
        elements = parent.select(f"[class='{class_}']")
        text = elements[0].get_text(strip=True) if len(elements) != 0 else None
    else:
        element = parent.find(tag, class_=class_)
        text = extract_text(element)

    return text


# Get text from HTML element
def extract_text(html_element):
    return html_element.get_text(strip=True) if html_element is not None else None


# Get link from HTML element
def get_link_from_html_element(parent, tag, class_):
    short_link = parent.find(tag, class_=class_)
    full_link = config.HOST + short_link.get('href') if short_link is not None else None
    return full_link


# Get quantity of pages
def get_pages_count(html):
    soup = BeautifulSoup(html.text, config.PARSER)
    pagination = soup.findAll(config.pagination.tag, class_=config.pagination.class_)

    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1


# GET INFORMATION ABOUT CARS FROM HTML
def get_cars(html):
    soup = BeautifulSoup(html, config.PARSER)
    propositions = soup.findAll(config.proposition.tag, config.proposition.class_)

    cars = []
    for proposition in propositions:
        title = get_html_element(proposition, config.title.tag, config.title.class_)
        link = get_link_from_html_element(proposition, config.link.tag, config.link.class_)
        price_usd = get_html_element(proposition, config.price_usd.tag, config.price_usd.class_)
        price_uah = get_html_element(proposition, config.price_uah.tag, config.price_uah.class_, True)

        city, transmission, drive, fuel_type, engine_capacity = None, None, None, None, None

        proposition_information = proposition.findAll(config.proposition_information.tag, class_=config.proposition_information.class_)
        for element in proposition_information:
            if config.fuel_data.class_ in element.i['class']:
                fuel_data = extract_text(element).split('•')
                fuel_type = fuel_data[0] if len(fuel_data) >= 1 else None
                engine_capacity = fuel_data[1] if len(fuel_data) == 2 else None
            if any(class_ in [config.transmission.class_, config.automatic_transmission.class_] for class_ in element.i['class']):
                transmission = extract_text(element)
            if config.drive.class_ in element.i['class']:
                drive = extract_text(element)
            if config.city.class_ in element['class']:
                city = extract_text(element)

        car = Car(title, link, price_usd, price_uah, city, transmission, fuel_type, engine_capacity, drive)
        if car.is_not_empty():
            cars.append(car)

    return cars


# PRINT
def print_table(cars):
    table = BeautifulTable(maxwidth=300)
    table.columns.header = config.COLS
    for car in cars:
        table.rows.append(car.to_list())
    print(table)


# SAVE
def save_data_to_csv_file(cars, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(config.COLS)
        for car in cars:
            writer.writerow(car.to_list())


# START PARSING
def parse():
    print("-----PARSING OF AUTO.RIA.com-----")
    now = datetime.now()
    current_date = now.strftime("%d.%m.%Y %H:%M:%S")
    print(current_date + '\n')

    url = input('Input URL (example: https://auto.ria.com/uk/newauto/marka-nissan/): ')

    html = get_html_page(url)
    if html.status_code == 200:
        cars = []

        pages_count = get_pages_count(html)
        for page in range(1, pages_count + 1):
            print(f'{page} / {pages_count} pages parsed')
            html = get_html_page(url, params={'page': page})
            cars.extend(get_cars(html.content))

        action = ''
        while action != '1' and action != '2':
            action = input('\nChoose action: \n\t1 - print table\n\t2 - save to CSV file\n')

        if action == '1':
            print_table(cars)
        elif action == '2':
            path = input('Input folder for CSV file (example: C:/Users/User/Desktop/): ')
            full_path = path + config.FILE
            save_data_to_csv_file(cars, full_path)

        print(f'\nInformation about {len(cars)} cars collected successfully!')
    else:
        print('Invalid URL')
