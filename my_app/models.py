from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from .extensions import db
from enum import Enum as PyEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(64), nullable=True)
    last_challenge_id = db.Column(
        db.String(36), db.ForeignKey("phishing_challenges.id"), nullable=True
    )
    current_challenge_id = db.Column(
        db.String(36), ForeignKey("phishing_challenges.id")
    )
    current_challenge = db.relationship(
        "PhishingChallenge", foreign_keys=[current_challenge_id]
    )
    phishing_responses = db.relationship('PhishingResponse', backref='user')
    
    has_completed_simulation = db.Column(db.Boolean, default=False)
    
    password_hash = db.Column(db.String(128))
    
    overall_score = db.Column(db.Integer)  # Overall score of the user
    grade_level = db.Column(db.String(50))  # Grade level of the user
    
    def __init__(self, username, password, gender=None):
        self.username = username
        self.password = password
        self.gender = gender

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



class PreSimulationResponse(db.Model):
    __tablename__ = "pre_simulation_responses"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    age = db.Column(db.Integer, nullable=False, default=0)
    gender = db.Column(db.String(64), nullable=False)
    training = db.Column(db.String(64), nullable=False)
    knowledge = db.Column(db.String(64), nullable=False)
    message = db.Column(db.String(64), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    actions = db.Column(db.String(64), nullable=False)
    consequences = db.Column(db.String(64), nullable=False)


class PhishingEnum(PyEnum):
    GENUINE = "genuine"
    PHISHING = "phishing"
    UNSURE = "unsure"


class PhishingResponse(db.Model):
    __tablename__ = "phishing_responses"
    

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    challenge_id = db.Column(
        db.String(36),
        db.ForeignKey("phishing_challenges.id"),
        nullable=False,
        index=True,
    )
    duration = db.Column(db.Integer, nullable=False)
    challenge_number = db.Column(db.Integer, nullable=False)
    clicked_link = db.Column(db.Boolean, nullable=False)
    phishing = db.Column(
        db.Enum(PhishingEnum.GENUINE.value, PhishingEnum.PHISHING.value, PhishingEnum.UNSURE.value), nullable=False
    )
    confidence = db.Column(db.String(255), nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=False, default=0)
    gender = db.Column(db.String(64), nullable=False)
    pre_simulation_id = db.Column(db.String(36), db.ForeignKey('pre_simulation_responses.id'))
    
    
    # Relationships
    
    challenge = db.relationship("PhishingChallenge", backref="phishing_challenge")
    pre_simulation = db.relationship("PreSimulationResponse",
                                  primaryjoin="PhishingResponse.pre_simulation_id==PreSimulationResponse.id",
                                  backref="phishing")


class PostSimulationResponse(db.Model):
    __tablename__ = "post_simulation_responses"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    awareness = db.Column(db.String(64), nullable=False)
    ratings = db.Column(db.Integer, nullable=False)
    helpful = db.Column(db.String(64), nullable=False)
    act = db.Column(db.String(64), nullable=False)
    behaviour = db.Column(db.String(64), nullable=False)
    effective = db.Column(db.String(64), nullable=False)
    life = db.Column(db.String(64), nullable=False)
    recommend = db.Column(db.String(64), nullable=True)


class PhishingChallenge(db.Model):
    __tablename__ = "phishing_challenges"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    subject = db.Column(db.String(512), nullable=True)
    sender = db.Column(db.String(512), nullable=True)
    content = db.Column(db.Text, nullable=False)
    is_phishing = db.Column(db.Enum("genuine", "phishing", "unsure"), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

class UserProgressLog(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # to know when this log was created
    user_score = db.Column(db.Integer)  # Assuming score is an integer after rounding
    grade_level = db.Column(db.String(50))  # String column to store grade