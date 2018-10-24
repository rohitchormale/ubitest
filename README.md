# ubitest v0.1

## Installation (Tested on Linux Mint 19)


### mongodb
- `apt-get install mongodb`
- On install mongodb will start automatically. If not then run command `systemctl start mongodb`


### Restrict access to specific ips
- open 27017 port on mongodb-server, for <webserver-ip> if webserver hosted on another machine. `sudo ufw allow from <webserver-ip>/32 to any port 27017`
- If webapp is on another server, instead running mongodb on all interface, restrict to private ip only by editing
    `/etc/mongodb.conf`, set value of `bind_ip` to both ips as `bind_ip = 127.0.0.1,<private-ip>`


### Secure access to mongodb using username and password
- Edit `/etc/mongodb.conf` and set value of `auth = True`
- Now connect to mongodb using command line client and execute below commands

    ```
    use <dbname>
    db.createUser({ user: "<dbuser>", pwd: "<dbpasswrd", roles: [ { role: "readWrite", db: "<dbname>" }, { role: "dbAdmin", db: "<dbname>" } ] })
    ```
- Test your connection

    ```
    use <dbname>
    db.auth("<dbuser>", "<dbpasswrd>")
    ```
- Now exit from mongo-client and restart db as `systemctl mongodb restart`.
- Now use details mentioned above in your webapp to connect mongodb


### flask package
- `apt-get install python3-pip`
- `pip3 install -r requirements.txt`


## Configuration

### mongodb

### flask package
- Add confidential config in `instance/config.py`. Do not commit this file. Common config can be ketp at `config.py`


## Usage
- Development server can be started as `python run.py` assuming you're in project root directory
- FreePoints Credit service can be run using `bin/fcpservice.sh` assuming you're in project root directory
- Run this service via crontab as `* * * * * <project-root-dir>/bin/fcpservice.sh > /dev/null`
- Do NOT use development server for production development.



## API References

- /inventory/connect/
    ```
    /GET
    Returns user's account info like free_points, purchased_points, inventory_list etc
    ```

- /inventory/getPoints
    ```
    /GET
    Returns user's free points and purchased points
    ```

- /inventory/purchasePoints
    ```
    /POST
    Purchase points. For testing only
    ```

- /inventory/getItems
    ```
    /GET
    Returns all items purchased by/credited to user
    ```

- /inventory/purchaseItem
    ```
    /POST
    Purchase one of the item from inventory
    ```

- /inventory/getInventory
    ```
    /GET
    Returns all items available to purchase
    ```

- /inventory/addInventory
    ```
    /POST
    Add new items in inventory to purchase
    Only admin can call it
    ```



## Notes
- User can buy same item multiple times. All items will be tracked separately.
- As transaction data can become huge later, it is kept separate in another collection.
- freepoints credit service is enabled for user, at 2 events
    - after registration
    - when free points go down below `FP_CREDIT_MAX_POINTS`(here 200) during purchase


