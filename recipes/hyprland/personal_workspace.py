import typer

import hyprlibs
print(hyprlibs.get_config())
workspace = hyprlibs.get_config()["workspace"]

app = typer.Typer()

def get_workspace(name):
  workspaces = hyprlibs.get_workspaces()
  print(name)
  print(workspaces)
  for ws in workspaces:
    if ws["name"] == name or ws["name"] == 'name:' + name or ws["name"] == 'special:' + name:
      return ws
  return None

@app.command()
def toggle(name: str):
  personal_workspace = get_workspace(name)
  if not personal_workspace:
    print("personal workspace not found")
    hyprlibs.notify("workspace not found, running app for you")
    default_app = workspace[f"name:{name}"]["app"]
    hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace name:{name}] {default_app}'")
    print(f"hyprctl dispatch exec '[workspace name:{name}] {default_app}'")
    
  hyprlibs.exec_or_remind(f"hyprctl dispatch workspace name:{name}")

@app.command()
def toggle_helper(name: str):
  personal_workspace = get_workspace(name)
  create = True
  if not personal_workspace:
    create = True
  else:
    apps = hyprlibs.get_windows()
    for _app in apps:
      if _app["workspace"]["name"] == f"special:{name}":
        create = False
  if create:
    default_app = workspace[f"special:{name}"]["app"]
    hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace special:{name}] {default_app}'")
  # hyprlibs.exec_or_remind(f"hyprctl dispatch exec '[workspace special:{name}] kitty'")
  # cur_workspace = hyprlibs.get_current_workspace()
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace {name}")
  # if "special" in cur_workspace["name"]:
  #   hyprlibs.exec_or_remind(f"hyprctl dispatch submap reset")
  # else:
  #   hyprlibs.exec_or_remind(f"hyprctl dispatch submap special")
  
  



# @app.command()
# def move_to():
#   hyprlibs.exec_or_remind(f"hyprctl dispatch movetoworkspace {personal_workspace_name}")

@app.command()
def switch():
  w = hyprlibs.choose_in_dmenu([name.replace('name:', '') for name in workspace.keys()], "choose workspace")
  
  print(f"choosen {w}")
  if w and len(w):
    toggle(w)

@app.command()
def exit_special_workspace():
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace exit")
  hyprlibs.exec_or_remind(f"hyprctl dispatch togglespecialworkspace exit")
  hyprlibs.exec_or_remind(f"hyprctl dispatch submap reset")


app()