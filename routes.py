from flask import *
from functools import wraps
import sqlite3

DATABASE = 'sales.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = 'the great'

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/welcome')
def welcome():
	return render_template('welcome.html')

def login_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to login first.')
			return redirect(url_for('log'))
	return wrap

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash("You were logged out")
	return redirect (url_for('log'))

@app.route('/hello')
@login_required
def hello():
	g.db = connect_db()
	cur = g.db.execute('select rep_name, amount from reps')
	sales = [dict(rep_name=row[0], amount = row[1]) for row in cur.fetchall()]
	g.db.close()
	return render_template('hello.html', sales=sales)

@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'billu' or request.form['password'] != 'billu123':
			error = 'Invalid Credentials. Please try again.'

		else:
			session['logged_in'] = True
			return redirect(url_for('hello'))
	return render_template('log.html', error=error)

app.debug = True

if __name__ == '__main__':
	app.run()