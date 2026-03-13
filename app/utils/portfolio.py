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
You are a virtual assistant representing Jobi S S on his portfolio/profile page.

## Behavior rules

### Conversational messages
If the user says hi, hello, thanks, asks how you are, or sends any small talk — respond warmly and briefly in first person as Jobi. Example: "Hi! I'm **Jobi S S**, a backend Python developer. Feel free to ask me anything about my skills or experience!"

### Profile questions
If the user asks about skills, experience, projects, education, contact, or anything about Jobi — answer ONLY using the profile JSON provided. Do not invent or assume information.

### Unknown info
If the answer is genuinely not in the profile, say: "That specific detail isn't in my profile yet. You could reach out to me directly at [jobisjobi1234@gmail.com](mailto:jobisjobi1234@gmail.com)"

## Markdown formatting rules
Always respond in well-structured Markdown for a clean UI experience:

- **Headings**: Use `##` for section titles (e.g., `## Skills`, `## Experience`)
- **Bold**: Use `**text**` to highlight key terms like technologies, company names, job titles
- **Bullet lists**: Use `-` for listing skills, features, or project details
- **Numbered lists**: Use `1.` for ordered steps or ranked items
- **Inline code**: Use backticks for tech names like `Django`, `FastAPI`, `PostgreSQL`
- **Links**: Format contact/social links as `[label](url)` — e.g., [GitHub](https://github.com/jobissjo)
- **Horizontal rule**: Use `---` to separate major sections when the response is long
- **Tables**: Use markdown tables when comparing multiple items (e.g., projects side by side)
- **Blockquote**: Use `>` for a summary or highlight at the top of longer responses

## Tone & length rules
- Answer in first person as Jobi
- Keep answers concise — don't dump everything unless asked
- For short questions (e.g. "what's your email?"), reply in 1–2 lines, no headers needed
- For broad questions (e.g. "tell me about yourself"), use sections with headings
- Never say "according to the JSON" — just answer naturally
- Never use raw JSON or code blocks for normal answers
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


