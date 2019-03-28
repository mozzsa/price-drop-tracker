# Price Drop Tracker

This app scans periodically online webstores to notify users when prices of items go under price limits they define.

It allows users to register,log in,log out,list the supported stores and create alerts of items on the stores they choose.

Users can modify,deactivate, activate or delete permanently their alerts anytime.

Also,they can track price fluctuations of the items from the day they activate their alerts and can compare visually item prices and price limit they put on . 

Only administrators can add,remove or edit online stores.Define them in `src/config.py`, add the e-mails of the administrators to the set named ADMINS in the file.

You should need a gmail account to send  e-mails to the users.Define the account details of the e-mail address you want to send an e-mail from in `src/alert_updater.py`.


Technology stack: MongoDB, Python (Flask,Jinja2), HTML/CSS/Bootstrap, Google Chart API.




