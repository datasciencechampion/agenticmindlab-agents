# Day 33: A resume-tailoring agent

Paste a job post and get your resume reworded for it, plus a match score and the skills you're missing.

```bash
pip install -r requirements.txt
cp ../.env.example .env        # then add your OPENAI_API_KEY
python tailor.py sample/resume.md sample/job.txt
```

Example output (the exact wording will vary):

```text
Match score: 78%
Missing skills: Docker, AWS
Changes:
  - Reworded "Worked on backend services" to highlight Python API work for checkout
  ...
Saved to tailored_resume.md. Read it before you send it!
```

Use your own resume as a markdown or text file, and paste the job post into a `.txt` file.

## The key rule

The system prompt says: **never invent experience, only reword what's true.** Skills from the job post that
aren't in your resume go into `missing_skills` instead of being added. Read the result before you send it,
because you are responsible for every line on your resume.

## Try next

- Generate a matching cover letter from the same inputs.
- Run it over 10 job posts and rank them by match score.
