from pypypy import sum2

def test_sum2():
    assert sum2(15, 8) == 23

def test_true():
    assert True

def test_false():
    assert False, 'Тест всегда провален'