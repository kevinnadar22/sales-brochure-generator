#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: scraper.py
Author: Maria Kevin
Created: 2025-12-10
Description: Scraper for web scraping
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

import asyncio
from bs4._typing import _AttributeValue


import aiohttp
import bs4


async def scrape(url: str) -> bs4.BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return bs4.BeautifulSoup(await response.text(), "html.parser")


async def fetch_website_content(url: str) -> bs4.BeautifulSoup:
    soup = await scrape(url)
    # remove all script, img, css, js, and other non-content elements
    for element in soup.find_all(["script", "img", "style", "link", "meta", "iframe"]):
        element.decompose()
    return soup


async def fetch_website_links(url: str) -> list[_AttributeValue | None]:
    soup = await scrape(url)
    return [link.get("href") for link in soup.find_all("a")]


async def parallel_fetch_pages(urls: list[str]) -> list[bs4.BeautifulSoup]:
    tasks = [fetch_website_content(url) for url in urls]
    return await asyncio.gather(*tasks)
