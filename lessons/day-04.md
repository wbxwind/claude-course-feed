# Day 4 — Mandatory Read
**Date:** Monday, April 27, 2026
**Topic:** JSON Schemas for Structured Output, Syntax vs Semantic Errors
**Source:** `claude-certified-architect/guide_en.MD`, lines 252–304
**Time:** ~25 minutes (plus 30 min Anthropic Academy: Building with the Claude API)

---

## 2.4 JSON Schemas for Structured Output

Using `tool_use` with JSON schemas is the **most reliable** way to obtain structured output from Claude. It:
- Guarantees syntactically valid JSON (no missing braces, no trailing commas)
- Enforces the required structure (required fields are present)
- Does **not** guarantee semantic correctness (values can still be wrong)

**Schema design — key principles:**

```json
{
  "type": "object",
  "properties": {
    "category": {
      "type": "string",
      "enum": ["bug", "feature", "docs", "unclear", "other"]
    },
    "category_detail": {
      "type": ["string", "null"],
      "description": "Details if category = 'other' or 'unclear'"
    },
    "severity": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low"]
    },
    "confidence": {
      "type": "number",
      "minimum": 0,
      "maximum": 1
    },
    "optional_field": {
      "type": ["string", "null"],
      "description": "Null if the information was not found in the source"
    }
  },
  "required": ["category", "severity"]
}
```

**Schema design rules:**
1. **Required vs optional:** mark fields as required only if the information is always available. Required fields push the model to fabricate values when data is missing.
2. **Nullable fields:** use `"type": ["string", "null"]` for information that may be absent. The model can return `null` instead of hallucinating.
3. **Enums with `"other"`:** add `"other"` + a detail string to avoid losing data outside your predefined categories.
4. **Enum `"unclear"`:** for cases where the model cannot confidently pick a category—honest `"unclear"` is better than a wrong category.

## 2.5 Syntax vs Semantic Errors

| Error type | Example | Mitigation |
|---|---|---|
| **Syntax** | Invalid JSON, wrong field type | `tool_use` with a JSON schema (eliminates) |
| **Semantic** | Totals don't add up, value in wrong field, hallucination | Validation checks, retry with feedback, self-correction |

---

## After reading, do:
1. Draft a JSON schema for extracting invoice data with at least one `"other"` enum and one nullable field.
2. Explain in one line why JSON schemas solve syntax but not semantic errors.
3. Continue **Building with the Claude API** Modules 1–3 → https://anthropic.skilljar.com/claude-with-the-anthropic-api
4. Add takeaways or confusions to `NOTES.md`.
