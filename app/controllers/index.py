from flask import *

from app import models

index = Blueprint('index', __name__, template_folder='templates')

@index.route('/')
def home():
    teams = models.Team.query.all()
    tasks = models.Task.query.all()
    options = {
        'teams': teams,
        'tasks': tasks,
    }
    return render_template('index.html', **options)
