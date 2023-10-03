from flask import Blueprint, render_template
from models import db
from models import Lemonade, User

dish_page = Blueprint('dish_page', __name__,
                        template_folder='templates_dishes')



@dish_page.route('/<int:item_number>')
def generic(item_number):
    item = Lemonade.query.filter_by(id = item_number).first()
    return render_template('templates_dishes/generic.html', item = item)



@dish_page.route('/')
def generic0():
    page = db.paginate(db.select(Lemonade).order_by(Lemonade.id))
    return render_template('templates_dishes/generic0.html', pagination = page)
