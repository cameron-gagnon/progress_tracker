from flask import *
from app import models, db

teams = Blueprint('teams', __name__, template_folder='templates')


@teams.route('/teams/create', methods=['GET', 'POST'])
def create_route():
    """
        Create a team
    """
    if request.method == 'GET':
        return render_template('create_team.html')
    else:
        team = models.Team(name=request.form['name'],
                           grade=request.form['grade'],
                           color=request.form['color'],
                           member1=request.form['member1'],
                           member2=request.form['member2'],
                           member3=request.form['member3'],
                           member4=request.form['member4'])
        db.session.add(team)
        db.session.commit()
        print(team)
        return redirect(url_for('index.home'))

@teams.route('/teams/finish', methods=['GET'])
def select_finish_route():
    """
        If no team_id is sent to the /teams/finish route, then we force
        the user to pick the team
    """
    teams = models.Team.query.all()
    options = {
        'teams': teams,
    }
    return render_template('select_team.html', **options)

@teams.route('/teams/finish/<int:team_id>', methods=['GET'])
def finish_route(team_id):
    """
        Displays a list of the generic tasks
    """

    if request.method != 'GET':
        return redirect(url_for('index.home'))

    team = models.Team.query.get(team_id)

    arduinoTasks = models.GenericTask.query.filter(models.GenericTask.type == 'Arduino').all()
    modelingTasks = models.GenericTask.query.filter(models.GenericTask.type == '3D Modeling').all()
    pythonTasks = models.GenericTask.query.filter(models.GenericTask.type == 'Python').all()

    options = {
        'arduinoTasks': arduinoTasks,
        'modelingTasks': modelingTasks,
        'pythonTasks': pythonTasks,
        'team': team,
    }
    return render_template('finish_task.html', **options)

@teams.route('/teams/overview/<int:team_id>', methods=['GET'])
def team_overview(team_id):
    team = models.Team.query.get(team_id)
    arduinoTasks = models.Task.query.filter(models.Task.type == 'Arduino').all()
    modelingTasks = models.Task.query.filter(models.Task.type == '3D Modeling').all()
    pythonTasks = models.Task.query.filter(models.Task.type == 'Python').all()

    options = {
        'team': team,
        'arduinoTasks': arduinoTasks,
        'modelingTasks': modelingTasks,
        'pythonTasks': pythonTasks,
    }

    return render_template('team_overview.html', **options)
