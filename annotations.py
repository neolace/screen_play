"""Image annotation utilities — draws click markers, arrows, and labels on screenshots."""
import math
from PIL import Image, ImageDraw, ImageFont
import config


def draw_click_marker(image: Image.Image, x: int, y: int, step: int) -> Image.Image:
    """Draw a red circle + arrow + step label at the click position."""
    img = image.copy()
    draw = ImageDraw.Draw(img)

    # Draw concentric ring (circle outline)
    r = config.MARKER_RADIUS
    w = config.MARKER_RING_WIDTH
    bbox = (x - r, y - r, x + r, y + r)
    draw.ellipse(bbox, outline=config.MARKER_COLOR, width=w)

    # Draw small filled center dot
    dot_r = 4
    draw.ellipse((x - dot_r, y - dot_r, x + dot_r, y + dot_r), fill=config.MARKER_COLOR)

    # Draw arrow pointing to the click from upper-left
    _draw_arrow(draw, x, y)

    # Draw step number label
    _draw_label(draw, x, y, step, img_size=img.size)

    return img


def _draw_arrow(draw: ImageDraw.Draw, target_x: int, target_y: int):
    """Draw an arrow pointing toward (target_x, target_y) from upper-left offset."""
    length = config.ARROW_LENGTH
    angle = math.radians(225)  # coming from upper-left

    start_x = target_x + int(length * math.cos(angle))
    start_y = target_y + int(length * math.sin(angle))

    # Arrow shaft
    draw.line(
        [(start_x, start_y), (target_x, target_y)],
        fill=config.ARROW_COLOR,
        width=3,
    )

    # Arrowhead
    head_len = 14
    for offset_angle in [math.radians(150), math.radians(210)]:
        hx = target_x + int(head_len * math.cos(angle + offset_angle - math.pi))
        hy = target_y + int(head_len * math.sin(angle + offset_angle - math.pi))
        draw.line([(target_x, target_y), (hx, hy)], fill=config.ARROW_COLOR, width=3)


def _draw_label(draw: ImageDraw.Draw, x: int, y: int, step: int, img_size: tuple = None):
    """Draw a numbered label badge near the click marker, clamped to image bounds."""
    text = f" {step} "
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", config.LABEL_FONT_SIZE)
    except (OSError, IOError):
        font = ImageFont.load_default()

    # Default position: above-right of marker
    label_x = x + config.MARKER_RADIUS + 6
    label_y = y - config.MARKER_RADIUS - 10

    # Clamp to image bounds if size is known
    if img_size:
        w, h = img_size
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0] + 10
        text_h = text_bbox[3] - text_bbox[1] + 10
        if label_x + text_w > w:
            label_x = x - config.MARKER_RADIUS - text_w
        if label_y < 0:
            label_y = y + config.MARKER_RADIUS + 6

    bbox = draw.textbbox((label_x, label_y), text, font=font)
    padding = 3
    draw.rounded_rectangle(
        (bbox[0] - padding, bbox[1] - padding, bbox[2] + padding, bbox[3] + padding),
        radius=4,
        fill=config.LABEL_BG_COLOR,
    )
    draw.text((label_x, label_y), text, fill=config.LABEL_COLOR, font=font)


def draw_action_label(image: Image.Image, action_text: str) -> Image.Image:
    """Draw a semi-transparent action description bar at the bottom of the image."""
    img = image.convert("RGBA")
    width, height = img.size

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except (OSError, IOError):
        font = ImageFont.load_default()

    bar_height = 30
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [(0, height - bar_height), (width, height)],
        fill=(30, 30, 30, 220),
    )
    overlay_draw.text(
        (10, height - bar_height + 7),
        action_text,
        fill=(255, 255, 255, 255),
        font=font,
    )
    img = Image.alpha_composite(img, overlay)
    return img.convert("RGB")
