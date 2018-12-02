import pytest

from main import Teacher, Student, InvalidAction

class TestStudent:
    def setup_method(self):
        self.student = Student('Aaron Buddy', 'Form 2')
        self.teacher = Teacher('Dayo Osikoya', 'Form 2')

        # Create quiz
        subject = 'Health Education'
        self.teacher.create_quiz(subject)
        self.teacher.add_question(subject, 'How are you?', {'A': 'Good', 'B': 'Not good'}, 'B')
        self.teacher.add_question(subject, 'Are you sure?', {'A': 'Yes', 'B': 'No'}, 'B')
        self.teacher.add_question(subject, 'Cold or fever?', {'A': 'Cold', 'B': 'Fever'}, 'B')

        # Assign quiz to student
        questions = self.teacher.get_questions(subject)
        student_with_quiz = self.teacher.assign_quiz(self.student, subject, questions)

    def test_student_details(self):
        assert self.student.name == 'Aaron Buddy'
        assert self.student.classroom == 'Form 2'

    def test_solve_question_answer_does_not_exist(self):
        with pytest.raises(InvalidAction) as excinfo:
            quiz = self.student.solve_question(1, 'C')
        assert 'Answer provided is not in options.' in str(excinfo.value)

    def test_solve_question(self):
        quiz = self.student.solve_question(1, 'A')
        assert quiz == {
            'name': 'Aaron Buddy',
            'answers': {'1': 'A'},
            'questions': {
                '1': {
                    'question': 'How are you?',
                    'options': {'A': 'Good', 'B': 'Not good'}
                },
                '3': {
                    'question': 'Cold or fever?',
                    'options': {'A': 'Cold', 'B': 'Fever'}
                },
                '2': {
                    'question': 'Are you sure?',
                    'options': {'A': 'Yes', 'B': 'No'}
                }
            },
            'subject': 'Health Education'
        }

    def test_submit_quiz(self):
        self.student.solve_question(1, 'A')
        self.student.solve_question(2, 'A')
        quiz = self.student.solve_question(3, 'A')

        completed_quiz = self.student.submit_quiz(quiz)
        assert completed_quiz == {
            'answers': {'1': 'A', '3': 'A', '2': 'A'},
            'completed': True,
            'name': 'Aaron Buddy',
            'questions': {
                '1': {
                    'question': 'How are you?', 'options': {'A': 'Good', 'B': 'Not good'}
                },
                '3': {
                    'question': 'Cold or fever?', 'options': {'A': 'Cold', 'B': 'Fever'}
                },
                '2': {
                    'question': 'Are you sure?', 'options': {'A': 'Yes', 'B': 'No'}
                }
            },
            'subject': 'Health Education'
        }

    def test_submit_incomplete_quiz(self):
        quiz = self.student.solve_question(1, 'A')
        with pytest.raises(InvalidAction) as excinfo:
            self.student.submit_quiz(quiz)
        assert 'You can only submit quiz after answering all questions.' in str(excinfo.value)