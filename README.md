=MiHive

Data recorder for Hive active heating systems (http://www.hivehome.com)

Downloads core Hive data from the website for your own use.
 
==Instalation

* This was designed to run on a raspberry pi or other unix system and use cron to download data every 5 minutes.

1. Rename config.json.example to config.json and edit the file to add your username, password and data directory (make sure it exists)
2. Edit MiHive.cron to specifically list the location of the app.
4. Run "python MiHive.py" to test it works
5. Run "crontab MiHive.cron" to set it up to log every 5 minutes.

