import hyprlibs
import typer
from sys import argv as args

app = typer.Typer()

def main(
  dest_workspace: int = typer.Argument(9, help="Workspace to move window to")
):  
  cur_win = hyprlibs.get_current_window()["address"]
  hyprlibs.exec_or_remind("hyprctl dispatch movetoworkspacesilent {},address:{}".format(dest_workspace, cur_win))
  # refocus to biggest window in current workspace  
  cur_workspace = hyprlibs.get_current_workspace(0)["id"]
  biggest_win = hyprlibs.biggest_window_in_workspace(cur_workspace["id"])
  hyprlibs.exec_or_remind("hyprctl dispatch focuswindow address:{}".format(biggest_win["address"]))


if __name__ == "__main__":
  typer.run(main)