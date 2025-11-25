import uuid
from fastapi import Request, Response


COOKIE_NAME = "visitor_id"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year


def get_or_set_visitor_id(request: Request, response: Response) -> str:
    visitor_id = request.cookies.get(COOKIE_NAME)
    if not visitor_id:
        visitor_id = str(uuid.uuid4())
        response.set_cookie(
            key=COOKIE_NAME,
            value=visitor_id,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
        )
    return visitor_id
