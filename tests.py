from purchase_analyzer import *


def test_read_valid_lines():
    purchases = read_purchases('incorrect.txt')

    assert purchases[0]["name"] == "apple"
    assert purchases[1]["price"] == 5.0


def test_skip_bad_lines_wrong_fields():
    purchases = read_purchases('incorrect.txt')

    assert len(purchases) == 3


def test_count_errors():
    errors = count_errors('incorrect.txt')

    assert errors == 1


def test_total_spent():
    purchases = read_purchases('incorrect.txt')
    total = total_spent(purchases)
    assert total == 42.30


def test_spent_by_category():
    purchases = read_purchases('incorrect.txt')
    result = spent_by_category(purchases)
    assert result["food"] == 35.0


def test_top_n_expensive():
    purchases = read_purchases('incorrect.txt')
    topik = top_n_expensive(purchases, n=3)
    assert topik[0]["name"] == "apple"
    assert topik[1]["name"] == "banana"
    assert topik[2]["name"] == "Vitamins C"