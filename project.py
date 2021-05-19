# -*- coding: utf-8 -*-
from datetime import datetime
from flask import Flask, abort, session,jsonify, redirect, render_template, request,send_file,url_for
from flask_msearch import Search
from flask_sqlalchemy import SQLAlchemy
from jieba.analyse.analyzer import ChineseAnalyzer
from werkzeug.exceptions import HTTPException, default_exceptions
from io import BytesIO
import re
from burinYield import BurinYield
import pandas as pd
import numpy as np

def JsonApp(app):
    def error_handling(error):
        if isinstance(error,HTTPException):
            result = { "code":error.code,"description":error.description,"message":str(error)}
        else:
            description = abort.mapping[500].description
            result = {"code": 500, "description":description, "message": str(error)}

        resp = jsonify(result)
        resp.status_code = result["code"]
        return resp

    for code in default_exceptions.keys():
        app.register_error_handler(code,error_handling)

    return app

app = Flask(__name__)
app.secret_key='2313!@#!#$%dkjdsfakfj'
app = JsonApp(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MSEARCH_INDEX_NAME'] = "whoosh_index"
app.config['MSEARCH_PRIMARY_KEY'] = "id"
app.config['MSEARCH_BACKEND'] = 'simple'
app.config['MSEARCH_ENABLE'] = True


db = SQLAlchemy(app)


search = Search(db=db)
search.init_app(app)

titanic_df = pd.read_csv("static/data/train.csv")
survived = titanic_df[(titanic_df['Survived']==1) & (titanic_df["Age"].notnull())]

#BlogPost table
class BlogPost(db.Model):
  __tablename__ = 'blog_post'
  __searchable__ = ['title', 'content','author','filename']  # these fields will be indexed by whoosh
  __analyzer__ = ChineseAnalyzer()   

  id = db.Column(db.Integer, primary_key =True,auto_increment=1)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.Text, nullable=False)
  author = db.Column(db.String(20), nullable=False, default = 'N/A')
  filename = db.Column(db.String(200))
  data = db.Column(db.LargeBinary)
  date_posted = db.Column(db.DateTime, nullable=False, default = datetime.now)

  def __repr__(self):
    return 'Blog post' + str(self.id)

#Accounts table
class Accounts(db.Model):
  __tablename__ = 'accounts'
  __searchable__ = ['fullname', 'username','email']  # these fields will be indexed by whoosh
  __analyzer__ = ChineseAnalyzer()   

  id = db.Column(db.Integer, primary_key =True,nullable=False)
  fullname = db.Column(db.String(200), nullable=True)
  username = db.Column(db.String(50), nullable=True)
  password = db.Column(db.String(255), nullable=True)
  email = db.Column(db.String(100))


  def __repr__(self):
    return 'Accounts:' + str(self.id)


#eol_pass_list table
class EolPassList(db.Model):
  __tablename__ = 'eol_pass_list'
  __searchable__ = ['PPID', 'TestItem']  # these fields will be indexed by whoosh
  __analyzer__ = ChineseAnalyzer()   

  id = db.Column(db.Integer, primary_key =True,nullable=False)
  fullname = db.Column(db.String(200), nullable=True)
  username = db.Column(db.String(50), nullable=True)
  password = db.Column(db.String(255), nullable=True)
  email = db.Column(db.String(100))


  def __repr__(self):
    return 'EolPassList:' + str(self.id)

#eol_pass_list table
class EolFailList(db.Model):
  __tablename__ = 'eol_pass_list'
  __searchable__ = ['PPID', 'TestItem']  # these fields will be indexed by whoosh
  __analyzer__ = ChineseAnalyzer()   

  id = db.Column(db.Integer, primary_key =True,nullable=False)
  fullname = db.Column(db.String(200), nullable=True)
  username = db.Column(db.String(50), nullable=True)
  password = db.Column(db.String(255), nullable=True)
  email = db.Column(db.String(100))


  def __repr__(self):
    return 'EolFailList:' + str(self.id)




