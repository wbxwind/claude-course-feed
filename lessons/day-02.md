# Day 2 — Mandatory Read
**Date:** Saturday, April 25, 2026
**Topic:** Claude API — Request Structure, Message Roles, and `stop_reason`
**Source:** `claude-certified-architect/guide_en.MD`, lines 116–168
**Time:** ~25 minutes (after finishing Claude 101)

---

# Chapter 1: Claude API — Fundamentals of Model Interaction

> Documentation: [Messages API](https://platform.claude.com/docs/en/api/messages) | [Prompt Engineering](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)

## 1.1 API Request Structure

The Claude API follows a request–response model. Each request to the Claude Messages API includes:

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are a helpful assistant.",
  "messages": [
    {"role": "user", "content": "Hi!"},
    {"role": "assistant", "content": "Hello!"},
    {"role": "user", "content": "How are you?"}
  ],
  "tools": [...],
  "tool_choice": {"type": "auto"}
}
```

**Key fields:**
- `model` — model selection (`claude-opus-4-6`, `claude-sonnet-4-6`, `claude-haiku-4-5`)
- `max_tokens` — maximum number of tokens in the response
- `system` — the system prompt (defines model behavior)
- `messages` — conversation history (**you must send the full history** to maintain coherence)
- `tools` — definitions of available tools
- `tool_choice` — tool selection strategy

## 1.2 Message Roles

The `messages` array uses three roles:
- `user` — user messages
- `assistant` — model responses (included when sending history)
- `tool` — tool call results (the role is not explicitly set; this appears as a `tool_result` content block)

**Critically important:** on every API request you must send the **full conversation history**. The model does not persist state between requests—each call is independent.

## 1.3 The `stop_reason` Field in the Response

The Claude API response includes `stop_reason`, which indicates why the model stopped generating:

| Value | Description | Action |
|---|---|---|
| `"end_turn"` | The model finished its response | Show the result to the user |
| `"tool_use"` | The model wants to call a tool | Execute the tool and return the result |
| `"max_tokens"` | Token limit reached | The response is truncated; you may need to increase the limit |
| `"stop_sequence"` | A stop sequence was encountered | Handle based on your application logic |

For agentic systems, `"tool_use"` and `"end_turn"` are the most important—they control the agent loop.

---

## After reading, do:
1. Write out the 4 `stop_reason` values from memory and what your code should do on each.
2. Note in your own words: why must you resend the full history every request?
3. Finish Claude 101 remaining modules → claim the free certificate.
4. Add anything confusing to `NOTES.md`.
