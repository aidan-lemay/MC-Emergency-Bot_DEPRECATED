## Python Bot for Linux-Based Web Servers
#### Created by Aidan LeMay, https://aidanlemay.com/

***

### Setting Up the Project
*This Guide assumes you are operating on a standard Linux installation (written using Ubuntu 20.04 Server), have Sudo privelages, and have Python3.8.10 (Minimum!) installed.*

* Clone the project into the directory of your choice and `cd` into it
* Activate or install your Virtual Environment if needed
* Run `pip install -r requirements.txt`

-- OR --

* Clone the project into the directory of your choice and `cd` into it
* Activate or install your Virtual Environment if needed
* `python3 -m pip install -U discord.py`
* `python3 -m pip install -U discord-py-slash-command`
* `python3 -m pip install -U discord-py-interactions`
* `python3 -m pip install -U pandas`
* `python3 -m pip install -U requests_html`

-- THEN --

* `cp storage.txt storage.py`
* `nano storage.py` and change the placeholder tokens to those of your bot (Can be obtained at https://discord.com/developers/ ) and the Guild ID's of the servers where it will be operating. Press `Ctrl + X`, then `Y`, then `Enter` to save and exit Nano
* Add your bot to your server with `https://discordapp.com/api/oauth2/authorize?client_id=<CLIENT_ID_HERE>&permissions=8&scope=bot`
* `python3 bot.py` to run your bot

-- To Run Your Bot Headless / In The Background --

* Install NPM (Node.JS Package Manager)
* `sudo npm install pm2 -g`
* `pm2 ls`
* `pm2 start bot.py --watch` (Omit `--watch` if you don't want your project auto-served when the project files are changed)

### Command Definitions
* `/help`: Displays Help command with these definitions
* `/M911 X#` [X#: Optional Quantity]: Returns X# of Monroe County 911 Events (Default 1) from https://www.monroecounty.gov/incidents911.rss