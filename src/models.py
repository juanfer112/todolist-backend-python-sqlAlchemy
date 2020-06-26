from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


engine = create_engine('mysql://root@localhost:3306/example')

class Todo(db.Model):
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(250), unique=True, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return '<Todo %r>' % self.label

    def serialize(self):
        return {
            "id": self.id,
            "label": self.label,
            "done": self.done
        }