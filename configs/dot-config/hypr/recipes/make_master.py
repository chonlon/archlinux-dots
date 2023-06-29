import typer
import hyprlibs

app = typer.Typer()



def main(
  win_id: str = typer.Argument("", help="Window id to focus or create"),
):
  pass