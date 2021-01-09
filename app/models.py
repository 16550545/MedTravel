from . import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    lastname = db.Column(db.String(64), unique=False)
    lastname_2 = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    procedure = db.Column(db.String(128), unique=False)

    def __repr__(self):
        print("User {} {} {}".format(self.name, self.lastname, self.lastname_2))

