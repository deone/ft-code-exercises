class Person(object):
    def __init__(self, name, classroom):
        self.name = name
        self.classroom = classroom

class Teacher(Person):
    def __init__(self, name, classroom):
        super(Teacher, self).__init__(name, classroom)
        self.quizzes = {}

    def create_quiz(self, subject):
        quiz = {
            'questions': [],
            'answers': []
        }
        self.quizzes[subject] = quiz

    def add_question(self, subject, question, options, answer):
        question_list = self.quizzes[subject]['questions']
        question_count = len(question_list)

        if question_count == 0:
            question_number = 1
        else:
            question_number = question_count + 1

        question_list.append({
            str(question_number): question,
            'options': options
        })
        self.quizzes[subject]['answers'].append(answer)
        return self.quizzes[subject]

    def get_questions(self, subject):
        return self.quizzes[subject]['questions']

    def assign_quiz(self, student, subject):
        questions = self.get_questions(subject)
        if not questions:
            raise AttributeError('Please add questions before assigning quiz.')
        return student.set_quiz(subject, questions)

class Student(Person):
    def set_quiz(self, subject, questions):
        self.quiz = {
            'subject': subject,
            'questions': questions
        }

    def submit_answer(self, answer):
        if answer not in self.quiz['questions']['answers']:
            raise KeyError('Answer provided is not in options.')
        return