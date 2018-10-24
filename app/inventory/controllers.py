"""
This module implements various controllers related with inventory apis

@author: Rohit Chormale
"""


import datetime
from flask import render_template, jsonify, request, flash
from flask_login import current_user, login_required
from app import app
from app.helpers import generate_transaction_id
from .models import Inventory, Transaction, FPCredit
from .forms import AddInventoryForm, PurchaseItemForm, PurchasePointsForm


@login_required
def dashboard():
    """Dashboard for user"""
    return render_template('dashboard.html', user=current_user, inventory=get_inventory_aggregate())


@login_required
def get_inventory_aggregate():
    """Return aggregate inventory list of current user"""
    inventory_aggregate = dict()
    for i in current_user.inventory_list:
        inventory_aggregate[i.name] = inventory_aggregate.get(i.name, 0) + 1
    return inventory_aggregate


@login_required
def get_account():
    """Return user's account info like free_points, purchased_points and inventory_list"""
    data = {"free_points": current_user.free_points, "purchased_points": current_user.purchased_points,
            "inventory_list": current_user.inventory_list, "inventory_aggregate": get_inventory_aggregate()}
    return jsonify(data), 200


@login_required
def get_points():
    """Returns user's current free points and purchased points"""
    data = {"free_points": current_user.free_points, "purchased_points": current_user.purchased_points}
    return jsonify(data), 200


@login_required
def purchase_points():
    """Purchase points. This is stub controller for testing only"""
    form = PurchasePointsForm()
    if request.method == "POST" and form.validate():
        points = int(form.points.data)
        current_user.purchased_points += points
        try:
            current_user.save()
            flash("Vola !!! Let's spend some money")
        except Exception as e:
            flash("Please try again after sometime")
    return render_template("points.html", user=current_user, form=form)


@login_required
def purchase_item():
    """Purchase items from inventory. Use can buy same item multiple time"""
    form = PurchaseItemForm()
    if request.method == "POST" and form.validate():
        name = form.name.data
        inventory = Inventory.objects(name=name).first()
        if inventory is None:
            flash("Sorry !!! Item is not available anymore.")
            return render_template("items.html", inventory=Inventory.objects.all(), form=form)

        price = inventory.points
        # discard if not enough balance
        if price > (current_user.free_points + current_user.purchased_points):
            flash("Not enough balance")
            return render_template("items.html", inventory=Inventory.objects.all(), form=form)

        trans_fp = None
        trans_pp = None
        timestamp = datetime.datetime.now()
        trans_id = generate_transaction_id()
        user = current_user._get_current_object()
        if (current_user.free_points - price) >= 0:
            # use fp
            current_user.free_points = current_user.free_points - price
            trans_fp = Transaction(user=user, trans_type="FP", trans_id=trans_id, points=-price, description="Purchased %s" % name, timestamp=timestamp)
        elif current_user.free_points == 0:
            # use pp
            current_user.purchased_points = current_user.purchased_points - price
            trans_pp = Transaction(user=user, trans_type="PP", trans_id=trans_id, points=-price, description="Purchased %s" % name, timestamp=timestamp)
        else:
            # use fp and pp
            required_pp = current_user.free_points - price
            current_user.purchased_points = current_user.purchased_points + required_pp
            trans_fp = Transaction(user=user, trans_type="FP", trans_id=trans_id, points=-current_user.free_points, description="Purchased %s" % name, timestamp=timestamp)
            current_user.free_points = 0
            trans_pp = Transaction(user=user, trans_type="PP", trans_id=trans_id, points=required_pp, description="Purchased %s" % name, timestamp=timestamp)

        current_user.inventory_list.append(inventory)
        try:
            current_user.save()
            if trans_fp: trans_fp.save()
            if trans_pp: trans_pp.save()
            if current_user.free_points < int(app.config["FP_CREDIT_MAX_POINTS"]):
                if FPCredit.objects(user=user).first() is None:
                    fp_credit = FPCredit(user=user, timestamp=timestamp)
                    fp_credit.save()
            flash("Congrats !!! You just bought %s !!!" % name)
        except Exception as e:
            print(e)
            flash("Sorry !!! Please try after sometime !!!")
            return render_template("items.html", inventory=Inventory.objects.all(), form=form)

    return render_template("items.html", inventory=Inventory.objects.all(), form=form)


@login_required
def get_items():
    """Return list of purchased items"""
    offset = request.args.get("offset", None)
    limit = request.args.get("limit", None)
    if offset is None or limit is None:
        return jsonify(current_user.inventory_list), 200
    else:
        return jsonify(current_user.inventory_list[int(offset):int(limit)]), 200


@login_required
def get_inventory():
    """Get all available items to purchase"""
    data = Inventory.objects.all()
    return jsonify(data), 200


# additional apis
@login_required
def add_inventory():
    """Add items to purchase. Only admin can update them."""
    form = AddInventoryForm()
    if not current_user.admin:
        flash("Only admin can update inventory.")
        return render_template("inventory.html", inventory=Inventory.objects.all(), form=form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        points = int(form.points.data)
        if name is not None and points is not None:
            Inventory.objects(name=name).modify(upsert=True, new=True, set__points=points)
    return render_template("inventory.html", inventory=Inventory.objects.all(), form=form)


@login_required
def get_transactions():
    """Return transactions of users"""
    offset = request.args.get("offset", None)
    limit = request.args.get("limit", None)
    if offset is None or limit is None:
        transactions = Transaction.objects(user=current_user._get_current_object()).order_by("-timestamp")
        return jsonify(transactions), 200
    transactions = Transaction.objects(user=current_user._get_current_object()).skip(int(offset)).limit(int(limit)).order_by("-timestamp")
    return jsonify(transactions), 200
