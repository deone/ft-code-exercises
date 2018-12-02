import pytest
from main import Teacher, Student

class TestTeacher:
    def setup_method(self):
        self.t = Teacher('Dayo', classroom='Form 2')

    def create_quiz(self, subject):
        self.t.create_quiz(subject)

    def add_question(self, subject, question, answers):
        return self.t.add_question(subject, question, answers)

    def test_teacher_details(self):
        assert self.t.name == 'Dayo'
        assert self.t.classroom == 'Form 2'

    def test_create_quiz(self):
        self.create_quiz('Science')
        assert self.t.quizzes == {
            'Science': {
                'questions': []
            }
        }

    def test_create_another_quiz(self):
        self.create_quiz('Science')
        self.create_quiz('Health Education')
        assert self.t.quizzes == {
            'Science': {
                'questions': []
            },
            'Health Education': {
                'questions': []
            }
        }

    def test_add_question_to_first_quiz(self):
        self.create_quiz('Science')
        quiz = self.add_question('Science', 'Day or night?', {'A': 'Day', 'B': 'Night'})
        assert quiz == {
            'questions': [
                {
                    '1': 'Day or night?',
                    'answers': {
                        'A': 'Day', 'B': 'Night'
                    }
                }
            ],
        }

    def test_add_question_to_second_quiz(self):
        self.create_quiz('Health Education')
        quiz = self.add_question('Health Education', 'How are you?', {'A': 'Good', 'B': 'Not good'})
        assert quiz == {
            'questions': [
                {
                    '1': 'How are you?',
                    'answers': {
                        'A': 'Good', 'B': 'Not good'
                    }
                }
            ],
        }

    def test_add_another_question_to_second_quiz(self):
        subject = 'Health Education'
        self.create_quiz(subject)
        self.add_question(subject, 'How are you?', {'A': 'Good', 'B': 'Not good'})
        quiz = self.add_question(subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'})
        assert quiz == {
            'questions': [
                {
                    '1': 'How are you?',
                    'answers': {
                        'A': 'Good', 'B': 'Not good'
                    }
                },
                {
                    '2': 'Are you sure?',
                    'answers': {
                        'A': 'Yes', 'B': 'No'
                    }
                }
            ],
        }

    def test_assign_quiz(self):
        subject = 'Health Education'
        self.create_quiz(subject)
        self.add_question(subject, 'How are you?', {'A': 'Good', 'B': 'Not good'})
        quiz = self.add_question(subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'})

        s = Student('Aaron', classroom='Form 2')
        s_with_quiz = self.t.assign_quiz(s, quiz)
        assert s.quiz == quiz

    def test_assign_quiz_without_questions(self):
        subject = 'Science'
        self.create_quiz(subject)
        s = Student('Aaron', classroom='Form 2')

        with pytest.raises(AttributeError) as excinfo:
            s_with_quiz = self.t.assign_quiz(s, self.t.quizzes[subject])
        assert 'Please add questions before assigning quiz.' in str(excinfo.value)