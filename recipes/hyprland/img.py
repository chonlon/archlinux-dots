import os
import hyprlibs
import typer

import textwrap


"""
this script will show(pin) the image from the clipboard, **ONLY WORKS WITH HYPRLAND**
qimgv, wl-paste and hyprctl are required, python pillow is also required
"""
tmp_img_path = "/tmp/.image_edit"


def auto_fit_text_to_image(
    text,
    font_path,
    output_path,
    font_size=20,
    max_width=3000,
    max_height=1500,
    margin=20,
):
    from PIL import Image, ImageDraw, ImageFont

    # Create a blank image with a white background
    image = Image.new("RGB", (max_width, max_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Load the font
    font = ImageFont.truetype(font_path, font_size)

    # Wrap the text based on the given maximum width
    # wrapped_text = textwrap.fill(text, width=max_width // font_size)
    wrapped_text = text

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
        output_path=output_path,
    )


def get_image_size(image_path):
    from PIL import Image, ImageDraw, ImageFont

    image = Image.open(image_path)
    return image.size


def gen_image_path(parent_path=tmp_img_path):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    import datetime

    return os.path.join(
        parent_path, datetime.datetime.now().strftime("%Y%m%d_%H-%M_%S.png")
    )


app = typer.Typer()


def clear_tmp_image(path=tmp_img_path):
    # remove image 2 days ago
    import datetime
    try:
        outdated_images = [
            f
            for f in os.listdir(path)
            if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")
        ]
        outdated_images = [
            f
            for f in outdated_images
            if datetime.datetime.strptime(f, "%Y%m%d_%H-%M_%S.png")
            < datetime.datetime.now() - datetime.timedelta(days=2)
        ]
        for f in outdated_images:
            os.remove(os.path.join(path, f))
    except Exception as e:
        print(e)

@app.command()
def show_folder(folder):
    files = os.listdir(folder)
    files = [
        f
        for f in files
        if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")
    ]
    print(files)
    max_img = 10
    if len(files) > max_img:
        files = files[:max_img]
    # full path
    files = [os.path.join(folder, f) for f in files]
    for f in files:
        iw, ih = get_image_size(f)
        show = f'hyprctl dispatch exec "[workspace special:img;maxsize {iw} {ih};bordersize 2; bordercolor rgba(ffff81ac);opacity 0.9;rounding 0;]" qimgv "{f}"'
        print(show)
        hyprlibs.exec_or_remind(show)


@app.command()
def to_workspace():
    win = hyprlibs.get_current_window()
    hyprlibs.exec_or_remind(f"hyprctl dispatch togglefloating")
    move = f'hyprctl dispatch movetoworkspacesilent special:img,address:{win["address"]}'
    hyprlibs.exec_or_remind(move)


def save_clipboard_image(path):
    mime_type_out = "wl-paste -l"
    mime_type = hyprlibs.exec_or_remind(mime_type_out)

    if mime_type.find("text") != -1:
        hyprlibs.notify("clipboard is not image")
        return False
    hyprlibs.exec_or_remind(f"wl-paste -t image/png > {path}")
    return True


@app.command()
def show():
    img = gen_image_path()
    clear_tmp_image()

    if not save_clipboard_image(img):
        return

    iw, ih = get_image_size(img)

    show = f'hyprctl dispatch exec "[float;maxsize {iw} {ih};bordersize 2; bordercolor rgba(ffff81ac);opacity 0.9;rounding 0;]" qimgv "{img}"'
    hyprlibs.exec_or_remind(show)
    # import float_window
    # float_window.move("rightup")
    hyprlibs.exec_or_remind(f"python ~/.recipes/hyprland/float_window.py move rightup")
    


@app.command()
def edit(ps: bool = typer.Option(False, "--ps", "-p")):
    img = gen_image_path()
    clear_tmp_image()
    if ps:
        edit = "gimp {img}"
    else:
        edit = "swappy -f {img}"
    if not save_clipboard_image(img):
        return

    hyprlibs.exec_or_remind(edit)


@app.command()
def drun():
    commands = ["edit", "pin", "save", "edit-ps", "hide"]
    command = hyprlibs.choose_in_dmenu(commands)
    if command == "edit":
        edit()
    elif command == "edit-ps":
        edit(ps=True)
    elif command == "pin":
        show()
    elif command == "hide":
        to_workspace()
    elif command == "save":
        save_clipboard_image(gen_image_path(os.path.expanduser("~/6_data/image/")))
        hyprlibs.notify("saved to ~/6_data/image/")


app()
