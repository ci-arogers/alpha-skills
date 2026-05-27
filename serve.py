"""Alpha Skills MCP Server.

Discovers SKILL.md files from the skills/ directory and exposes them as:
  - MCP Prompts  → /skill-name slash commands in Claude Code
  - MCP Tools    → programmatic invocation by agents

Skills follow the agentskills.io SKILL.md standard:
  skills/
    my-skill/
      SKILL.md   (YAML frontmatter + Markdown instructions)

Usage:
    python serve.py
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path

import mcp.server.stdio
import mcp.types as types
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions

_ROOT = Path(__file__).resolve().parent
_SKILLS_DIR = _ROOT / "skills"


# ---------------------------------------------------------------------------
# Skill discovery
# ---------------------------------------------------------------------------

def _parse_skill(skill_dir: Path) -> dict | None:
    """Parse a SKILL.md file into a skill definition."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return None

    text = skill_md.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    frontmatter = {}
    body = text
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        body = fm_match.group(2).strip()
        for line in fm_text.splitlines():
            if ":" in line:
                key, _, val = line.partition(":")
                frontmatter[key.strip()] = val.strip()

    name = frontmatter.get("name", skill_dir.name)
    description = frontmatter.get("description", "")
    allowed_tools = frontmatter.get("allowed-tools", "")

    # Parse arguments from frontmatter if present
    arguments = []
    raw_args = frontmatter.get("arguments", "")
    if raw_args:
        for arg in raw_args.split(","):
            arg = arg.strip()
            if arg:
                required = not arg.endswith("?")
                arg_name = arg.rstrip("?")
                arguments.append(types.PromptArgument(
                    name=arg_name,
                    description=f"Argument: {arg_name}",
                    required=required,
                ))

    return {
        "name": name,
        "description": description,
        "body": body,
        "arguments": arguments,
        "allowed_tools": allowed_tools,
        "path": str(skill_md),
    }


def _discover_skills() -> dict[str, dict]:
    """Discover all SKILL.md files in skills/ directory."""
    skills = {}
    if not _SKILLS_DIR.exists():
        return skills
    for skill_dir in sorted(_SKILLS_DIR.iterdir()):
        if skill_dir.is_dir():
            skill = _parse_skill(skill_dir)
            if skill:
                skills[skill["name"]] = skill
    return skills


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

app = Server("alpha-skills")


@app.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    skills = _discover_skills()
    return [
        types.Prompt(
            name=s["name"],
            description=s["description"],
            arguments=s["arguments"] or None,
        )
        for s in skills.values()
    ]


@app.get_prompt()
async def get_prompt(
    name: str,
    arguments: dict[str, str] | None,
) -> types.GetPromptResult:
    skills = _discover_skills()
    skill = skills.get(name)
    if not skill:
        raise ValueError(f"Skill not found: {name}")

    body = skill["body"]

    # Simple argument substitution: {{arg_name}} → value
    if arguments:
        for k, v in arguments.items():
            body = body.replace(f"{{{{{k}}}}}", v)

    return types.GetPromptResult(
        description=skill["description"],
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(type="text", text=body),
            )
        ],
    )


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """Expose skills as tools for programmatic invocation."""
    skills = _discover_skills()
    tools = []
    for s in skills.values():
        # Build JSON schema for tool arguments
        properties = {}
        required = []
        for arg in s["arguments"]:
            properties[arg.name] = {"type": "string", "description": arg.description}
            if arg.required:
                required.append(arg.name)

        tools.append(types.Tool(
            name=f"skill__{s['name'].replace('-', '_')}",
            description=f"[Skill] {s['description']}",
            inputSchema={
                "type": "object",
                "properties": properties,
                "required": required,
            },
        ))
    return tools


@app.call_tool()
async def call_tool(
    name: str,
    arguments: dict,
) -> list[types.TextContent]:
    if not name.startswith("skill__"):
        raise ValueError(f"Unknown tool: {name}")

    skill_name = name[len("skill__"):].replace("_", "-")
    skills = _discover_skills()
    skill = skills.get(skill_name)
    if not skill:
        raise ValueError(f"Skill not found: {skill_name}")

    body = skill["body"]
    for k, v in (arguments or {}).items():
        body = body.replace(f"{{{{{k}}}}}", v)

    return [types.TextContent(type="text", text=body)]


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

async def main():
    skill_count = len(_discover_skills())
    print(f"Alpha Skills MCP — {skill_count} skills loaded from {_SKILLS_DIR}", file=sys.stderr)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alpha-skills",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(prompts_changed=True),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
