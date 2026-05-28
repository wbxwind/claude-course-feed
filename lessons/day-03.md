# Day 3 — Mandatory Read
**Date:** Sunday, April 26, 2026
**Topic:** System Prompt, Context Window, `tool_use`, Tool Definition, `tool_choice`
**Source:** `claude-certified-architect/guide_en.MD`, lines 169–251
**Time:** ~40 minutes

---

## 1.4 System Prompt

The system prompt is a special instruction that defines context and behavioral rules. It:
- Is not part of the `messages` array; it is passed separately in the `system` field
- Has priority over user messages
- Is loaded once and applies throughout the conversation
- Is used to define role, constraints, and output format

**Important for the exam:** system prompt wording can create unintended tool associations. For example, an instruction like "always verify the customer" can cause the model to overuse `get_customer`, even when it is unnecessary.

## 1.5 Context Window

The context window is the total amount of text (in tokens) the model can process at once. It includes:
- The system prompt
- The full message history
- Tool definitions
- Tool results

**Key context-window problems:**

1. **Lost-in-the-middle effect:** models reliably process information at the start and end of a long input but can miss details in the middle. Mitigation: place key information near the beginning or end.

2. **Accumulation of tool results:** every tool call adds output to the context. If a tool returns 40+ fields but only 5 matter, then most of the context is wasted.

3. **Progressive summarization:** when compressing history, numeric values, percentages, and dates often get lost and become vague ("about", "roughly", "a few").

---

# Chapter 2: Tools and `tool_use`

> Documentation: [Tool Use](https://platform.claude.com/docs/en/build-with-claude/tool-use)

## 2.1 What is `tool_use`

`tool_use` is a mechanism that allows Claude to call external functions. The model does not run code directly—it generates a structured tool call request; your code executes it and returns the result.

## 2.2 Tool Definition

Each tool is defined using a JSON schema:

```json
{
  "name": "get_customer",
  "description": "Finds a customer by email or ID. Returns the customer profile, including name, email, order history, and account status. Use this tool BEFORE lookup_order to verify the customer's identity. Accepts an email (format: user@domain.com) or a numeric customer_id.",
  "input_schema": {
    "type": "object",
    "properties": {
      "email": {"type": "string", "description": "Customer email"},
      "customer_id": {"type": "integer", "description": "Numeric customer ID"}
    },
    "required": []
  }
}
```

**Critically important aspects of a tool description:**

1. **The description is the primary selection mechanism.** An LLM chooses tools based on their descriptions. Minimal descriptions ("Retrieves customer information") lead to mistakes when tools overlap.

2. **Include in the description:**
   - What the tool does and returns
   - Input formats and example values
   - Edge cases and constraints
   - When to use this tool vs similar alternatives

3. **Avoid** identical or overlapping descriptions across tools. If `analyze_content` and `analyze_document` have nearly identical descriptions, the model will confuse them.

4. **Built-in tools vs MCP tools:** agents may prefer built-in tools (Read, Grep) over MCP tools with similar functionality. To prevent this, strengthen MCP tool descriptions—highlight concrete advantages, unique data, or context that built-in tools cannot provide.

## 2.3 The `tool_choice` Parameter

`tool_choice` controls how the model selects tools:

| Value | Behavior | When to use |
|---|---|---|
| `{"type": "auto"}` | The model decides whether to call a tool or answer in text | Default for most cases |
| `{"type": "any"}` | The model **must** call some tool | When you need guaranteed structured output |
| `{"type": "tool", "name": "extract_metadata"}` | The model **must** call a specific tool | When you need a forced first step / execution order |

**Important scenarios:**
- `tool_choice: "any"` + multiple extraction tools → the model picks the best one, but you still get structured output
- Forced selection → when you must guarantee a specific first action (e.g., `extract_metadata` before enrichment)

---

## After reading, do:
1. Make 5 flashcards: lost-in-the-middle, accumulation of tool results, progressive summarization, `auto` vs `any` vs forced `tool_choice`, built-in vs MCP tool preference.
2. Answer in one sentence: "Why does `tool_choice: any` matter for structured output?"
3. Note one mistake to avoid when writing tool descriptions.
4. Log open questions in `NOTES.md`.
