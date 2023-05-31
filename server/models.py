from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime 
from sqlalchemy.sql import func


convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    campers = db.relationship('Camper', backref='activity')

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))

    @validates('camper')
    def validate_camper(self, age, name):
        if name and age >= 8 and age <= 18:
            return name 
        else:
            raise ValueError('age must be between 8 - 18 and name must exist')
        
        

    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'
    
class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    camper_id = db.Column(db.Integer, unique=True)
    activity_id = db.Column(db.Integer) 
    time = db.Column(db.Integer) 
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now()) 

    activities = db.relationship('Activity', foreign_keys=[Activity.id],
                                 backref=db.backref('activity', lazy='joined'), lazy='dynamic')
    
    campers = db.relationship('Camper', foreign_keys=[Camper.id], 
                              backref=db.backref('followed', lazy='joined'), lazy='dynamic')
    
    @validates('signup')
    def validate_signup(self, time, name):
        if time > 0 and time <= 23:
            return name 
        
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need. 