from flask import Flask, request, url_for, render_template, flash, redirect, session, g
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from requests import post, get
import simplejson


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
context = []

@app.route("/")
def index():
    response = get('http://localhost:7000/message')
    data = simplejson.loads(response.json())
    print data.get('data')
    return render_template('index.html', 
            messages=[{'title':m.get('title'), 'text':m.get('text')} for m in data.get('data')])


@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        response = get('http://localhost:6000/user', data={'data':\
                simplejson.dumps({'username':request.form['username'],\
                     'password':request.form['password']})})
        data = simplejson.loads(response.json())
        if data.get('status') == 'success':
            session['logged_in'] = True
            session['cur_user'] = {'user_id':1}
            return redirect(url_for('index'))
        else:
            error = 'invalid login'
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route("/create_account", methods=['POST', 'GET'])
def create_account():
    error = None
    if request.method == 'POST':
        response = post('http://localhost:6000/user', data={'data':\
                simplejson.dumps({'username':request.form['username'],\
                     'password':request.form['password'],
                     'email':request.form['email']})})
        data = simplejson.loads(response.json())
        if data.get('status') == 'success':
            return redirect(url_for('index'))
    return render_template('create_account.html', error=error)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    session.pop('cur_user', None)
    flash('logged out')
    return redirect(url_for('index'))

@app.route("/admin_init")
def admin():
    db.drop_all()
    db.create_all()
    return "db created"

@app.route("/post_message", methods=['POST', 'GET'])
def post_message():
    error = None
    if request.method == 'POST':
        response = post('http://localhost:7000/message', data={'data':\
                simplejson.dumps({'text':request.form['text'],\
                     'title':request.form['title'],\
                     'user_id':session['cur_user'].get('user_id')})})

        data = simplejson.loads(response.json())
        if data.get('status') == 'success':
            return redirect(url_for('index'))
        else:
            error = data.get('error')
    return render_template('post_message.html', error=error)


app.secret_key='SUPERSECRETKEY'

class MessageUri(Resource):
    def get(self, msg_id):
        res = Message.query.filter_by(id=msg_id).all()
        return {"message": res[0]}

    def post(self):
        try:
            msg = request.form['data']
            blah = Message(msg.get('text'), msg.get('title'), msg.get('user_id'))
            db.session.add(blah)
            db.session.commit()
            flash('New message made')
            return {"status": "success"}
        except:
            db.session.rollback()
            return {"status": "error"}

api.add_resource(MessageUri, '/message/<string:m_id>', '/message')


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
    app.run(port=5555,debug=True)
