from flask import *
from app import models, db, helpers
from collections import namedtuple

teams = Blueprint('teams', __name__, template_folder='templates')


@teams.route('/teams/create', methods=['GET', 'POST'])
def create_route():
    """
        Create a team
    """
    if request.method == 'GET':
        options = {
            'colors': helpers.colors,
            'grades': helpers.grades,
        }
        return render_template('create_team.html', **options)

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
        return redirect(url_for('index.home'))

@teams.route('/teams/edit/<int:team_id>', methods=['GET', 'POST'])
def edit_team_info(team_id):
    if not session.get('username'):
        return redirect(url_for('login_api.login'))

    team = models.Team.query.get(team_id)
    team.member1 = '' if not team.member1 else team.member1
    team.member2 = '' if not team.member2 else team.member2
    team.member3 = '' if not team.member3 else team.member3
    team.member4 = '' if not team.member4 else team.member4

    if request.method == 'GET':

        options = {
            'team': team,
            'colors': helpers.colors,
            'grades': helpers.grades,
            'selectedColor': team.color,
            'selectedGrade': team.grade,
        }

        return render_template('edit_team_info.html', **options)

    else:

        team.name = request.form['name']
        team.member1 = request.form['member1']
        team.member2 = request.form['member2']
        team.member3 = request.form['member3']
        team.member4 = request.form['member4']
        team.grade = request.form['grade']
        team.color = request.form['color']

        db.session.add(team)
        db.session.commit()
        return redirect(url_for('index.home'))

@teams.route('/teams/delete/<int:team_id>', methods=['GET'])
def delete_team(team_id):
    if not session.get('username'):
        return redirect(url_for('index.home'))

    models.Team.query.filter(models.Team.id == team_id).delete()
    db.session.commit()

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

    TechInfo = namedtuple('TechInfo', ['type', 'tasks', 'color'])
    techTuples = [TechInfo("Arduino", arduinoTasks, "blue"),
                  TechInfo("3D Modeling", modelingTasks, "red"),
                  TechInfo("Python", pythonTasks, "yellow")]

    options = {
        'techTuples': techTuples,
        'team': team,
    }
    return render_template('finish_task.html', **options)

@teams.route('/teams/overview/<int:team_id>', methods=['GET'])
def team_overview(team_id):
    team = models.Team.query.get(team_id)

    arduinoTasks = models.Task.query.filter(models.Task.type == 'Arduino').filter(models.Task.resolved == True).all()
    modelingTasks = models.Task.query.filter(models.Task.type == '3D Modeling').filter(models.Task.resolved == True).all()
    pythonTasks = models.Task.query.filter(models.Task.type == 'Python').filter(models.Task.resolved == True).all()

    TechInfo = namedtuple('TechInfo', ['type', 'tasks', 'color'])
    techTuples = [TechInfo("Arduino", arduinoTasks, "blue"),
                  TechInfo("3D Modeling", modelingTasks, "red"),
                  TechInfo("Python", pythonTasks, "yellow")]

    options = {
        'techTuples': techTuples,
        'team': team,
    }

    return render_template('team_overview.html', **options)
