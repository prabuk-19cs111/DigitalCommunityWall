from logging import debug
from re import L
from flask import Flask, render_template,request,redirect,url_for,flash,session
from flask_login import login_required
from functools import wraps
from pymongo import MongoClient
from datetime import date
import hashlib
import ast
import json
app = Flask(__name__)
app.secret_key  = "unauthorized0"
session={}
session['log_status']=None
session['event_name']=None

def login_check(uname,pword):
    for i in cred.find():
        if uname == i["username"] and hashlib.sha512(pword.encode()).hexdigest() == i["password"]:
            session['log_status']=True
            session['clubname']=i['clubname']
            return True


def event_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['event_name']==None:
            flash("Please select an event","Error")
            return redirect(url_for('edit'))
        else:
            return f(*args, **kwargs)

    return decorated_function

def login_required(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if session['log_status']:
            return f(*args,**kwargs)
        else:
            flash("please login","Error")
            return redirect(url_for('login'))
    return wrap

@app.route('/')
def home():
   return render_template('index.html',l=col.find())

@app.route('/login',methods=('GET','POST'))
def login():
    keys = ["username","password"]
    d = dict.fromkeys(keys,None)
    if request.method == 'POST':
        d["username"] = request.form.get("uname")
        d["password"] = request.form.get("pword")
        if login_check(d["username"],d["password"]):
           session['username']=d["username"]
           session['password']=d["password"]
           flash("Login Successful","success")
           return redirect(url_for('home'))
        else:
           flash("Login Credentials Doesnot match","Error")
           return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/passwordchange/',methods=('GET','POST'))
@login_required
def changepword():
   if request.method=='POST':
      cu =request.form['curr_pass']
      m1 = request.form['match1']
      m2 = request.form['match2']
      i = cred.find({"username":session['username']})
      for c in i:
             pass
      x=c['password']
      if x==hashlib.sha512(cu.encode()).hexdigest():
            if m1==m2:
                  cred.delete_one({"password":x})
                  c['password']=hashlib.sha512(m1.encode()).hexdigest()
                  cred.insert_one(c)
                  flash("Password changed Successfully","success")
                  return redirect(url_for('home'))
            else:
               flash("Password doesnot match","Error")
               return redirect(url_for('changepword'))
      else:
             flash("Incorrect password","Error")
             return redirect(url_for('changepword'))
   return render_template('passwordchange.html')

   
@app.route('/update/',methods=('GET','POST'))
@login_required
@event_required
def upd():
   v = request.args.get('v')
   y = v.replace("'","\"")
   ul = y.split(",")
   ul.pop(0)
   s = "{"+",".join(ul)
   #s.replace("\'","\"")
   x = json.loads(s)
   en = request.args.get('en')
   dt = str(type(v))
   keys = ["cname","ename","date","desc","time","venue","link"]
   updated_doc  = dict.fromkeys(keys,None)
   if request.method=='POST':
      updated_doc['ename'] = request.form['ename']
      updated_doc['cname'] = request.form['cname']
      updated_doc['desc'] = request.form['desc']
      updated_doc['date'] = request.form['date']
      updated_doc['time'] = request.form['time']
      updated_doc['link'] = request.form['link']
      updated_doc['venue'] = request.form['venue']
      col.delete_one(x)
      col.insert_one(updated_doc)
      return redirect(url_for('home'))
   return render_template('updationpage.html',i=x)

@app.route('/delete/',methods=('GET','POST'))
@login_required
def delete():
   if request.method=='POST':
      del_ename = request.form['del_event']
      if del_ename!="none":
         col.delete_one({"ename":del_ename})
         return redirect(url_for('home'))
      else:
         flash("Select an event to delete","Error")
         return redirect(url_for('delete'))
   return render_template('delete.html',l=col.find({"cname":session['clubname']}))

@app.route('/logout/')
@login_required
def logout():
       session['log_status']=None
       session['username']=None
       session['password']=None
       flash("Logged Out Successfully","success")
       return redirect(url_for('home'))


@app.route('/create/',methods=('GET','POST'))
@login_required
def create():
   today = date.today()
   d = today.strftime("%Y-%m-%d")
   keys = ["cname","ename","date","desc","time","venue","link"]
   inserted_doc  = dict.fromkeys(keys,None)
   if request.method == 'POST':
      inserted_doc['cname'] = request.form['cname']
      inserted_doc['ename'] = request.form['ename']
      inserted_doc['date'] = request.form['date']
      inserted_doc['desc'] = request.form['desc']
      inserted_doc['time'] = request.form['time']
      inserted_doc['venue'] = request.form['venue']
      inserted_doc['link'] = request.form['link']
      col.insert_one(inserted_doc)
      flash("Created Successfully","success")
      return redirect(url_for('home'))
   return render_template('create.html',val=d,cn=session['clubname'])

@app.route('/edit',methods = ('GET','POST'))
@login_required
def edit():
   sel_val = None
   if request.method == 'POST':
         sel_val = request.form['edite']
         if sel_val!="none":
            for l in [x for x in col.find() if x['ename']== sel_val]:
                  pass
            session['event_name']=sel_val
            return redirect(url_for('upd',v=l,en = sel_val))
         else:
            flash("Please Select an Event","Error")
            return redirect(url_for('edit'))
   return render_template("edit.html",v = col.find({"cname":session['clubname']}))    


if __name__ == '__main__':
   client = MongoClient("mongodb://localhost:27017")
   db = client['events']
   col = db['posts']
   cred  = db['users']
   app.run(debug=True)