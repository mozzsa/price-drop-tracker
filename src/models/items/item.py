import re
import uuid
import requests
from bs4 import BeautifulSoup
import src.models.items.constants as ItemConstants
from src.common.database import Database
from src.common.utils import Utils
from src.models.stores.store import Store

class Item(object):
    def __init__(self, name, url, store_id, price=None, _id=None):
        self.name = name
        self.url = url
        self.store_id = store_id
        store = Store.get_by_id(store_id)
        self.tag_name = store.tag_name
        self.query = store.query
        self.price = None if price is None else price
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.url)

    def load_price(self):
        request = requests.get(self.url)
        content = request.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        #amazon
        # element = soup.find("span", {"id": "price_inside_buybox","class": "a-size-medium a-color-price"})
        string_price = element.text.strip()
        pattern = re.compile("[0-9]+([,.][0-9]+)+") # get the price
        match = pattern.search(string_price)
        self.price = Utils.get_price_float(match.group())
        return self.price

    def save_to_mongo(self):
        Database.update(ItemConstants.COLLECTION, {'_id': self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "store_id": self.store_id,
            "name": self.name,
            "url": self.url,
            "price": self.price
        }

    @classmethod
    def get_by_id(cls, item_id):
        return cls(**Database.find_one(ItemConstants.COLLECTION, {"_id": item_id}))
