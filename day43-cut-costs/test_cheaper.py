import cheaper as c


def test_routes_easy_questions_to_the_small_model():
    assert c.route("Are you open on Sunday?") == c.SMALL
    assert c.route("Why was I charged twice?") == c.LARGE


def test_cached_system_prompt_drops_repeat_tokens():
    full = c.estimate(6, 3000, c.LARGE, cached_system=False)
    cached = c.estimate(6, 3000, c.LARGE, cached_system=True)
    saved = (6 - 1) * c.SYSTEM_TOKENS * c.PRICE[c.LARGE] / 1_000_000
    assert round(full - cached, 4) == round(saved, 4)
    assert cached < full


def test_five_demo_tasks_are_about_ten_times_cheaper():
    fat = c.bill_for(c.DEMO, fat=True)
    cheap = c.bill_for(c.DEMO, fat=False)
    assert fat / cheap >= 10
    assert cheap > 0
