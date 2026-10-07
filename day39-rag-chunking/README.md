# Day 39: Why your RAG gives bad answers — chunking

Day 10: RAG looks up chunks, then answers. If the chunk is wrong, the answer is wrong.
The usual cause is chunking: too big buries the fact, too small splits it in half.

```bash
python chunk.py sample/clinic.txt
```

You'll see the same question — *What is the last entry time on Sunday?* — fail when chunks
are tiny with no overlap, and succeed when each chunk repeats the end of the last one.

## The rule

Start around **400 tokens** with **100 tokens of overlap**, then eval (Day 40). There is no
magic number. Overlap is what keeps a fact like "last entry 1:30pm" in the same window as
"Sunday hours".

## Try next

- Swap in your own policy PDF text.
- Change `size` and `overlap` until the printed `YES` / `NO` flips.
- Replace the keyword `score` with real embeddings when you wire this into an agent.
