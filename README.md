# ubitest v0.1

## Installation (Tested on Linux Mint 19)


### mongodb
apt-get install mongodb

### flask package
apt-get install python3-pip
pip3 install -r requirements.txt


## Configuration

### mongodb
- open 27017 port on mongodb-server, for webserver-ip if webserver hosted on another machine. `sudo ufw allow from <webserver-ip>/32 to any port 27017`

### ubitest packate
- Add confidential config in `instance/config.py`. Do not commit this file. Common config can be ketp at `config.py`


## Usage
- Development server can be started as `python run.py` assuming you're in project root directory
- FreePoints Credit service can be run using `bin/fcpservice.sh` assuming you're in project root directory
- Run this service via crontab as `* * * * * <project-root-dir>/bin/fcpservice.sh > /dev/null`
- Do NOT use development server for production development.



## API Reference


