from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from flask_login import UserMixin


db = SQLAlchemy()






class MyView(ModelView):
    form_extra_fields = {
        'img': ImageUploadField(base_path = 'static')
    }


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))
    rews = db.relationship('Lemonade', backref = 'users')
    rews2 = db.relationship('Comment', backref = 'users')

    def __str__(self):
        return self.login


class Lemonade(db.Model):
    __tablename__ = 'lems'
    id = db.Column(db.Integer, primary_key = True)
    place = db.Column(db.String(50))
    place_id = db.Column(db.String(100))
    description = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey('users.id'))
    rews = db.relationship('Comment', backref = 'lems')
    #img = db.Column(db.String(150))

    def __str__(self):
        return self.place

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(50))
    body = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey('users.id'))
    lem_id = db.Column(db.ForeignKey('lems.id'))