def calculate_percentage(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.divide(val, total)
    
    return percent

@app.route('/')
def index():
  return redirect(url_for('login'))


@app.before_request
def require_login():
  allowed_routes = ['login','register']
  if request.endpoint not in allowed_routes and 'username' not in session:
    return redirect('/login')

# http://localhost:3000/login/ - this will be the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
  # Output message if something goes wrong...
  msg = ''
  # Check if "username" and "password" POST requests exist (user submitted form)
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
      # Create variables for easy access
      username = request.form['username']
      password = request.form['password']

      # Check if account exists using filter, Fetch one record and return result
      accounts = Accounts.query.filter(Accounts.username.like("%"+username+"%"), Accounts.password.like("%"+password+"%")).all()   
  
  # If account exists in accounts table in out database
      if accounts:
        for account in accounts:

          # Create session data, we can access this data in other routes
          session['loggedin'] = True
          session['id'] = account.id
          session['username'] = account.username
          # Redirect to home page
          #return 'Logged in successfully!'
          return redirect(url_for('home'))
      else:
        # Account doesnt exist or username/password incorrect
        msg = 'Incorrect username/password!'
  
  return render_template('loginindex.html', msg=msg)

# http://localhost:5000/register - this will be the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
  msg = ''
  # Check if "username", "password" and "email" POST requests exist (user submitted form)
  if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
      # Create variables for easy access
      fullname = request.form['fullname']
      username = request.form['username']
      password = request.form['password']
      email = request.form['email']
      print(email)
  
      #Check if account exists using MySQL
      account = Accounts.query.filter_by(username=username).all()
      # If account exists show error and validation checks
      if account:
          msg = 'Account already exists!'
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
          msg = 'Invalid email address!'
      elif not re.match(r'[A-Za-z0-9]+', username):
          msg = 'Username must contain only characters and numbers!'
      elif not username or not password or not email:
          msg = 'Please fill out the form!'
      else:
          # Account doesnt exists and the form data is valid, now insert new account into accounts table
          new_account = Accounts(username=username, password=password,fullname=fullname,email=email)
          db.session.add(new_account)
          db.session.commit()
          msg = 'You have successfully registered!'
  elif request.method == 'POST':
      # Form is empty... (no POST data)
      msg = 'Please fill out the form!'
  # Show registration form with message (if any)
  return render_template('register.html', msg=msg)
  
# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
  # User is loggedin show them the home page
  return render_template('home.html', username=session['username'])

  
# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))
 
# http://localhost:5000/posts - this will be the profile page, only accessible for loggedin users
@app.route('/posts',methods = ['GET','POST'])
def posts(): 
    # We need all the account info for the user so we can display it on the profile page
    # Show the profile page with account info
    accounts = Accounts.query.msearch(str(session['id']),fields=['id'],limit=20).all()
    for account in accounts:
        page = request.args.get('page',1,type=int)
        if request.method =='POST':
          post_title = request.form['title']
          post_content = request.form['content']
          post_author = request.form['author']
          post_filename = request.form['filename']
          new_post = BlogPost(title=post_title,content=post_content, author = post_author,filename =post_filename)
          db.session.add(new_post)
          db.session.commit()
          return redirect('/posts')
        else:
          all_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page,per_page=6)
          return render_template('postsList.html',posts=all_posts.items,pages=page,pagination = all_posts)

@app.route('/posts/download/<int:id>')
def download(id):
  post = BlogPost.query.filter_by(id=id).first()
  if request.method =='POST':
    post.title = request.form.get('title')
    post.author = request.form.get('author')
    post.content = request.form.get('content')  
    post.filename = request.form.get('filename')
    post.data = request.form.get('data')
    return redirect('/posts')
  else:
    return send_file(BytesIO(post.data),attachment_filename=post.filename , as_attachment=True)

@app.route('/posts/delete/<int:id>')
def delete(id):
  post = BlogPost.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods= ['GET','POST'])
