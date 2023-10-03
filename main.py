from flask import Flask, render_template, redirect, request
from models import Lemonade, User, MyView, Comment
from models import db
from dishes import dish_page
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user
from wtforms_alchemy import ModelForm
from dotenv import load_dotenv
import os
import random
from mail_part import send_mail, mail


load_dotenv()
login_manager = LoginManager()

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = os.environ['MAIL_SERVER'],
    MAIL_PORT = os.environ['MAIL_PORT'],
    MAIL_USE_SSL = os.environ['MAIL_USE_SSL'],
    MAIL_USERNAME = os.environ['MAIL_USERNAME'],
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD'],
)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DB']
app.secret_key = os.environ['key']
app.app_context().push()
app.register_blueprint(dish_page, url_prefix = '/dish')

mail.init_app(app)
db.init_app(app)
login_manager.init_app(app)

'''for i in range(200):
    lemoned = Lemonade(id = i, place = f'place {i}', place_id = i,
                       description = random.randrange(1000))
    db.session.add(lemoned)
db.session.commit()'''

'''uss = User(id = 1, login = 'Lamiroth', password = 'Jinni030507')
db.session.add(uss)
db.session.commit()'''

class UserForm(ModelForm):
    class Meta:
        model = User
        
class AuthModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect('/')


with app.app_context():
    db.create_all()
    send_mail(
        title =' One message',
        body = 'Msg',
        from_p = "ilatroh@gmail.com",
        to_p = ['thormyl@lic145.kiev.ua'])
    
@login_manager.user_loader
def get_user(ident):
    return User.query.get(ident)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/elements')
def elements():
    return render_template('elements.html')



@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':
        data = request.form
        user = User.query.filter(User.login == data.get('login'))\
        .filter(User.password == data.get('password')).first()
        if user:
            login_user(user)
            return redirect('/')
    return render_template('login.html', form = form)
    



@app.errorhandler(404)
def error_404(e):
    return "Такої сторінки не існує"

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')





admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(AuthModelView(Lemonade, db.session))
admin.add_view(AuthModelView(User, db.session))
admin.add_view(AuthModelView(Comment, db.session))
if __name__ == '__main__':
    app.run()
