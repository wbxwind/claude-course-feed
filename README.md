# claude-course-feed

Daily Slack feed that summarizes lessons from the **Claude Certified Architect — Foundations** course. Runs automatically at 10:00 AM PDT via GitHub Actions.

---

## How it works

1. GitHub Actions triggers at 17:00 UTC (10 AM PDT) every day.
2. `scripts/summarize_and_post.py` computes which lesson day it is (Day 1 = April 24, 2026).
3. It reads `lessons/day-NN.md` for that day.
4. It calls **Claude claude-sonnet-4** to generate a concise Slack summary (intro sentence + bullet points).
5. It posts the message to your Slack channel via Incoming Webhook.

---

## Repository structure

```
claude-course-feed/
├── lessons/
│   ├── day-01.md          ← Real content (Days 1-7 from course material)
│   ├── day-02.md
│   ├── ...
│   ├── day-08.md          ← Stubs for Days 8-21 (fill in your notes)
│   └── day-21.md
├── scripts/
│   └── summarize_and_post.py
├── .github/
│   └── workflows/
│       └── daily_post.yml
└── README.md
```

---

## Setup: GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret** and add:

| Secret name         | Value                                              |
|---------------------|----------------------------------------------------|
| `ANTHROPIC_API_KEY` | Your key from https://console.anthropic.com        |
| `SLACK_WEBHOOK_URL` | The Incoming Webhook URL from your Slack workspace |

---

## Testing manually

You can trigger the workflow at any time from the **Actions** tab in GitHub:

1. Click **Daily Claude Certification Feed** in the left sidebar.
2. Click **Run workflow** → **Run workflow**.

Or run locally (requires both env vars to be set in your shell):

```bash
cd claude-course-feed
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
python scripts/summarize_and_post.py
```

---

## Updating lesson stubs (Days 8-21)

Files `lessons/day-08.md` through `lessons/day-21.md` are stubs. As you complete each week, replace the placeholder content with your actual notes — Claude will use whatever is in the file to generate the summary.

---

## Schedule reference

| Day | Date       | Topic                                          |
|-----|------------|------------------------------------------------|
| 1   | Apr 24     | Orientation & Exam Format                      |
| 2   | Apr 25     | Claude API Fundamentals                        |
| 3   | Apr 26     | System Prompt, Context Window, tool_use        |
| 4   | Apr 27     | JSON Schemas & Error Handling                  |
| 5   | Apr 28     | Message Batches API                            |
| 6   | Apr 29     | Agent SDK: Agentic Loop                        |
| 7   | Apr 30     | Coordinator, Subagents, Hooks                  |
| 8   | May 1      | MCP Fundamentals                               |
| 9   | May 2      | MCP isError, Resources                         |
| 10  | May 3      | Claude Code: CLAUDE.md & Rules                 |
| 11  | May 4      | Slash Commands, Skills, Planning Mode          |
| 12  | May 5      | /compact, /memory, CI/CD, Sessions             |
| 13  | May 6      | Built-in Tools + Practice Set                  |
| 14  | May 7      | Week 2 Review                                  |
| 15  | May 8      | Prompt Engineering I                           |
| 16  | May 9      | Prompt Engineering II + Task Decomposition     |
| 17  | May 10     | Escalation & Error Handling                    |
| 18  | May 11     | Context Management & Provenance                |
| 19  | May 12     | Domain Review + Exercises 1 & 3                |
| 20  | May 13     | Practical Exercise 4 + Practice Questions      |
| 21  | May 14     | Final Practice Test & Readiness Check          |
