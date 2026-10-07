from pathlib import Path

import chunk

DOC = Path(__file__).parent.joinpath("sample", "clinic.txt").read_text(encoding="utf-8")
Q = "What is the last entry time on Sunday?"


def test_overlap_keeps_the_sunday_last_entry_fact():
    bad = chunk.retrieve(Q, chunk.chunk_text(DOC, 8, 0))[0]
    good = chunk.retrieve(Q, chunk.chunk_text(DOC, 16, 6))[0]
    assert "1:30" not in bad
    assert "1:30" in good
    assert "Sunday" in good


def test_step_never_stalls():
    assert chunk.chunk_text("one two three four", 2, 2) == ["one two", "two three", "three four", "four"]
