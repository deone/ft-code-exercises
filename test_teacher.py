import pytest

from main import Teacher, Student, InvalidAction

class TestTeacher:
    def setup_method(self):
        self.teacher = Teacher('Dayo Osikoya', 'Form 2')
        self.student = Student('Aaron Buddy', classroom='Form 2')

    def create_quiz(self, subject):
        self.teacher.create_quiz(subject)

    def create_quiz_with_questions(self, subject):
        subject = 'Health Education'
        self.create_quiz(subject)
        self.add_question(subject, 'How are you?', {'A': 'Good', 'B': 'Not good'}, 'B')
        self.add_question(subject, 'Cold or Fever?', {'A': 'Cold', 'B': 'Fever'}, 'B')
        return self.add_question(subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'}, 'B')

    def add_question(self, subject, question, options, answer):
        return self.teacher.add_question(subject, question, options, answer)

    def test_teacher_details(self):
        assert self.teacher.name == 'Dayo Osikoya'
        assert self.teacher.classroom == 'Form 2'

    def test_create_quiz(self):
        self.create_quiz('Science')
        assert self.teacher.quizzes == {
            'Science': {
                'questions': {},
                'answers': {}
            }
        }

    def test_create_another_quiz(self):
        self.create_quiz('Science')
        self.create_quiz('Health Education')
        assert self.teacher.quizzes == {
            'Science': {
                'questions': {},
                'answers': {}
            },
            'Health Education': {
                'questions': {},
                'answers': {}
            }
        }

    def test_add_question_to_first_quiz(self):
        self.create_quiz('Science')
        quiz = self.add_question('Science', 'Day or night?', {'A': 'Day', 'B': 'Night'}, 'A')
        assert quiz == {
            'answers': {'1': 'A'},
            'questions': {
                '1': {'question': 'Day or night?', 'options': {'A': 'Day', 'B': 'Night'}}
            }
            
        }

    def test_add_question_to_second_quiz(self):
        subject = 'Health Education'
        quiz = self.create_quiz_with_questions(subject)
        assert quiz == {
            'answers': {'1': 'B', '3': 'B', '2': 'B'},
            'questions': {
                '1': {
                    'question': 'How are you?',
                    'options': {'A': 'Good', 'B': 'Not good'}
                },
                '3': {
                    'question': 'Are you sure?',
                    'options': {'A': 'Yes', 'B': 'No'}
                },
                '2': {
                    'question': 'Cold or Fever?',
                    'options': {'A': 'Cold', 'B': 'Fever'}
                }
            }
        }

    def test_add_another_question_to_second_quiz(self):
        subject = 'Health Education'
        self.create_quiz_with_questions(subject)
        quiz = self.add_question(
            subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'}, 'B')
        assert quiz == {
            'answers': {'1': 'B', '3': 'B', '2': 'B', '4': 'B'},
            'questions': {
                '1': {
                    'question': 'How are you?',
                    'options': {'A': 'Good', 'B': 'Not good'}
                },
                '3': {
                    'question': 'Are you sure?',
                    'options': {'A': 'Yes', 'B': 'No'}
                },
                '2': {
                    'question': 'Cold or Fever?',
                    'options': {'A': 'Cold', 'B': 'Fever'}
                },
                '4': {
                    'question': 'Are you sure?',
                    'options': {'A': 'Yes', 'B': 'No'}
                }
            }
        }

    def test_get_questions(self):
        subject = 'Health Education'
        self.create_quiz_with_questions(subject)
        assert self.teacher.get_questions('Health Education') == {
            '1': {
                'question': 'How are you?',
                'options': {'A': 'Good', 'B': 'Not good'}
            },
            '3': {
                'question': 'Are you sure?',
                'options': {'A': 'Yes', 'B': 'No'}
            },
            '2': {
                'question': 'Cold or Fever?',
                'options': {'A': 'Cold', 'B': 'Fever'}
            }
        }

    def test_assign_quiz_without_questions(self):
        subject = 'Science'
        self.create_quiz(subject)

        with pytest.raises(InvalidAction) as excinfo:
            questions = self.teacher.get_questions(subject)
            self.teacher.assign_quiz(self.student, subject, questions)
        assert 'Please add questions before assigning quiz.' in str(excinfo.value)

    def test_assign_quiz(self):
        subject = 'Health Education'
        self.create_quiz_with_questions(subject)

        questions = self.teacher.get_questions(subject)
        self.teacher.assign_quiz(self.student, subject, questions)
        assert self.student.quiz == {
            'name': 'Aaron Buddy',
            'questions': {
                '1': {
                    'question': 'How are you?',
                    'options': {'A': 'Good', 'B': 'Not good'}
                },
                '3': {
                    'question': 'Are you sure?',
                    'options': {'A': 'Yes', 'B': 'No'}
                },
                '2': {
                    'question': 'Cold or Fever?',
                    'options': {'A': 'Cold', 'B': 'Fever'}
                }
            },
            'subject': 'Health Education'
        }

    def test_grade_incomplete_quiz(self):
        # Create quiz
        subject = 'Health Education'
        self.create_quiz_with_questions(subject)

        # Assign quiz
        questions = self.teacher.get_questions(subject)
        self.teacher.assign_quiz(self.student, subject, questions)

        # Solve quiz
        self.student.solve_question(1, 'A')
        quiz = self.student.solve_question(2, 'A')

        with pytest.raises(InvalidAction) as excinfo:
            self.teacher.grade_quiz(quiz)
        assert 'You cannot grade an incomplete quiz.' in str(excinfo.value)

    def test_grade_quiz(self):
        # Create quiz
        subject = 'Health Education'
        self.create_quiz_with_questions(subject)

        # Assign quiz
        questions = self.teacher.get_questions(subject)
        self.teacher.assign_quiz(self.student, subject, questions)

        # Solve quiz
        self.student.solve_question(1, 'B')
        self.student.solve_question(2, 'A')
        quiz = self.student.solve_question(3, 'B')

        # Submit quiz
        completed_quiz = self.student.submit_quiz(quiz)

        #Grade quiz
        assert self.teacher.grade_quiz(completed_quiz) == {'Aaron Buddy': '66.67'}