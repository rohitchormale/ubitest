"""
This module implements various blueprints and routers for different controllers related with inventory management.

@author: Rohit Chormale
"""


from flask import Blueprint
from .controllers import *

inventory_blueprint = Blueprint('inventory', 'inventory', url_prefix='/inventory')

inventory_blueprint.add_url_rule('dashboard', 'dashboard', dashboard, methods=["GET",])
inventory_blueprint.add_url_rule('connect', 'connect', get_account, methods=["GET",])

inventory_blueprint.add_url_rule('getPoints', 'getPoints', get_points, methods=["GET",])
inventory_blueprint.add_url_rule('purchasePoints', 'purchasePoints', purchase_points, methods=["GET", "POST"])

inventory_blueprint.add_url_rule('getItems', 'get_items', get_items, methods=["GET",])
inventory_blueprint.add_url_rule('purchaseItem', 'purchaseItem', purchase_item, methods=["GET", "POST"])

inventory_blueprint.add_url_rule('getInventory', 'getInventory', get_inventory, methods=["GET"])
inventory_blueprint.add_url_rule('addInventory', 'addInventory', add_inventory, methods=["GET", "POST"])


inventory_blueprint.add_url_rule('getTransactions', 'getTransactions', get_transactions, methods=["GET",])


