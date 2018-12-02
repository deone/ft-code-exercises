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
        student_with_quiz = self.teacher.assign_quiz(self.student, subject)

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