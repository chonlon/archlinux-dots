import hyprlibs
import typer

app = typer.Typer()


def alt_scale(delta):
    monitor = hyprlibs.focused_monitor()
    current_scale = monitor["scale"]
    scale = current_scale + float(delta)
    res_hz = f'{monitor["width"]}x{monitor["height"]}@{monitor["refreshRate"]}'
    pos = f'{monitor["x"]}x{monitor["y"]}'
    monitor = monitor["name"]
    

    cmd = f'hyprctl keyword monitor "{monitor},{res_hz},{pos},{scale}"'
    print(cmd)
    hyprlibs.exec_or_remind(cmd)


@app.command()
def add_scale(delta: float = typer.Argument(0.1, help="Scale to add to current scale")):
    alt_scale(delta)


@app.command()
def sub_scale(
    delta: float = typer.Argument(0.1, help="Scale to subtract from current scale")
):
    alt_scale(-delta)

@app.command()
def set_scale(
    scale: float = typer.Argument(1, help="Scale to subtract from current scale")
):
    monitor = hyprlibs.focused_monitor()
    current_scale = monitor["scale"]
    res_hz = f'{monitor["width"]}x{monitor["height"]}@{monitor["refreshRate"]}'
    pos = f'{monitor["x"]}x{monitor["y"]}'
    monitor = monitor["name"]
    

    cmd = f'hyprctl keyword monitor "{monitor},{res_hz},{pos},{scale}"'
    print(cmd)
    hyprlibs.exec_or_remind(cmd)


app()
