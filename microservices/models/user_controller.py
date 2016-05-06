from flask import Flask, request, url_for, render_template, flash, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
import simplejson


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_controller.db'
db = SQLAlchemy(app)
context = []

class UserUri(Resource):
    def get(self):
        data = simplejson.loads(request.form['data'])
        print data
        user = User.query.filter_by(username=data.get('username')).all()
        if user:
            if user[0].password == data.get('password'):
                return simplejson.dumps({'status': 'success'})
        else:
            return simplejson.dumps({'status': 'error'})

    def post(self):
        try:
            data = simplejson.loads(request.form['data'])
            print data
            new_user = User(data.get('username'), data.get('email'), data.get('password'))
            db.session.add(new_user)
            db.session.commit()
            return simplejson.dumps({'status': 'success'})
        except:
            db.session.rollback()
            return simplejson.dumps({'status': 'error'})


api.add_resource(UserUri, '/user')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


if __name__=="__main__":
    app.run(port=6000, debug=True)
