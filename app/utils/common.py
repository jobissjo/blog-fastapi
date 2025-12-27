from typing import Dict, Optional
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
import asyncio
from fastapi import status


class CustomException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: Optional[Dict] = None,
    ):
        self.message = message
        self.status_code = status_code
        self.data = data




template_path = Path(__file__).parent.parent / 'templates'
environment = Environment(loader=FileSystemLoader(template_path))

async def render_email_template(template_name:str, payload_data:dict):
    template = environment.get_template(template_name)
    return await asyncio.to_thread(template.render, **payload_data)

