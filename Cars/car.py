# MODEL of the car data

class Car:
    def __init__(self, title, link, price_usd, price_uah, city, transmission, fuel_type, engine_capacity, drive):
        self.title = title
        self.link = link
        self.price_usd = str(price_usd).replace('$', '').strip()
        self.price_uah = str(price_uah).replace('грн', '').strip()
        self.city = city
        self.transmission = transmission
        self.fuel_type = fuel_type
        self.engine_capacity = str(engine_capacity).replace('л', '').strip()
        self.drive = str(drive).replace('привід', '').strip()

    def to_list(self):  # According to COLS from config!
        return [self.title,
                self.transmission,
                self.fuel_type,
                self.engine_capacity,
                self.drive,
                self.price_usd,
                self.price_uah,
                self.city,
                self.link]

    def is_not_empty(self):  # No actual car data without name and link
        return (self.title and self.link) is not None
