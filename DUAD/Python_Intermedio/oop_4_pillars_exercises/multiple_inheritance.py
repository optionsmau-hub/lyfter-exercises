class Walker:
    def walk(self):
        return "I can walk."


class Speaker:
    def speak(self):
        return "I can speak."


class RobotAssistant(Walker, Speaker):
    def assist(self):
        return "I can assist humans."