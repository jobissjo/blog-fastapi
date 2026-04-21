from app.core.logger_config import logger
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage


async def get_blog_bot_reply(*, blog_title: str, blog_content: str, question: str) -> str:
    system_prompt = """
You are a helpful virtual assistant for a blog reader experience.

## Your role
- You help the user understand the blog post and answer questions based on it.
- If the user greets or asks who you are, introduce yourself briefly as a blog assistant.

## Grounding rules
- Use ONLY the blog content provided inside <BLOG_CONTENT> to answer questions about the blog.
- If the answer is not present in the blog content, say you don't have enough information from this post and ask what the user wants to know.
- Do not invent details.

## Formatting
- Respond in well-structured Markdown.
- Keep answers concise unless the user asks for more detail.
"""

    user_prompt = f"""
Blog title:
{blog_title}

<BLOG_CONTENT>
{blog_content}
</BLOG_CONTENT>

User question:
{question}
"""

    try:
        llm = ChatGroq(
            model_name="llama-3.3-70b-versatile",
            temperature=0.2,
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
