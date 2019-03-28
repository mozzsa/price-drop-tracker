from src.common.database import Database
from src.models.alerts.alert import Alert
from src.models.priceLogs.price_log import Price

#scans the website of the item a defined period of time(ALERT_TIMEOUT)
# updates the prices of items and inserts the logs to priceLogs table
# to analyse the item prices from the date the alert was activated
# in order to show the user price fluctuations
def update_alert():
    while True:
        Database.initialize()
        alerts_needing_update = Alert.find_needing_update()
        for alert in alerts_needing_update:
            price = alert.load_item_price()
            price_data = Price(alert._id, price)
            price_data.save_to_mango()
            alert.send_email_if_price_reached()
