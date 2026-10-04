# Day 34: A meeting-notes agent

Give it a meeting transcript and get a summary, the decisions, and who does what by when. Optionally, post the
notes to Slack.

```bash
pip install -r requirements.txt
cp ../.env.example .env        # then add your OPENAI_API_KEY
python notes.py sample/transcript.vtt
```

Example output (the exact wording will vary):

```text
*Summary*
• Launch plan reviewed; payment testing needs one more week
*Decisions*
• Launch moves from 8 October to 15 October
*Action items*
• Priya: Update the launch deck with the new date (by Friday)
• Rahul: Finish payment testing (by the 13th)
• UNASSIGNED: Tell the support team about the new date
```

## Getting a transcript

- **Zoom**: turn on cloud recording with audio transcript, then download the `.vtt` file.
- **Google Meet**: turn on transcripts; the transcript is saved to Google Drive. Copy it into a `.txt` file.
- **Microsoft Teams**: turn on transcription, then download the transcript as `.vtt`.

`.vtt`, `.srt` and plain `.txt` all work.

## Post to Slack

Create a Slack [incoming webhook](https://api.slack.com/messaging/webhooks), put its URL in `.env` as
`SLACK_WEBHOOK_URL`, then run:

```bash
python notes.py sample/transcript.vtt --slack
```

## The trick

The system prompt says **quote, don't guess**. Tasks nobody agreed to own are marked `UNASSIGNED` instead of
being given to whoever seems likely.

## Privacy

Always tell everyone the meeting is being recorded, and follow your company's rules about sending meeting
content to an AI provider.
