class Person:
    def __init__(self, name):
        self.name = name
        self.quiz = {}

class Teacher(Person):
    def create_quiz(self, subject):
        self.quiz.update({
            'teacher_name': self.name,
            'subject': subject,
            'questions': []
        })

    def add_question(self, question, answers):
        question_list = self.quiz['questions']
        question_count = len(question_list)

        if question_count == 0:
            question_number = 1
        else:
            question_number = question_count + 1

        question_list.append({
            str(question_number): question,
            'answers': answers
        })
        return self.quiz

    def assign_quiz(self, student, quiz):
        if not quiz['questions']:
            raise AttributeError('Please add questions before assigning quiz.')
        return student.set_quiz(quiz)

class Student(Person):
    def set_quiz(self, quiz):
        self.quiz.update(quiz)

    def submit_answer(self, answer):
        if answer not in self.quiz['questions']['answers']:
            raise KeyError('Answer provided is not in options.')
        return