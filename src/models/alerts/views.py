from flask import Blueprint, request, render_template, session, redirect, url_for
import src.models.users.decorators as user_decorators
from src.common.utils import Utils
from src.models.alerts.alert import Alert
from src.models.items.item import Item
from src.models.priceLogs.price_log import Price

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/new_alert/<string:store_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def create_alert(store_id):
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']
        price_limit = Utils.get_price_float(request.form['price_limit'])
        item = Item(name, url, store_id)
        item.save_to_mongo()
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()

    return render_template("alerts/new_alert.html",
                           store_id=store_id)

@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    if request.method == 'POST':
        price_limit = Utils.get_price_float(request.form['price_limit'])
        alert = Alert.find_by_id(alert_id)
        alert.price_limit = price_limit
        alert.load_item_price()
        return redirect(url_for('.get_alert_page', alert_id=alert_id))

    # METHOD GET
    return render_template("alerts/edit_alert.html",
                           alert=Alert.find_by_id(alert_id))

@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    Alert.find_by_id(alert_id).deactivate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    Alert.find_by_id(alert_id).activate()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    Alert.find_by_id(alert_id).delete()
    return redirect(url_for('users.user_alerts'))

@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    #passing price and dates list in order to draw a chart
    price_list = []
    date_list = []
    prices = Price.get_user_price_by_alert(alert_id, alert.activate_date)

    for price in prices:
        price_list.append(price.price)
        date_list.append(price.create_date)

    return render_template('alerts/alert.html', alert=alert, price_list=price_list, date_list=date_list)

@alert_blueprint.route('/check_price/<string:alert_id>')
def check_alert_price(alert_id):
    Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id=alert_id))
