from Queue import PriorityQueue

class Student:
    name = ""
    score = 0

    def __init__(self, name , score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score > other.score


q = PriorityQueue()
q.put(Student("A",1))
q.put(Student("C",3))
q.put(Student("B",2))
q.put(Student("0",0))
#
# print q.get().name
# print q.get().name
# print q.get().name
# print q.get().name
# print q.empty()
