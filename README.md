# ubitest v0.1

## Installation (Tested on Linux Mint 19)


### mongodb
apt-get install mongodb

### flask package
- `apt-get install python3-pip`
- `pip3 install -r requirements.txt`


## Configuration

### mongodb
- open 27017 port on mongodb-server, for webserver-ip if webserver hosted on another machine. `sudo ufw allow from <webserver-ip>/32 to any port 27017`

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
    ````
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


