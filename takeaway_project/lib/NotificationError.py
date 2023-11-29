class NotificationError(Exception):
    def __init__(self, message="Notification Failed"):
        self.message = message
        self.status = 'FAIL'
        super().__init__(self.message)