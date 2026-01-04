from typing import Dict, Any
import aiofiles
import json
from rapidfuzz import process, fuzz
from pathlib import Path
from app.core.logger_config import logger


PROFILE_CACHE: Dict[str, Any] | None = None


async def get_profile() -> Dict[str, Any]:
    global PROFILE_CACHE

    if PROFILE_CACHE is not None:
        return PROFILE_CACHE

    file_path = Path(__file__).parent.parent.parent / "profile.json"

    async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
        content = await f.read()
        PROFILE_CACHE = json.loads(content)

    return PROFILE_CACHE


INTENT_MAP = {
    "who are you": "basic.summary",
    "your name": "basic.name",
    "where are you located": "basic.location",
    "tell me about yourself": "basic.briefSummary",
    "tell me about experience": "experience",
    "skills": "skills",
    "tech stack": "skills",
    "technologies": "skills",
    "total experience": "total_experience",
    "total experience angular react django python": "total_experience_python_django_angular_react",
    "experience": "experience",
    "work experience": "experience",
    "projects": "projects",
    "portfolio projects": "projects",
    "contact": "contact",
    "email": "contact.email",
    "phone": "contact.phone",
    "links": "contact.links",
    "linkedin": "contact.links.linkedin",
    "github": "contact.links.github",
    "portfolio": "contact.links.portfolio",
    "leetcode": "contact.links.leetcode",
    "social media links": "contact.social_media_links",
}


# ----------------------------
# Helpers
# ----------------------------
def get_value_from_path(data: Dict[str, Any], path: str):
    for key in path.split("."):
        data = data[key]
    return data


def format_response(data: Any) -> str:
    if isinstance(data, dict):
        responses = []
        for k, v in data.items():
            if isinstance(v, list):
                responses.append(f"• {k}: {format_response(v)}")
            else:
                responses.append(f"• {k}: {v}")
        return "\n".join(responses)

    if isinstance(data, list):
        responses = []
        for item in data:
            if isinstance(item, dict):
                responses.append(f"• {item['name']}: {item.get('description', '')}")
            elif isinstance(item, list):
                responses.append(f"• {format_response(item)}")
            else:
                responses.append(str(item))
        return "\n".join(responses)

    return str(data)


async def get_bot_reply(question: str) -> str:
    profile = await get_profile()

    match, score, _ = process.extractOne(
        question.lower(), INTENT_MAP.keys(), scorer=fuzz.token_sort_ratio
    )

    if score < 55:
        return (
            "🤖 You can ask me about my skills, experience, projects, "
            "or how to contact me."
        )
    try:
        path = INTENT_MAP[match]
        data = get_value_from_path(profile, path)
        return format_response(data)
    except Exception as e:
        logger.error(f"Error in get_bot_reply: {e}")
        return "I'm sorry, I don't understand that. Can you please rephrase?"
