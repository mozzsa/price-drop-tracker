import datetime
import uuid
import src.models.priceLogs.constants as PriceConstants
from src.common.database import Database

class Price(object):
    # this class's objective is to collect the priceLogs from
    # every scan to show the user analyze the price fluctuations form the day they activate their alerts
    def __init__(self, alert_id, price, create_date=None, _id=None):
        self.alert_id = alert_id
        self.create_date = datetime.datetime.utcnow() if create_date is None else create_date
        self.price = price
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_user_price_by_alert(cls, alert_id, activate_date, ):
        return [cls(**price) for price in Database.find(PriceConstants.COLLECTION,
                                                        {"alert_id": alert_id, "create_date": {"$gte": activate_date}})]

    def save_to_mango(self):
        Database.insert(PriceConstants.COLLECTION, self.json())

    def json(self):
        return {
            "alert_id": self.alert_id,
            "create_date": self.create_date,
            "price": self.price,
            "_id": self._id
        }
