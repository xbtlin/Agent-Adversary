import os
import json
import asyncio
from typing import List, Dict, Optional
from playwright.async_api import async_playwright
from .base import BaseConnector

class BrowserConnector(BaseConnector):
    """
    Connector for testing browser-based agents or interacting with agents via a web UI.
    Uses Playwright for automation.
    """
    def __init__(self, url: str, input_selector: str, submit_selector: str, response_selector: str):
        self.url = url
        self.input_selector = input_selector
        self.submit_selector = submit_selector
        self.response_selector = response_selector
        self.history: List[Dict[str, str]] = []
        self.playwright = None
        self.browser = None
        self.page = None

    async def _init_browser(self):
        if not self.page:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.page = await self.browser.new_page()
            await self.page.goto(self.url)

    async def send_message_async(self, message: str) -> str:
        await self._init_browser()
        
        # Type the message
        await self.page.fill(self.input_selector, message)
        # Click submit
        await self.page.click(self.submit_selector)
        
        # Wait for a new response element to appear or change
        # This is a simplified wait strategy
        await self.page.wait_for_timeout(5000) 
        
        # Extract the latest response
        responses = await self.page.query_selector_all(self.response_selector)
        if responses:
            last_response = await responses[-1].inner_text()
        else:
            last_response = "Error: No response detected in browser UI."
            
        self.history.append({"role": "user", "content": message})
        self.history.append({"role": "agent", "content": last_response})
        return last_response

    def send_message(self, message: str) -> str:
        """Synchronous wrapper for async message sending."""
        return asyncio.run(self.send_message_async(message))

    async def reset_async(self):
        if self.page:
            await self.page.reload()
            self.history = []

    def reset(self):
        asyncio.run(self.reset_async())

    async def close_async(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def close(self):
        try:
            asyncio.run(self.close_async())
        except Exception:
            pass
