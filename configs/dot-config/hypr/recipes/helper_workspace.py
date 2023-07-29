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
  personal_workspace = get_helper_workspace()
  if not personal_workspace:
    print("personal workspace not found")
    hyprlibs.notify("personal workspace not found, running kitty for you")
    hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace {helper_workspace_name}]' {default_app}")
    import time
    time.sleep(1)
    
  
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace {helper_workspace_name_raw}")

@app.command()
def move_to():
  print(f"hyprctl dispatch movetoworkspace {helper_workspace_name}")
  hyprlibs.exec_or_remind(f"hyprctl dispatch movetoworkspace {helper_workspace_name}")


# move_to()
app()