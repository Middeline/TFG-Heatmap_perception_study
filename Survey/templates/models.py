import datetime as dt
from __main__ import db

class AnswersData(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    date        = db.Column(db.String(32))      # '2017-05-10'
    time        = db.Column(db.String(32))      # '08:12:47.292000'
    user        = db.Column(db.Integer)         # User id
    task        = db.Column(db.String(255))     # Task being performed
    age         = db.Column(db.Integer)         # Age
    gender      = db.Column(db.String(255))     # Gender
    education   = db.Column(db.String(255))     # Education level
    eyesight    = db.Column(db.String(255))     # Eyesight
    display     = db.Column(db.String(32))      # Inches of the display
    understood  = db.Column(db.String(32))      # Understanding
    easiness    = db.Column(db.String(32))      # Easiness of the tasks
    satisfied   = db.Column(db.String(32))      # Satisfaction on the time spent
    comments    = db.Column(db.String(1000))    # Additional comments
    chart       = db.Column(db.String(255))     # Image shown
    bar_A       = db.Column(db.Integer)         # Value bar A
    answer_A    = db.Column(db.Integer)         # Answer A
    bar_B       = db.Column(db.Integer)         # Value bar B
    answer_B    = db.Column(db.Integer)         # Answer B
    error_A     = db.Column(db.Integer)         # Error A
    error_B     = db.Column(db.Integer)         # Error B
    abs_error_A = db.Column(db.Integer)         # Absolute error A
    abs_error_B = db.Column(db.Integer)         # Absolute error B
    time_spent  = db.Column(db.String(32))      # Time spent to answer
    prolific_code  = db.Column(db.String(32))       # Prolific's  code
