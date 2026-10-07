import server


def test_sunday_hours():
    assert "10am-2pm" in server.get_hours("Sunday")
    assert "1:30pm" in server.get_hours(" sunday ")


def test_unknown_day_is_closed():
    assert server.get_hours("holiday") == "Closed that day."


def test_book_slot_is_a_confirmation_not_a_side_effect():
    assert "Priya" in server.book_slot("Priya", "11am")
    assert "11am" in server.book_slot("Priya", "11am")
