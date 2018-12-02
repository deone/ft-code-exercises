from main import Teacher

def test_teacher():
    t = Teacher('Dayo')
    assert t.name == 'Dayo'