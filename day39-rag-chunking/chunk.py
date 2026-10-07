"""Why your RAG gives bad answers: chunking (Day 39).

Usage: python chunk.py sample/clinic.txt
"""
import argparse
from pathlib import Path

QUESTION = "What is the last entry time on Sunday?"


def chunk_text(text, size, overlap=0):
    """Split on words. size and overlap are word counts (close enough to tokens for a demo)."""
    words = text.split()
    if size < 1:
        raise ValueError("size must be at least 1")
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)]


def score(chunk, question):
    q = {w.strip("?.") for w in question.lower().split()}
    return sum(1 for w in chunk.lower().split() if w.strip(".,") in q)


def retrieve(question, chunks, k=1):
    ranked = sorted(chunks, key=lambda c: score(c, question), reverse=True)
    return ranked[:k]


def show(label, chunks, question):
    top = retrieve(question, chunks)[0]
    hit = "1:30" in top
    print(f"\n{label}  ({len(chunks)} chunks)")
    print(f"  retrieved: {top}")
    print(f"  last-entry fact present: {'YES' if hit else 'NO — the answer will be wrong'}")
    return hit


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("document", type=Path, nargs="?", default=Path("sample/clinic.txt"))
    args = p.parse_args()
    text = args.document.read_text(encoding="utf-8")
    question = QUESTION
    print(f"QUESTION: {question}")
    bad = show("TOO SMALL, NO OVERLAP  size=8 overlap=0", chunk_text(text, 8, 0), question)
    good = show("OVERLAP KEEPS FACTS    size=16 overlap=6", chunk_text(text, 16, 6), question)
    print("\nRule of thumb: start around 400 tokens with 100 of overlap, then test.")
    if bad and not good:
        raise SystemExit(1)
    if not good:
        print("This document may need a slightly larger overlap. That's the point: test.")


if __name__ == "__main__":
    main()
