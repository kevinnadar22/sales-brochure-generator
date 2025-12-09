#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: llm.py
Author: Maria Kevin
Created: 2025-12-10
Description: Brief description
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


from typing import Dict, List, Optional, Union
from openai import AsyncOpenAI

from ..utils import fetch_website_content, fetch_website_links, parallel_fetch_pages
import json
from config import settings
from loguru import logger

async def get_response(
    system_prompt: str,
    prompt: str,
    base_url: str = settings.base_url,
    model: str = settings.model,
    response_format: Optional[str] = "json_object",
) -> Union[Dict[str, List], str]:
    client = AsyncOpenAI(base_url=base_url, api_key=settings.openai_api_key)

    kwargs = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
    }
    if response_format == "json_object":
        kwargs["response_format"] = {"type": response_format}
    response = await client.chat.completions.create(**kwargs)
    response_text = response.choices[0].message.content
    logger.info(response_text)

    if response_format == "json_object":
        return json.loads(response_text or "{}")
    return response_text


async def select_relevant_links(url: str):
    links = await fetch_website_links(url)
    clean_links = [x for x in links if isinstance(x, str)]

    system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.
You should respond in JSON as in this example:

{
    "links": [
        {"type": "about page", "url": "https://full.url/goes/here/about"},
        {"type": "careers page", "url": "https://another.full.url/careers"}
    ]
}
    """
    prompt = f"""
Here is the list of links on the website {url} -
Please decide which of these are relevant web links for a brochure about the company, 
respond with the full https URL in JSON format as in the example.
Do not include Terms of Service, Privacy, email links.

Links (some might be relative links):
{'\n'.join(clean_links)}
    """
    response = await get_response(
        system_prompt,
        prompt,
    )
    return response.get("links", [])


async def fetch_page_and_relevant_links(url: str):
    relevant_links = await select_relevant_links(url)
    pages = await parallel_fetch_pages([link["url"] for link in relevant_links])
    landing_page = await fetch_website_content(url)
    text = f"Website: {url}\n\n# Landing page\n{landing_page}\n\n# Relevant pages\n{pages}"
    return text


async def generate_brochure(url: str):
    text = await fetch_page_and_relevant_links(url)

    text = text[:5000]

    system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
    """
    prompt = f"""
You are looking at a company called: {url}
Here are the contents of its landing page and other relevant pages;
use this information to build a short brochure of the company in markdown without code blocks.\n\n
{text}
"""
    response = await get_response(
        system_prompt,
        prompt,
        response_format="markdown"
    )
    return response