import pytest
from main import Teacher, Student

class TestTeacher:
    def setup_method(self):
        self.t = Teacher('Dayo', classroom='Form 2')
    
    def test_teacher_name(self):
        assert self.t.name == 'Dayo'

    def create_quiz(self):
        self.t.create_quiz('Science')

    def add_question(self, question, answers):
        return self.t.add_question(question, answers)

    def test_teacher_create_quiz(self):
        self.create_quiz()
        assert self.t.quiz == {
            'teacher_name': 'Dayo',
            'questions': [],
            'subject': 'Science'
        }

    def test_teacher_add_question(self):
        self.create_quiz()
        quiz = self.t.add_question('How are you?', {'A': 'Good', 'B': 'Not good'})
        assert quiz == {
            'teacher_name': 'Dayo',
            'questions': [
                {
                    '1': 'How are you?',
                    'answers': {
                        'A': 'Good', 'B': 'Not good'
                    }
                }
            ],
            'subject': 'Science'
        }

    def test_add_another_question(self):
        self.create_quiz()
        self.t.add_question('How are you?', {'A': 'Good', 'B': 'Not good'})
        quiz = self.add_question('Are you sure?', {'A': 'Yes', 'B': 'No'})
        assert quiz == {
            'teacher_name': 'Dayo',
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
            'subject': 'Science'
        }

    def test_assign_quiz(self):
        self.create_quiz()
        self.t.add_question('How are you?', {'A': 'Good', 'B': 'Not good'})
        quiz = self.add_question('Are you sure?', {'A': 'Yes', 'B': 'No'})

        s = Student('Aaron', classroom='Form 2')
        s_with_quiz = self.t.assign_quiz(s, quiz)
        assert s.quiz == quiz

    def test_assign_quiz_without_questions(self):
        self.create_quiz()
        s = Student('Aaron', classroom='Form 2')

        with pytest.raises(AttributeError) as excinfo:
            s_with_quiz = self.t.assign_quiz(s, self.t.quiz)
        assert 'Please add questions before assigning quiz.' in str(excinfo.value)