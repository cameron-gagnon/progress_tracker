from flask import *

from app import models, db

login_api = Blueprint('login_api', __name__, template_folder='templates')


@login_api.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('username'):
            return redirect(url_for('index.home'))
        else:
            return render_template('login.html')
    else:
        username = request.form['username']
        password = request.form['password']

        res = models.User.query.filter(models.User.username == username).first()
        if not res:
            return redirect(url_for('login_api.login'))
        else:
            session['username'] = escape(username)
            return redirect(url_for('index.home'))

@login_api.route('/logout', methods=['GET'])
def logout():
    if session.get('username'):
        session.pop('username', None)

    return redirect(url_for('index.home'))


