from taskr import db
from taskr.models import FTasks
from datetime import date

db.create_all()

db.session.add(FTasks("Finish this ", date(2013, 12, 21), 10, 1))
db.session.add(FTasks("Finish that ", date(2013, 12, 22), 10, 1))

db.session.commit()
