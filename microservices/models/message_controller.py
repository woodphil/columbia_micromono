from flask import Flask, request, url_for, render_template, flash, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse
import simplejson


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_controller.db'
db = SQLAlchemy(app)
context = []

class MessageUri(Resource):
    def get(self):
        msgs = Message.query.all()
        return simplejson.dumps({'status': 'success', 
            'data':[{'title': m.title, 'text': m.text} for m in msgs]})

    def post(self):
        try:
            data = simplejson.loads(request.form['data'])
            blah = Message(data.get('text'), data.get('title'), data.get('user_id'))
            db.session.add(blah)
            db.session.commit()
            return simplejson.dumps({"status": "success"})
        except Exception as e:
            print e
            db.session.rollback()
            return simplejson.dumps({"status": "error", "error": "ERRORLOL"})

api.add_resource(MessageUri, '/message')
app.secret_key='MESSAGERSECRETKEY'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    title = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, text, title, user_id):
        self.text = text
        self.title = title
        self.user_id = user_id

if __name__=="__main__":
    app.run(port=7000, debug=True)
