from flask import Flask,request,redirect,render_template,url_for,flash
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import StringField,IntegerField,SubmitField,SelectField,IntegerField,DecimalField
from wtforms.validators import DataRequired
import os
import datetime
from flask_bootstrap import Bootstrap
import sqlite3
import time
import random




app= Flask(__name__)
app.config['SECRET_KEY'] = 'hannah'


@app.route("/",methods=['GET', 'POST'])
def index() :
	return render_template('index.html')
#display matter
@app.route('/matter',methods= ['GET','POST'])
def matter() :
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "SELECT * FROM people2"
	curr.execute(query)
	result = curr.fetchall()
	return render_template('matter.html',result = result)
#add picture
@app.route('/add_image',methods=['POST'])
def add_image():
	file = request.files['addimage']
	file_name = secure_filename(file.filename)
	file.save(os.path.join('./static/' ,file_name))
	first_name=request.form['first_name']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "UPDATE people2 SET Picture = '" + file_name + "' WHERE Name = '" + first_name + "' "
	curr.execute(query)
	conn.commit()
	conn.close()
	return render_template('index.html')
#search picture by fname
@app.route('/user_image',methods=['GET','POST'])
def user_image():
	first_name = request.form['first_name']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "SELECT Picture from people2 where Name = '" + first_name.strip() + "' and Picture IS NOT NULL"
	curr.execute(query)
	image = curr.fetchall()
	if not image or image[0][0] == '':
		return render_template('404.html')
	else:
		return render_template('picture.html', image=image)

#search picture by salary 
@app.route('/salary_image',methods=['GET','POST'])
def salary_image():
	salary = request.form['salary']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "SELECT Picture from people2 where Salary = '" + salary.strip() + "' and Picture IS NOT NULL"
	curr.execute(query)
	image = curr.fetchall()
	print(image)
	if not image or image[0][0] == '':
		return render_template('404.html')
	else:
		return render_template('picture.html', image=image)
#update the keywords
@app.route('/update_keyword',methods=['GET','POST'])
def update_keyword():
	name = request.form['first_name']
	keywords = request.form['keyword']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "UPDATE people2 SET Keywords = '" + keywords + "' WHERE Name = '" + name + "' "
	curr.execute(query)
	conn.commit()
	conn.close()
	return render_template('index.html')
#update the salary

@app.route('/salary_update',methods=['GET','POST'])
def salary_update():
	name = request.form['first_name']
	salary = request.form['updatesalary']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "UPDATE people2 SET Salary = '" + salary + "' WHERE Name = '" + name + "'"
	curr.execute(query)
	conn.commit()
	conn.close()
	return render_template('index.html')
#remove user
@app.route('/remove_user',methods=['POST'])
def remove_user():
	username=request.form['first_name']
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()
	query = "DELETE FROM people2 WHERE Name = '" + username + "'  "
	curr.execute(query)
	conn.commit()
	conn.close()
	return render_template('index.html')
#upload csv
@app.route('/upload_csv',methods=['POST'])
def upload_csv():
	file= request.files['uploadcsv']
	file_contents = file.stream.read().decode("utf-8")
	conn = sqlite3.connect("./hannah.db")
	curr = conn.cursor()


	try:
		curr.execute("DROP TABLE IF EXISTS people2")
	except sqlite3.Error as error:
		print(error)
		return {"error": "some problem with DB"}
	else:
		columns = file_contents.split('\n')[0].split(',')
		stripped_columns = [("%s varchar" % name.strip('\r').strip('\n').lstrip('\ufeff').strip()) for name in columns]
		sql = """create table IF NOT EXISTS people2 (\n""" +",".join(stripped_columns) + ")"
		curr.execute(sql)
		strippedcolumns = [("%s" % name.strip('\r').strip('\n').lstrip('\ufeff').strip()) for name in columns]

		for i in file_contents.split('\n')[1:-1]:
			tuple_  = tuple(k.strip('\r').strip('\n').strip() for k in i.split(','))
			curr.execute("""INSERT INTO people2 (""" + ",".join(strippedcolumns) + """) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", tuple(tuple_))
		conn.commit()
		conn.close()

		return redirect('/')

if __name__=="__main__":
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 3000)),debug=True)