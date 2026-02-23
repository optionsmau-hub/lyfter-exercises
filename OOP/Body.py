class Head:
    def __init__(self):
        self.eyes = 2


class Hand:
    def __init__(self):
        self.fingers = 5


class Feet:
    def __init__(self):
        self.toes = 5


class Arm:
    def __init__(self, hand):
        self.hand = hand


class Leg:
    def __init__(self, feet):
        self.feet = feet


class Torso:
    def __init__(self, head, right_arm, left_arm):
        self.head = head
        self.right_arm = right_arm
        self.left_arm = left_arm


class Human:
    def __init__(self):
        head = Head()

        right_hand = Hand()
        left_hand = Hand()

        right_arm = Arm(right_hand)
        left_arm = Arm(left_hand)

        right_leg = Leg(Feet())
        left_leg = Leg(Feet())

        self.torso = Torso(head, right_arm, left_arm)
        self.right_leg = right_leg
        self.left_leg = left_leg


if __name__ == "__main__":
    human = Human()

    print("Eyes:", human.torso.head.eyes)
    print("Right hand fingers:", human.torso.right_arm.hand.fingers)
    print("Left foot toes:", human.left_leg.feet.toes)