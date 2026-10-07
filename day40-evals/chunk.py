"""Local copy of Day 39's chunker so this folder runs on its own."""


def chunk_text(text, size, overlap=0):
    words = text.split()
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)]


def score(chunk, question):
    q = {w.strip("?.") for w in question.lower().split()}
    return sum(1 for w in chunk.lower().split() if w.strip(".,") in q)


def retrieve(question, chunks, k=1):
    return sorted(chunks, key=lambda c: score(c, question), reverse=True)[:k]
