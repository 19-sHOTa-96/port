#My modules
from contact import Contactor


#Flask imports
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, flash, abort
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_login import UserMixin, LoginManager, current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from flask_migrate import Migrate
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASEURI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False




#adnresmobtana@gmail.com
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MY_EMAIL")
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.String(80), unique=True, nullable=False)
	user_email = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), unique=True, nullable=False)


#Own Objects
sender = Contactor()



def admin(func):
	@wraps(func)
	def wrapper():
		if not current_user.is_authenticated:
			flash('Log In Required')
			return redirect(url_for('home'))
		return func()
	return wrapper



@app.route('/')
def home():
	return render_template('home.html')



@app.route('/about')
def about():
	return render_template('about.html')



@app.route('/registration', methods=['POST', 'GET'])
def registration():

	if request.method == 'POST':
		name, email, password = request.form['first_name'], request.form['email'], generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=8)
		if name and email and password:
			new_user = Users(user_name=name, user_email=email, password=password)
			db.session.add(new_user)
			db.session.commit()

	return render_template('registration.html')



@app.route('/login', methods=['POST', 'GET'])
def login():

	if request.method == 'POST':
		user = Users.query.filter_by(user_name=request.form['first_name']).first()
		
		if user:
			if user.user_email == request.form['email']:
				print(user.user_email)
				if check_password_hash(user.password, request.form['password']):
					login_user(user)
					return redirect(url_for('home'))
				elif not check_password_hash(user.password, request.form['password']):
					flash("Incorrect Password! try again.")
			elif not user.user_email == request.form['email']:
				flash("Incorrect Mail! try again.")	
		elif not user:
			flash("Incorrect User Name! try again.")
		else:
			flash("Incorrect Credentials! try again.")

	return render_template('login.html')



@app.route('/logout')
# @login_required
@admin
def logout():
	logout_user()
	return redirect(url_for('home'))


# ------------------------------------------------------------------------------------------------------------- #

@app.route('/contact-email', methods=['POST', 'GET'])
# @login_required
@admin
def contact_email():

	if request.method == 'POST':
		name, email, msg = request.form['name'], request.form['email'], request.form['text']
		sender.send_email(name, email, msg)
		# print(name, email, msg)			

	return render_template('contact-email.html')


@app.route('/contact-sms', methods=['POST', 'GET'])
@admin
def contact_sms():

	if request.method == 'POST':
		name, phone, text = request.form['name'], request.form['phone'], request.form['text']
		sender.send_sms(name, phone, text)
		# print(name, phone, text)

	return render_template('contact-sms.html')		

# ------------------------------------------------------------------------------------------------------------- #


@app.route('/download')
# @login_required
@admin
def download():
	return render_template('download.html')


@app.route('/download-app-1')
def download_app_1():
	return send_from_directory('static', path="static/files/App.txt", filename="files/App.txt", as_attachment=True)



@app.route('/download-cv')
def download_cv():
	return send_from_directory('static', path="static/files/CV.txt", filename="files/CV.txt", as_attachment=True)






if __name__ == "__main__":
	app.run(debug=True)    
