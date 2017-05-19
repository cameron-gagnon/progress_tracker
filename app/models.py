from app import db

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    tasks = db.relationship('Task')
    grade = db.Column(db.String(5))
    color = db.Column(db.String(20))
    member1 = db.Column(db.Text)
    member2 = db.Column(db.Text)
    member3 = db.Column(db.Text)
    member4 = db.Column(db.Text)

    def __repr__(self):
        return 'Team: {}.\n\tGrade: {}\n\tTasks: {}\n\tMembers: {}, {}, {}, {}\n\tColors: {}'.format(
                self.name, self.grade, self.tasks, self.member1,
                self.member2, self.member3, self.member4, self.color)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    resolved = db.Column(db.Boolean, default=False, nullable=False)
    value = db.Column(db.Integer)
    description = db.Column(db.Text)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    def __repr__(self):
        return 'Task name: {}.\n\tType: {}\n\tDescription: {}\n\tValue: {}\n\tResolved: {}'.format(
                self.name, self.type, self.description, self.value, self.resolved)


class GenericTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    type = db.Column(db.String(80))
    value = db.Column(db.Integer)
    description = db.Column(db.Text)

    def __repr__(self):
        return 'Task name: {}.\n\tType: {}\n\tDescription: {}'.format(
                self.name, self.type, self.description)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __repr__(self):
        return 'Username: {}.\n\tPassword: {}'.format(
                self.username, self.password)
