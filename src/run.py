from multiprocessing import Process
import alert_updater
from src.app import app

if __name__ == '__main__':
    p = Process(target=alert_updater.update_alert)
    p.start()
    app.run(debug=app.config['DEBUG'], port=5000, use_reloader=False)
    p.join()
