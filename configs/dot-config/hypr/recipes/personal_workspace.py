import typer
import hyprlibs

personal_workspace_name = "special:personal"
personal_workspace_name_raw = "personal"
# default_app = "/opt/google/chrome/google-chrome --profile-directory=Default --app-id=lhkfonfikbojlapbmofnpdmgfmeoeaoe"
default_app = "dida"
app = typer.Typer()

def get_personal_workspace():
  workspaces = hyprlibs.get_workspaces()
  for ws in workspaces:
    if ws["name"] == personal_workspace_name:
      return ws
  return None

@app.command()
def toggle():
  personal_workspace = get_personal_workspace()
  if not personal_workspace:
    print("personal workspace not found")
    hyprlibs.notify("personal workspace not found, running dida for you")
    hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace {personal_workspace_name}] {default_app}'")
    print(f"hyprctl dispatch exec '[workspace {personal_workspace_name}] {default_app}'")
    
  
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace {personal_workspace_name_raw}")

@app.command()
def move_to():
  hyprlibs.exec_or_remind(f"hyprctl dispatch movetoworkspace {personal_workspace_name}")


app()
