#!/usr/bin/env python3
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db, models
import os.path
db.create_all()

ARDUINO  = "Arduino"
MODELING = "3D Modeling"
PYTHON   = "Python"


if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))

# create admins
user1 = models.User(username='cgagnon', password='')
user2 = models.User(username='lawteng', password='')
db.session.add(user1)
db.session.add(user2)


# create admin Team
adminTeam = models.Team(name='Los G\'s',
                        grade=16,
                        color='blue',
                        member1='Cameron Gagnon',
                        member2='Lawrence Teng')
db.session.add(adminTeam)

# create generic tasks
generic_tasks = []
# ARDUINO
generic_tasks.append(models.GenericTask(name='Complete and Modify a Circuit',
                               type=ARDUINO,
                               value=2,
                               description='Completed a circuit from the book'))
generic_tasks.append(models.GenericTask(name='Teach Another Student',
                               type=ARDUINO,
                               value=1,
                               description='Taught another student about a circuit'))
generic_tasks.append(models.GenericTask(name='Completely Original Circuit',
                               type=ARDUINO,
                               value=4,
                               description='Completed a custom circuit'))
generic_tasks.append(models.GenericTask(name='Complete Capstone Project',
                               type=ARDUINO,
                               value=10,
                               description='Completed a larger, complex project'))
# PYTHON
generic_tasks.append(models.GenericTask(name='Complete a Lesson in Codecademy',
                               type=PYTHON,
                               value=2,
                               description='Completed a Lesson in Codecademy'))
generic_tasks.append(models.GenericTask(name='Complete a Skills Project',
                               type=PYTHON,
                               value=3,
                               description='Completed a skills lesson'))
generic_tasks.append(models.GenericTask(name='Modify a Skills Project',
                               type=PYTHON,
                               value=1,
                               description='Modified a Skills Lesson'))
generic_tasks.append(models.GenericTask(name='Teach Another Student',
                               type=PYTHON,
                               value=1,
                               description='Taught another student about a Python topic'))
generic_tasks.append(models.GenericTask(name='Write an Original Program in Python',
                               type=PYTHON,
                               value=4,
                               description='Wrote a custom, mostly original program in Python'))
generic_tasks.append(models.GenericTask(name='Complete Capstone Project',
                               type=PYTHON,
                               value=10,
                               description='Completed a larger, complex project'))

# 3D Modeling
generic_tasks.append(models.GenericTask(name='Complete a Skills Project',
                               type=MODELING,
                               value=3,
                               description='Completed a skills lesson in Codecademy'))
generic_tasks.append(models.GenericTask(name='Modify a Skills Project',
                               type=MODELING,
                               value=1,
                               description='Modified a skills project'))
generic_tasks.append(models.GenericTask(name='Teach Another Student',
                               type=MODELING,
                               value=1,
                               description='Taught another student about a 3D Modeling skill or concept'))
generic_tasks.append(models.GenericTask(name='Model your own object in Fusion',
                               type=MODELING,
                               value=4,
                               description='Modeled a custom object in Fusion'))
generic_tasks.append(models.GenericTask(name='Complete Capstone Project',
                               type=MODELING,
                               value=10,
                               description='Completed a larger, complex project'))

for gen_task in generic_tasks:
    db.session.add(gen_task)

db.session.commit()
