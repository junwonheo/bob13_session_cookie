from flask import Flask, render_template, request, url_for, make_response, redirect, session
from flask_session import Session
import os

app = Flask(__name__)

# Flask-Session configuration
app.config['SECRET_KEY'] = os.urandom(32)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        session['userid'] = request.form.get('userid')
        session['cash'] = 0
        return redirect(url_for('cash'))

@app.route('/cash', methods=['GET', 'POST'])
def cash():
    if 'userid' not in session:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('cash.html', userid=session['userid'], cash=session['cash'])
    
    if request.method == 'POST':
        session['cash'] += 10
        return render_template('cash.html', userid=session['userid'], cash=session['cash'])

if __name__ == '__main__':
    app.run(debug=True)
