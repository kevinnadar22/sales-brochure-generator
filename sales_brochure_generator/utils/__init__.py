#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: __init__.py
Author: Maria Kevin
Created: 2025-12-10
Description: Brief description
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

from .scraper import fetch_website_content, fetch_website_links, parallel_fetch_pages
from .markdown_to_pdf import make_pdf

__all__ = [
    "fetch_website_content",
    "fetch_website_links",
    "parallel_fetch_pages",
    "make_pdf",
]
