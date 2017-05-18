from flask import *

from app import models, db

tasks = Blueprint('tasks', __name__, template_folder='templates')

@tasks.route('/tasks/edit/<int:team_id>', methods=['GET', 'POST'])
def edit_task(team_id):
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
        return render_template('edit_task.html', **options)

    else:
        if not session.get('username'):
            return redirect(url_for('login_api.login'))

        new_task = models.Task(name=request.form['name'],
                               type=request.form['type'],
                               description=request.form['description'],
                               value=request.form['value'],
                               team_id=team_id)
        team = models.Team.query.get(team_id)
        team.tasks.append(new_task)
        db.session.add(team)
        db.session.commit()

        return redirect(url_for('index.home'))
