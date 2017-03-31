from app.Controller import Controller


class UserView:

    ctrl = None
    nlInput = ""
    def __init__(self):
        self.ctrl = Controller()
        #self.nlInput = raw_input("Enter Natural Language Input:\n")
        self.nlInput = "Return the number of authors who published theory papers before 1980 ."
        self.start()

    def start(self):
        self.ctrl.processNaturalLanguage(self.nlInput)

userView = UserView()
userView.start()