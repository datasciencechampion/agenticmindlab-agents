"""Tailor your resume to a job post, without inventing experience (Day 33).

Usage: python tailor.py resume.md job.txt [-o tailored_resume.md]
"""
import argparse
import json
from pathlib import Path

MODEL = "gpt-4.1-mini"

SYSTEM_PROMPT = """You tailor resumes to job posts.
1. Read the job post and list its key skills and must-haves.
2. Match them to the candidate's REAL experience in the resume.
3. Rewrite bullet points to use the job post's language, leading with the most relevant work.

Rules:
- Never invent experience, skills, employers, dates or numbers. Only reword what's true.
- If a skill from the job post is missing from the resume, list it in missing_skills. Do not add it.
- Keep the same sections and markdown format as the original resume.

Reply in JSON:
{"tailored_resume": "<markdown>", "match_score": <0-100>, "missing_skills": ["..."],
 "changes": ["<one line per change you made>"]}"""


def tailor(resume, job_post, client):
    r = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": f"# RESUME\n{resume}\n\n# JOB POST\n{job_post}"}])
    result = json.loads(r.choices[0].message.content)
    result["match_score"] = max(0, min(100, int(result.get("match_score", 0))))
    result.setdefault("missing_skills", [])
    result.setdefault("changes", [])
    return result


def main():
    from dotenv import load_dotenv
    from openai import OpenAI

    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("resume", type=Path)
    p.add_argument("job", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("tailored_resume.md"))
    args = p.parse_args()

    load_dotenv()
    result = tailor(args.resume.read_text(), args.job.read_text(), OpenAI())
    args.output.write_text(result["tailored_resume"])

    print(f"Match score: {result['match_score']}%")
    print("Missing skills: " + (", ".join(result["missing_skills"]) or "none"))
    print("Changes:")
    for change in result["changes"]:
        print(f"  - {change}")
    print(f"\nSaved to {args.output}. Read it before you send it!")


if __name__ == "__main__":
    main()
