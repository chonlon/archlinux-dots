import os
import hyprlibs
from PIL import Image, ImageDraw, ImageFont
import textwrap


"""
this script will show the image from the clipboard, **ONLY WORKS WITH HYPRLAND**
qimgv, wl-paste and hyprctl are required, python pillow is also required
"""

def auto_fit_text_to_image(text, font_path, output_path,font_size=20, max_width=500, max_height=500, margin=20):
    # Create a blank image with a white background
    image = Image.new("RGB", (max_width, max_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Wrap the text based on the given maximum width
    wrapped_text = textwrap.fill(text, width=max_width // font_size)

    # Calculate the size of the text block after wrapping
    text_width, text_height = draw.textsize(wrapped_text, font=font)

    # Calculate the size of the image
    image_width = text_width + margin * 2
    image_height = text_height + margin * 2

    # Resize the image if needed to fit the text
    if image_width > max_width:
        image_width = max_width
    if image_height > max_height:
        image_height = max_height

    # Resize the image to the calculated size
    image = image.resize((image_width, image_height))

    # Draw the text on the image
    draw = ImageDraw.Draw(image)
    draw.text((margin, margin), wrapped_text, font=font, fill="black")

    image.save(output_path)

def simple_text_to_image(text, output_path):
    auto_fit_text_to_image(
        text=text,
        font_path="/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf",  # Replace with the path to your font file
        font_size=20,
        output_path=output_path
    )

def get_image_size(image_path):
    image = Image.open(image_path)
    return image.size

mime_type_out = "wl-paste -l" 
mime_type = hyprlibs.exec_or_remind(mime_type_out)

if mime_type.find("text") != -1:
  text = "wl-paste"
  text = hyprlibs.exec_or_remind(text)
  simple_text_to_image(text, "/tmp/clipboard.png")
else:
  paste = "wl-paste -t image/png > /tmp/clipboard.png"
  hyprlibs.exec_or_remind(paste)

iw, ih = get_image_size("/tmp/clipboard.png")

show = f'hyprctl dispatch exec "[float;pin;size {iw} {ih}]" qimgv /tmp/clipboard.png'
hyprlibs.exec_or_remind(show)