#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: config.py
Author: Maria Kevin
Created: 2025-12-10
Description: Brief description
"""

__author__ = "Maria Kevin"
__version__ = "0.1.0"

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model: str = "gpt-3.5-turbo"
    base_url: str = "https://api.openai.com/v1"
    openai_api_key: str = "blah"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
