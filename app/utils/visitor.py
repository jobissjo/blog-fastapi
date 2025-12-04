import uuid
from fastapi import Request, Response


COOKIE_NAME = "visitor_id"
COOKIE_MAX_AGE = 60 * 60 * 24 * 365  # 1 year

def is_valid_uuid(value: str) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except Exception:
        return False


def get_or_set_visitor_id(request: Request, response: Response) -> str:
    # 1. Check query param
    query_id = request.query_params.get("visitor_id")
    if query_id and is_valid_uuid(query_id):
        # Set cookie to match query param ID
        response.set_cookie(
            key=COOKIE_NAME,
            value=query_id,
            max_age=COOKIE_MAX_AGE,
            httponly=True,
        )
        return query_id

    # 2. Check cookie
    cookie_id = request.cookies.get(COOKIE_NAME)
    if cookie_id and is_valid_uuid(cookie_id):
        return cookie_id

    # 3. No valid ID found → generate new
    new_id = str(uuid.uuid4())
    response.set_cookie(
        key=COOKIE_NAME,
        value=new_id,
        max_age=COOKIE_MAX_AGE,
        httponly=True,
    )
    return new_id
