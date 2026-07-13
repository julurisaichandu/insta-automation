import os
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1080, 1080
BG_COLOR = (18, 18, 18)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (255, 90, 95)

FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def generate_image(text, output_path="output/post.jpg"):
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)

    font_size = 64
    wrapped = textwrap.fill(text, width=22)
    font = load_font(font_size)
    bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=12)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    while (text_w > WIDTH - 160 or text_h > HEIGHT - 300) and font_size > 24:
        font_size -= 4
        font = load_font(font_size)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=12)
        text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    x = (WIDTH - text_w) / 2
    y = (HEIGHT - text_h) / 2
    draw.multiline_text((x, y), wrapped, font=font, fill=TEXT_COLOR, align="center", spacing=12)

    bar_h = 10
    draw.rectangle([0, HEIGHT - bar_h, WIDTH, HEIGHT], fill=ACCENT_COLOR)

    img.save(output_path, "JPEG", quality=95)
    return output_path


if __name__ == "__main__":
    context = sys.argv[1] if len(sys.argv) > 1 else "Your context text goes here."
    path = generate_image(context)
    print(f"Saved: {path}")
