from flask import Flask, render_template, request,url_for ,make_response, redirect
import os

app = Flask(__name__)

session_storage={}

def generate_session(userid):
    session_id = os.urandom(32).hex()
    session_storage[session_id] = {'userid' : userid, 'cash' : 0}
    return session_id


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':
        session_id = generate_session(request.form.get('userid'))
        user_session_id = f'session_id={session_id}; HttpOnly; path=/;'
        response = make_response(redirect(url_for('cash')))
        response.headers['Set-Cookie'] = user_session_id
        print(session_storage)
        return response

@app.route('/cash', methods=['GET', 'POST'])
def cash():
    if request.method == 'GET':
        session = request.cookies.get('session_id')
        return render_template('cash.html', userid=session_storage[session]['userid'], cash=session_storage[session]['cash'])
    
    if request.method == 'POST':
        session = request.cookies.get('session_id')
        session_storage[session]['cash'] += 10
        print(session_storage)
        return render_template('cash.html', userid=session_storage[session]['userid'], cash=session_storage[session]['cash'])


if __name__ == '__main__':
    app.run(debug=True)
