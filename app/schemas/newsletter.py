from pydantic import BaseModel

class NewsletterSubscribeSchema(BaseModel):
    email: str
    