class Email:
    def __init__(self, activityid, description, regardingobjectid, createdon):
        self.activityid = activityid
        self.content = description
        self.caseid = regardingobjectid
        self.createdon = createdon