"""Configuration for the annotated screenshot test framework."""
import os

# Browser settings
HEADLESS = os.getenv("SP_HEADLESS", "true").lower() == "true"
BROWSER = os.getenv("SP_BROWSER", "chromium")  # chromium, firefox, webkit
VIEWPORT_WIDTH = int(os.getenv("SP_VIEWPORT_WIDTH", "1280"))
VIEWPORT_HEIGHT = int(os.getenv("SP_VIEWPORT_HEIGHT", "720"))
SLOW_MO = int(os.getenv("SP_SLOW_MO", "0"))  # ms between actions

# Screenshot / annotation settings
OUTPUT_DIR = os.getenv("SP_OUTPUT_DIR", "reports")
MARKER_COLOR = (255, 50, 50)  # RGB red
MARKER_RADIUS = 18
MARKER_RING_WIDTH = 4
ARROW_LENGTH = 60
ARROW_COLOR = (255, 50, 50)
LABEL_FONT_SIZE = 16
LABEL_COLOR = (255, 255, 255)
LABEL_BG_COLOR = (200, 30, 30)

# Timing
SCREENSHOT_DELAY_MS = int(os.getenv("SP_SCREENSHOT_DELAY", "300"))
