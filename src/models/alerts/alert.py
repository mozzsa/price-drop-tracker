import datetime
import smtplib
import uuid
import src.models.alerts.constants as AlertConstants
from src.common.database import Database
from src.models.items.item import Item

class Alert(object):
    def __init__(self, user_email, price_limit, item_id, active=True, last_checked=None, _id=None, activate_date=None,
                 deactivate_date=None):
        self.user_email = user_email
        self.price_limit = price_limit
        self.active = active
        self.item = Item.get_by_id(item_id)
        self.last_checked = datetime.datetime.utcnow() if last_checked is None else last_checked
        self.activate_date = datetime.datetime.utcnow() if activate_date is None else activate_date
        self.deactivate_date = "" if deactivate_date is None else deactivate_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<Alert for {} on item {} with price {}>".format(self.user_email, self.item.name, self.price_limit)

    def send(self):
        subject = "Price limit reached for {}".format(self.item.name)
        body = "We've found a deal! ({}).".format(self.item.url)
        sent_from = AlertConstants.FROM
        key = AlertConstants.KEY
        to = self.user_email
        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s
        Body: %s
        """ % (sent_from, ", ".join(to), subject, body)
        try:
            server = smtplib.SMTP_SSL(AlertConstants.URL, AlertConstants.PORT)
            server.ehlo()
            server.login(sent_from, key)
            server.sendmail(sent_from, self.user_email, email_text)
            server.close()
            print 'Email sent!'
        except smtplib.SMTPException:
            print 'Unable to send an e-mail'

    @classmethod
    def find_needing_update(cls, minutes_since_update=AlertConstants.ALERT_TIMEOUT):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minutes_since_update)
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION,
                                                      {"last_checked":
                                                           {"$lte": last_updated_limit},
                                                       "active": True
                                                       })]

    #if there is a data match it updates the table or inserts data to the database
    def save_to_mongo(self):
        Database.update(AlertConstants.COLLECTION, {"_id": self._id}, self.json())

    def json(self):
        return {
            "_id": self._id,
            "price_limit": self.price_limit,
            "last_checked": self.last_checked,
            "user_email": self.user_email,
            "item_id": self.item._id,
            "active": self.active,
            "activate_date": self.activate_date,
            "deactivate_date": self.deactivate_date
        }

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.item.save_to_mongo()
        self.save_to_mongo()
        return self.item.price

    def send_email_if_price_reached(self):
        if self.item.price <= self.price_limit:
            self.send()

    @classmethod
    def find_by_user_email(cls, user_email):
        return [cls(**elem) for elem in Database.find(AlertConstants.COLLECTION, {'user_email': user_email})]

    @classmethod
    def find_by_id(cls, alert_id):
        return cls(**Database.find_one(AlertConstants.COLLECTION, {'_id': alert_id}))

    def deactivate(self):
        self.active = False
        self.deactivate_date = datetime.datetime.utcnow()
        self.save_to_mongo()

    def activate(self):
        self.active = True
        self.activate_date = datetime.datetime.utcnow()
        self.save_to_mongo()

    def delete(self):
        Database.remove(AlertConstants.COLLECTION, {'_id': self._id})
