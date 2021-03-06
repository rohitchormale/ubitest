# ubitest v0.1

## Installation (Tested on Linux Mint 19/Ubuntu 18)


### mongodb
- `apt install mongodb`
- On finishing installation, mongodb will start automatically. If it doesn't,  then start it explicitly by `systemctl start mongodb`


### Restrict access to specific ips
- Only allow requests from webserver on port 27017 `sudo ufw allow from <webserver-ip>/32 to any port 27017`
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
- `apt install python3-pip`
- `pip3 install -r requirements.txt`


## Configuration

### mongodb

### flask package
- Add confidential config in `instance/config.py`. Do not commit this file. Common config can be ketp at `config.py`


## Usage
- FreePoints Credit service can be run using `bin/fpcservice.sh` assuming you're in project root directory
- Run this service via crontab as `* * * * * <project-root-dir>/bin/fpcservice.sh > /dev/null`
- Development server can be started as `python run.py` assuming you're in project root directory
- Do NOT use development server for production development.



## API References

- /inventory/connect/
    ```
    /GET
    Returns user's account info like free_points, purchased_points, inventory_list etc
    Sample Response -
    {
      "free_points": 0,
      "purchased_points": 50,
      "inventory_aggregate": {
        "healing potion": 1,
        "notebook": 1,
        "sentry": 1
      },
      "inventory_list": [
        {
          "_id": {
            "$oid": "5bd08a0d9c22ac8142abc759"
          },
          "name": "healing potion",
          "points": 100
        },
        {
          "_id": {
            "$oid": "5bd08a839c22ac8142abc796"
          },
          "name": "notebook",
          "points": 0
        },
        {
          "_id": {
            "$oid": "5bd08aa09c22ac8142abc7a7"
          },
          "name": "sentry",
          "points": 300
        }
      ],
    }
    ```

- /inventory/getPoints
    ```
    /GET
    Returns user's free points and purchased points
    Sample Response -
    {
      "free_points": 0,
      "purchased_points": 50
    }
    ```

- /inventory/purchasePoints
    ```
    /POST
    Purchase points. For testing only
    ```

- /inventory/getItems or /inventory/getItems?offset=7&limit=2
    ```
    /GET
    Returns all items purchased by/credited to user
    Sample Response -
    [
      {
        "_id": {
          "$oid": "5bd08a0d9c22ac8142abc759"
        },
        "name": "healing potion",
        "points": 100
      },
      {
        "_id": {
          "$oid": "5bd08a839c22ac8142abc796"
        },
        "name": "notebook",
        "points": 0
      },
    ]
    ```

- /inventory/purchaseItem
    ```
    /POST
    Purchase one of the item from inventory
    ```

 - /inventory/getTransactions or /inventory/getTransactions?offset=5&limit=5
    ```
    /GET
    Returns transactions of given user
    Sample Response -
    [
      {
        "_id": {
          "$oid": "5bcf98780aadd461c29a5670"
        },
        "description": "Purchased notebook",
        "points": 0,
        "timestamp": {
          "$date": 1540351440658
        },
        "trans_id": "2b1f33d5-7f2f-42cd-9e7f-fa10750f185d",
        "trans_type": "FP",
        "user": {
          "$oid": "5bcf28240aadd47fd98156e2"
        }
      }
    ```

- /inventory/getInventory
    ```
    /GET
    Returns all items available to purchase
    Sample Response-
    [
      {
        "_id": {
          "$oid": "5bd08a0d9c22ac8142abc759"
        },
        "name": "healing potion",
        "points": 100
      },
      {
        "_id": {
          "$oid": "5bd08a839c22ac8142abc796"
        },
        "name": "notebook",
        "points": 0
      },
    ]
    ```

- /inventory/addInventory
    ```
    /POST
    Add new items in inventory to purchase
    Only admin can call it
    ```


## Notes
- User can buy same item multiple times. All items will be tracked separately.
- As transaction data can become huge later, it is separated in another collection.
- Minimum cost of item can be 0.
- freepoints credit service is enabled for user, at 2 events
    - after registration
    - when free points go down below `FP_CREDIT_MAX_POINTS`(here 200) during purchase


