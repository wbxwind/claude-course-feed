"""
summarize_and_post.py

Calculates today's lesson day based on course start date,
reads the corresponding lessons/day-NN.md file,
calls Claude API to generate a Slack-ready summary (bullets + short intro),
and posts it to a Slack Incoming Webhook.

Required environment variables:
  ANTHROPIC_API_KEY   — Your Anthropic API key
  SLACK_WEBHOOK_URL   — Slack Incoming Webhook URL
"""

import os
import sys
from datetime import date, timedelta
import anthropic
import urllib.request
import urllib.error
import json

# ── Config ────────────────────────────────────────────────────────────────────

COURSE_START = date(2026, 5, 28)   # Day 1
TOTAL_DAYS   = 21
LESSONS_DIR  = os.path.join(os.path.dirname(__file__), "..", "lessons")

# ── Helpers ───────────────────────────────────────────────────────────────────

def get_day_number() -> int | None:
    """Return today's lesson day number (1-21), or None if outside the window."""
    today = date.today()
    delta = (today - COURSE_START).days + 1  # Day 1 on start date
    if delta < 1 or delta > TOTAL_DAYS:
        return None
    return delta


def read_lesson(day: int) -> str:
    """Read the markdown file for the given day number."""
    filename = f"day-{day:02d}.md"
    path = os.path.join(LESSONS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Lesson file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def generate_summary(lesson_text: str, day: int) -> str:
    """
    Call Claude claude-sonnet-4 to generate a Slack-ready summary.
    Format: one-sentence intro + 3-5 bullet points of key concepts.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = (
        "You are a study coach helping an architect candidate review their Claude certification lessons. "
        "Your summaries are concise, exam-focused, and easy to absorb in under 2 minutes. "
        "Always respond in the same language as the lesson content (English)."
    )

    user_prompt = f"""Below is the content for Day {day} of the Claude Certified Architect — Foundations course.

Produce a Slack message with this exact structure (no markdown headers, just the text):

*Day {day} of 21 — [Topic Name]*
[One sentence that explains what this lesson covers and why it matters for the exam.]

Key concepts:
• [Point 1 — be specific, include any relevant terms, parameters, or patterns]
• [Point 2]
• [Point 3]
• [Point 4 if warranted]
• [Point 5 if warranted]

_Study tip: [One actionable tip for retaining or applying today's material.]_

Keep the entire message under 250 words. Do not add any text before or after this structure.

---
LESSON CONTENT:
{lesson_text}
"""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    return message.content[0].text.strip()


def post_to_slack(text: str) -> None:
    """POST a message to the Slack Incoming Webhook."""
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        raise EnvironmentError("SLACK_WEBHOOK_URL environment variable not set.")

    payload = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode()
            if body != "ok":
                raise RuntimeError(f"Unexpected Slack response: {body}")
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Slack webhook HTTP error {e.code}: {e.read().decode()}") from e


# ── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    day = get_day_number()

    if day is None:
        today = date.today()
        if today < COURSE_START:
            print(f"Course hasn't started yet. Start date: {COURSE_START}. Skipping.")
        else:
            print(f"Course is complete (ended Day {TOTAL_DAYS}). Skipping.")
        sys.exit(0)

    print(f"Today is Day {day} of {TOTAL_DAYS}.")

    print(f"Reading lesson file for Day {day}...")
    lesson_text = read_lesson(day)

    print("Generating summary via Claude API...")
    summary = generate_summary(lesson_text, day)
    print("--- SUMMARY PREVIEW ---")
    print(summary)
    print("-----------------------")

    print("Posting to Slack...")
    post_to_slack(summary)
    print("Posted successfully.")


if __name__ == "__main__":
    main()
