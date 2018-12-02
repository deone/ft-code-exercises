import pytest
from main import Teacher, Student

class TestTeacher:
    def setup_method(self):
        self.teacher = Teacher('Dayo', classroom='Form 2')

    def create_quiz(self, subject):
        self.teacher.create_quiz(subject)

    def create_quiz_with_questions(self):
        subject = 'Health Education'
        self.create_quiz(subject)
        return self.add_question(subject, 'How are you?', {'A': 'Good', 'B': 'Not good'}, 'B')

    def add_question(self, subject, question, options, answer):
        return self.teacher.add_question(subject, question, options, answer)

    def test_teacher_details(self):
        assert self.teacher.name == 'Dayo'
        assert self.teacher.classroom == 'Form 2'

    def test_create_quiz(self):
        self.create_quiz('Science')
        assert self.teacher.quizzes == {
            'Science': {
                'questions': [],
                'answers': []
            }
        }

    def test_create_another_quiz(self):
        self.create_quiz('Science')
        self.create_quiz('Health Education')
        assert self.teacher.quizzes == {
            'Science': {
                'questions': [],
                'answers': []
            },
            'Health Education': {
                'questions': [],
                'answers': []
            }
        }

    def test_add_question_to_first_quiz(self):
        self.create_quiz('Science')
        quiz = self.add_question('Science', 'Day or night?', {'A': 'Day', 'B': 'Night'}, 'A')
        assert quiz == {
            'questions': [
                {
                    '1': 'Day or night?',
                    'options': {
                        'A': 'Day', 'B': 'Night'
                    }
                }
            ],
            'answers': ['A']
        }

    def test_add_question_to_second_quiz(self):
        quiz = self.create_quiz_with_questions()
        assert quiz == {
            'questions': [
                {
                    '1': 'How are you?',
                    'options': {
                        'A': 'Good', 'B': 'Not good'
                    }
                }
            ],
            'answers': ['B']
        }

    def test_add_another_question_to_second_quiz(self):
        subject = 'Health Education'
        self.create_quiz_with_questions()
        quiz = self.add_question(subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'}, 'B')
        assert quiz == {
            'questions': [
                {
                    '1': 'How are you?',
                    'options': {
                        'A': 'Good', 'B': 'Not good'
                    }
                },
                {
                    '2': 'Are you sure?',
                    'options': {
                        'A': 'Yes', 'B': 'No'
                    }
                }
            ],
            'answers': ['B', 'B']
        }

    def test_get_questions(self):
        self.create_quiz_with_questions()
        assert self.teacher.get_questions('Health Education') == [{
                '1': 'How are you?',
                'options': {
                    'A': 'Good', 'B': 'Not good'
                }
            }
        ]

    def test_assign_quiz_without_questions(self):
        subject = 'Science'
        self.create_quiz(subject)
        student = Student('Aaron', classroom='Form 2')

        with pytest.raises(AttributeError) as excinfo:
            student_with_quiz = self.teacher.assign_quiz(student, subject)
        assert 'Please add questions before assigning quiz.' in str(excinfo.value)

    def test_assign_quiz(self):
        student = Student('Aaron', classroom='Form 2')
        subject = 'Health Education'
        quiz = self.create_quiz_with_questions()

        student_with_quiz = self.teacher.assign_quiz(student, subject)

        assert student.quiz == {
            'subject': 'Health Education',
            'questions': [{'1': 'How are you?', 'options': {'A': 'Good', 'B': 'Not good'}}]
        }