from flask import *

from app import models, db, helpers
from collections import defaultdict, namedtuple

tasks = Blueprint('tasks', __name__, template_folder='templates')

@tasks.route('/tasks/submit/<int:team_id>', methods=['GET', 'POST'])
def submit_task(team_id):
    """
        Update a task for a team
    """
    if request.method == 'GET':
        task_id = request.args.get('task_id')
        task = models.GenericTask.query.get(task_id)
        team = models.Team.query.get(team_id)
        options = {
            'task': task,
            'team': team,
            'arduinoChecked': "Checked" if task.type == 'Arduino' else '',
            'pythonChecked': "Checked" if task.type == 'Python' else '',
            'modelChecked': "Checked" if task.type == '3D Modeling' else '',
        }
        return render_template('submit_task.html', **options)

    else:
        new_task = models.Task(name=request.form['name'],
                               type=request.form['type'],
                               description=request.form['description'],
                               value=request.form['value'],
                               team_id=team_id)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for('index.home'))

@tasks.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
def task_edit(task_id):

    if not session.get('username'):
        return redirect(url_for('index.home'))

    if request.method == 'GET':
        task_id = request.args.get('task_id')
        task = models.Task.query.get(task_id)
        team = models.Team.query.get(task.team_id)
        options = {
            'task': task,
            'team': team,
            'arduinoChecked': "Checked" if task.type == 'Arduino' else '',
            'pythonChecked': "Checked" if task.type == 'Python' else '',
            'modelChecked': "Checked" if task.type == '3D Modeling' else '',
        }
        return render_template('edit_task.html', **options)

    else:
        task = models.Task.query.get(task_id)

        task.name = request.form['name']
        task.type = request.form['type']
        task.description = request.form['description']
        task.value = request.form['value']
        task.resolved = True

        db.session.add(task)
        db.session.commit()

        return redirect(url_for('tasks.tasks_pending'))



@tasks.route('/tasks/pending', methods=['GET', 'POST'])
def tasks_pending():
    if not session.get('username'):
        return redirect(url_for('index.home'))

    if request.method == 'GET':
        # TODO: order by oldest to newest
        pendingTasks = models.Task.query.filter(models.Task.resolved == False).all()
        TeamTaskPairs = namedtuple('TeamTaskPairs', ['team', 'tasks'])
        teamTasks = defaultdict(list)

        for task in pendingTasks:
            team = models.Team.query.get(task.team_id)
            teamTasks[team].append(task)

        options = {
            'pendingTeamTasks': teamTasks,
            'colorMap': helpers.colorMap,
        }

        return render_template('tasks_pending.html', **options)

    else:
        task_id = request.form.get('task_id')

        task = models.Task.query.get(task_id)
        task.resolved = True
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('tasks.tasks_pending'))



@tasks.route('/tasks/delete/<int:task_id>', methods=['GET'])
def task_delete(task_id):
    if not session.get('username'):
        return redirect(url_for('index.home'))

    models.Task.query.filter(models.Task.id == task_id).delete()
    db.session.commit()

    return redirect(url_for('tasks.tasks_pending'))
