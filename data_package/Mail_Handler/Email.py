class Email:
    def __init__(self, activityid, description, regardingobjectid, createdon):
        """
        :param activityid:
        :param description:
        :param regardingobjectid:
        :param createdon:
        """
        self.activityid = activityid
        self.content = description
        self.caseid = regardingobjectid
        self.createdon = createdon