#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: markdown_to_pdf.py
Author: Maria Kevin
Created: 2025-12-10
Description: Brief description
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"


import os
import uuid

from markdown_pdf import MarkdownPdf, Section


def make_pdf(markdown: str) -> str:
    """Generate PDF from markdown and return the URL path for download."""
    pdf = MarkdownPdf(toc_level=2, optimize=True)
    user_css = """
        body {
        font-family: "Helvetica", "Arial", sans-serif;
        color: #333333;
        margin: 0.5in;
}
"""
    pdf.add_section(Section(markdown), user_css=user_css)
    
    # Generate unique filename
    pdf_filename = f"brochure_{uuid.uuid4()}.pdf"
    
    # Save to assets directory (Reflex serves files from here)
    os.makedirs("assets", exist_ok=True)
    file_path = os.path.join("assets", pdf_filename)
    pdf.save(file_path)
    
    # Return URL path (Reflex serves assets at /filename)
    return f"/{pdf_filename}"