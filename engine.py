"""Core engine — AnnotatedBrowser wraps Playwright and captures annotated screenshots."""
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from PIL import Image
import io

import config
import annotations


class AnnotatedBrowser:
    """A Playwright browser wrapper that auto-captures annotated screenshots on each action."""

    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or config.OUTPUT_DIR)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.step = 0
        self._pw = None
        self._browser: Browser = None
        self._context: BrowserContext = None
        self.page: Page = None

    def start(self):
        """Launch the browser."""
        self._pw = sync_playwright().start()
        launcher = getattr(self._pw, config.BROWSER)
        self._browser = launcher.launch(
            headless=config.HEADLESS,
            slow_mo=config.SLOW_MO,
        )
        self._context = self._browser.new_context(
            viewport={"width": config.VIEWPORT_WIDTH, "height": config.VIEWPORT_HEIGHT}
        )
        self.page = self._context.new_page()
        return self

    def stop(self):
        """Close browser and Playwright."""
        if self._browser:
            self._browser.close()
        if self._pw:
            self._pw.stop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        self.stop()

    # --- Actions ---

    def navigate(self, url: str):
        """Navigate to a URL and capture a screenshot."""
        self.page.goto(url, wait_until="domcontentloaded")
        self._wait()
        self._capture(action_text=f"Navigate: {url}")

    def click(self, selector: str):
        """Click an element, annotate the screenshot with click location."""
        element = self.page.locator(selector).first
        element.wait_for(state="visible", timeout=10000)
        box = element.bounding_box()
        if not box:
            raise ValueError(f"Element not found or not visible: {selector}")

        # Calculate click center
        cx = int(box["x"] + box["width"] / 2)
        cy = int(box["y"] + box["height"] / 2)

        element.click()
        self._wait()
        self._capture(
            click_pos=(cx, cy),
            action_text=f"Click: {selector}",
        )

    def fill(self, selector: str, text: str):
        """Fill an input field and capture a screenshot."""
        element = self.page.locator(selector).first
        element.wait_for(state="visible", timeout=10000)
        box = element.bounding_box()
        cx = int(box["x"] + box["width"] / 2) if box else None
        cy = int(box["y"] + box["height"] / 2) if box else None

        element.fill(text)
        self._wait()
        self._capture(
            click_pos=(cx, cy) if cx is not None else None,
            action_text=f"Fill: {selector} = '{text}'",
        )

    def select(self, selector: str, value: str):
        """Select a dropdown value."""
        self.page.locator(selector).first.select_option(value)
        self._wait()
        self._capture(action_text=f"Select: {selector} = '{value}'")

    def scroll(self, direction: str = "down", amount: int = 300):
        """Scroll the page."""
        delta = amount if direction == "down" else -amount
        self.page.mouse.wheel(0, delta)
        self._wait()
        self._capture(action_text=f"Scroll {direction} {amount}px")

    def wait(self, selector: str, timeout: int = 10000):
        """Wait for an element to appear."""
        self.page.locator(selector).first.wait_for(state="visible", timeout=timeout)
        self._capture(action_text=f"Wait for: {selector}")

    def screenshot(self, label: str = ""):
        """Take a manual screenshot without any action."""
        self._capture(action_text=label or "Manual screenshot")

    # --- Internal ---

    def _wait(self):
        """Brief pause to let the page settle after an action."""
        time.sleep(config.SCREENSHOT_DELAY_MS / 1000.0)

    def _capture(self, click_pos: tuple = None, action_text: str = ""):
        """Take a screenshot and annotate it."""
        self.step += 1
        raw_bytes = self.page.screenshot(type="png")
        img = Image.open(io.BytesIO(raw_bytes))

        if click_pos:
            img = annotations.draw_click_marker(img, click_pos[0], click_pos[1], self.step)

        if action_text:
            img = annotations.draw_action_label(img, f"Step {self.step}: {action_text}")

        filename = f"step_{self.step:03d}.png"
        img.save(self.output_dir / filename)
        print(f"  📸 {filename} — {action_text}")
