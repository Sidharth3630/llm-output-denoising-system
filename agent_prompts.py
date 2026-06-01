"""Prompt templates and schemas for agent outputs."""

# Kept as a convenience for humans/diagnostics.
FINAL_SCHEMA = {
    "agent_name": "string",
    "issues": [
        {
            "category": "factual_errors|repetition|inconsistency|style",
            "description": "string",
            "severity": "low|medium|high",
        }
    ],
    "changes_made": ["string"],
    "revised_text": "string",
}

# Minimal JSON output instruction to keep parsing reliable.
STRUCTURED_OUTPUT_INSTRUCTIONS = (
    "Return ONLY valid JSON that matches this shape: {"
    "\"agent_name\": string,"
    "\"issues\": [{\"category\": \"factual_errors|repetition|inconsistency|style\", "
    "\"description\": string, \"severity\": \"low|medium|high\"}],"
    "\"changes_made\": [string],"
    "\"revised_text\": string"
    "}. "
    "No markdown, no commentary, no trailing commas."
)

