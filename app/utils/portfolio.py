from typing import Dict, Any
import aiofiles
import json
from pathlib import Path
from app.core.logger_config import logger
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import json


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



async def get_bot_reply(question: str) -> str:
    profile = await get_profile()

    system_prompt = """
You are an AI assistant acting as Jobi S S.

Rules:
1. You MUST answer ONLY using the provided profile JSON.
2. Do NOT add any information that is not present in the JSON.
3. Do NOT guess or assume.
4. If the answer is not found in the JSON, respond with:
   "I don't have that information in my profile. Could you please rephrase or ask something else?"
5. Answer in first person (as Jobi S S).
6. Keep responses clear, professional, and concise.
7. If the data is a list, format it as bullet points.
8. If the data is structured (skills, experience, projects), summarize naturally.
"""

    user_prompt = f"""
Here is my profile data (JSON):

<PROFILE_JSON>
{json.dumps(profile, indent=2)}
</PROFILE_JSON>

User question:
{question}

Based on the rules, answer the question.
"""

    try:
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,   # low hallucination
            streaming=False,
        )
        response = await llm.ainvoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt),
            ]
        )
        return response.content.strip()

    except Exception as e:
        logger.error(f"Groq error: {e}")
        return "Sorry, something went wrong while answering your question."


