import hyprlibs
import typer
from sys import argv as args

app = typer.Typer()

def main(
  dest_workspace: int = typer.Argument(-1, help="Workspace to move window to")
):
  cur_win = hyprlibs.get_current_window()
  if dest_workspace == -1:
    dest_workspace = 9
    config = hyprlibs.get_config()
    target_rules = config["window"]["target_rules"]
    for rule in target_rules:
      if hyprlibs.is_window_match(cur_win, rule):
        dest_workspace = rule["workspace"]
        break
  print("moving: {}-{}".format(cur_win["address"], cur_win["title"]))
  cur_win = cur_win["address"]
  hyprlibs.exec_or_remind("hyprctl dispatch movetoworkspacesilent {},address:{}".format(dest_workspace, cur_win))
  # refocus to biggest window in current workspace  
  # cur_workspace = hyprlibs.get_current_workspace(0)["id"]
  # biggest_win = hyprlibs.biggest_window_in_workspace(cur_workspace["id"])
  # hyprlibs.exec_or_remind("hyprctl dispatch focuswindow address:{}".format(biggest_win["address"]))
  hyprlibs.exec_or_remind("hyprctl dispatch cyclenext")


if __name__ == "__main__":
  typer.run(main)