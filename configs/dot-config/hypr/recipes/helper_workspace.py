import typer
import hyprlibs

helper_workspace_name = "special:helper"
helper_workspace_name_raw = "helper"
default_app = "kitty"
app = typer.Typer()

def get_helper_workspace():
  workspaces = hyprlibs.get_workspaces()
  for ws in workspaces:
    if ws["name"] == helper_workspace_name:
      return ws
  return None

@app.command()
def toggle():
  helper_workspace = get_helper_workspace()
  if not helper_workspace:
    print("helper workspace not found")
    hyprlibs.notify("helper workspace not found, running kitty for you")
    hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace {helper_workspace_name}]' {default_app}")
    import time
    # time.sleep(1)
    
  
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace {helper_workspace_name_raw}")

@app.command()
def move_to():
  cur_win = hyprlibs.get_current_window()
  if cur_win['workspace']['name'] == helper_workspace_name:
    cur_workspace = hyprlibs.get_current_workspace()
    hyprlibs.exec_or_remind("hyprctl dispatch movetoworkspace {},address:{}".format(cur_workspace['id'], cur_win['address']))
    toggle()
  else:
    # print(f"hyprctl dispatch movetoworkspace {helper_workspace_name}")
    hyprlibs.exec_or_remind(f"hyprctl dispatch movetoworkspace {helper_workspace_name}")
    toggle()


# move_to()
app()