def edit(id):
  post = BlogPost.query.get_or_404(id)
  if request.method =='POST':
    file = request.files['inputFile']
    post.title = request.form.get('title')
    post.author = request.form.get('author')
    post.content = request.form.get('content')  
    post.filename = request.form.get('filename')  
    db.session.delete(post)  #delete the current post
    db.session.commit()
    new_post = BlogPost(id=id,title=post.title,content=post.content, author = post.author,filename=file.filename, data = file.read())
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('edit.html',post=post)

@app.route('/posts/view/<int:id>',methods= ['GET','POST'])
def view(id):
  post = BlogPost.query.get_or_404(id)
  if request.method =='POST':
    post.title = request.form.get('title')
    post.author = request.form.get('author')
    post.content = request.form.get('content')  
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('view.html',post=post)

@app.route('/posts/new',methods= ['GET','POST'])
def new_post():
  if request.method =='POST':
    file = request.files['inputFile']
    post_title = request.form.get('title')
    post_author = request.form.get('author')
    post_content = request.form.get('content') 
    new_post = BlogPost(title=post_title,content=post_content, author = post_author,filename=file.filename, data = file.read())
    db.session.add(new_post)
    db.session.commit()
    return redirect('/posts')
  else:
    return render_template('new_post.html')

@app.route('/search')
def search():
  keyword = request.args.get('query')
  print(keyword)
  results = BlogPost.query.msearch(keyword,fields=['title','content','author','filename'],limit=20).all()
  return render_template('postsList.html',posts=results)

@app.route('/get_piechart_data')
def get_piechart_data():
    class_labels = ['Class I', 'Class II', 'Class III']
    pclass_percent = calculate_percentage(survived.groupby('Pclass').size().values, survived['PassengerId'].count())*100
    pieChartData = []
    for index, item in enumerate(pclass_percent):
        eachData = {}
        eachData['category'] = class_labels[index]
        eachData['measure'] =  round(item,1)
        pieChartData.append(eachData)

    return jsonify(pieChartData)

@app.route('/get_barchart_data')
def get_barchart_data():

    age_labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79']
    survived["age_group"] = pd.cut(survived.Age, range(0, 81, 10), right=False, labels=age_labels)
    survived[['age_group', 'Pclass']]

    survivorFirstClass = survived[survived['Pclass']==1]
    survivorSecondClass = survived[survived['Pclass']==2]
    survivorThirdClass = survived[survived['Pclass']==3]

    survivorAllclassPercent = calculate_percentage(survived.groupby('age_group').size().values,survived['PassengerId'].count())*100
    survivorFirstclassPercent = calculate_percentage(survivorFirstClass.groupby('age_group').size().values,survivorFirstClass['PassengerId'].count())*100
    survivorSecondclassPercent = calculate_percentage(survivorSecondClass.groupby('age_group').size().values,survivorSecondClass['PassengerId'].count())*100
    survivorThirdclassPercent = calculate_percentage(survivorThirdClass.groupby('age_group').size().values,survivorThirdClass['PassengerId'].count())*100

    barChartData = []
    for index, item in enumerate(survivorAllclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "All"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)


    for index, item in enumerate(survivorFirstclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class I"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)

    for index, item in enumerate(survivorSecondclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class II"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)

    for index, item in enumerate(survivorThirdclassPercent):
        eachBarChart = {}
        eachBarChart['group'] = "Class III"
        eachBarChart['category'] = age_labels[index]
        eachBarChart['measure'] = round(item,1)
        barChartData.append(eachBarChart)
    
    return jsonify(barChartData)

@app.route('/charts')
def charts():
  return render_template('charts.html')
  

@app.route('/eolCharts')
def eolCharts():
  post = BlogPost.query.get_or_404(id)
  if request.method =='POST':
    file = request.files['inputFile']

  return render_template('charts.html')



if __name__ == '__main__':
    app.run(debug=True,port=3000,threaded=True)
