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
            'questions': {},
            'answers': {}
        }
        self.quizzes[subject] = quiz

    def add_question(self, subject, question, options, answer):
        questions = self.quizzes[subject]['questions']
        question_count = len(questions.items())

        if question_count == 0:
            question_number = 1
        else:
            question_number = question_count + 1

        questions.update({
            str(question_number): {
                'question': question,
                'options': options
            }
        })

        self.quizzes[subject]['answers'].update({
            str(question_number): answer
        })

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

    def solve_question(self, question_number, answer):
        # Select question
        question = self.quiz['questions']['1']

        if answer not in self.quiz['questions']['answers']:
            raise KeyError('Answer provided is not in options.')
        return