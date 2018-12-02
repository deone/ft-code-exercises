import itertools
from collections import OrderedDict

class InvalidAction(Exception):
    pass

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

    def assign_quiz(self, student, subject, questions):
        if not questions:
            raise InvalidAction('Please add questions before assigning quiz.')
        return student.set_quiz(subject, questions)

    def grade_quiz(self, quiz):
        # Only grade quiz if submitted
        score = 0
        grade_book = {}

        completed = quiz.get('completed', None)

        if completed:
            # Compare teacher's answers to student's answers
            subject = quiz['subject']
            student_name = quiz['name']
            students_answers = OrderedDict(quiz['answers'])
            score_per_question = 100 / len(quiz['questions'].keys())
            teachers_answers = OrderedDict(self.quizzes[subject]['answers'])
            for teacher_answer, student_answer in itertools.izip(teachers_answers, students_answers):
                if teacher_answer == student_answer:
                    score += score_per_question

            grade_book[student_name] = score
            return grade_book
        else:
            raise InvalidAction('You cannot grade an incomplete quiz.')

class Student(Person):
    def set_quiz(self, subject, questions):
        self.quiz = {
            'name': self.name,
            'subject': subject,
            'questions': questions
        }

    def solve_question(self, question_number, answer):
        # Select question
        question = self.quiz['questions'][str(question_number)]
        options = question['options']

        if answer not in options:
            raise InvalidAction('Answer provided is not in options.')

        answers = self.quiz.get('answers', None)
        if answers is None:
            self.quiz['answers'] = {str(question_number): answer}
        else:
            answers[str(question_number)] = answer

        return self.quiz

    def submit_quiz(self, quiz):
        # Only submit quiz if all questions have been answered
        if len(quiz['questions']) == len(quiz['answers']):
            quiz['completed'] = True
            return quiz
        else:
            raise InvalidAction('You can only submit quiz after answering all questions.')