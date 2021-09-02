from app import db
import datetime

class Message(db.Model):    
    
    __tablename__ = 'messages'
    id = db.Column(db.Integer,primary_key=True,nullable=False)
    time = db.Column(db.DateTime,default = datetime.datetime.utcnow)
    text= db.Column(db.VARCHAR(length=255),nullable=False)
    
    def __init__(self,text,time):
        self.text = text
        self.time = time
    
    def __repr__(self):
        return f'Text: {self.text} time: {self.time}'

    