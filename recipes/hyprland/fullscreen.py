import hyprlibs

cur = hyprlibs.get_current_window()
windows = hyprlibs.get_windows()
cur_ws = hyprlibs.get_current_workspace()
cur_ws_id = cur_ws["id"]
count = 0
    
for win in windows:
    if win["workspace"]["id"] == cur_ws_id:
      if win.get("floating", False) == False:
        count = count + 1

def get_config_from():
    import os
    import json
    """
    {"fullscreen": [{"address":"", "origian_workspace":""}]}
    """
    config_path = os.path.join("/tmp", "hypr", "runtime.json")
    try:
      with open(config_path) as f:
          config = json.load(f)
    except:
      return None
    return config


  
def write_config_to(config_fullscreen, config):
    import os
    import json
    config_path = os.path.join("/tmp", "hypr", "runtime.json")
    config = config if config else {}
    config["fullscreen"] = config_fullscreen
    with open(config_path, "w") as f:
        json.dump(config, f)
    

config = get_config_from()

fullscreens = config["fullscreen"] if config else []
for full in fullscreens:
  if full["address"] == cur["address"]:
    hyprlibs.exec_or_remind(f'hyprctl dispatch movetoworkspace {full["origian_workspace"]},address:{ cur["address"]}')
    hyprlibs.exec_or_remind(f'hyprctl dispatch cyclenext')
    fullscreens.remove(full)
    write_config_to(fullscreens, config)
    exit(0)
if count <= 1:
  exit(0)
print(count)
full = {"address": cur["address"], "origian_workspace": cur_ws["name"]}
fullscreens.append(full)
hyprlibs.exec_or_remind("hyprctl dispatch workspace empty")
cur_ws = hyprlibs.get_current_workspace()
hyprlibs.exec_or_remind(f'hyprctl dispatch movetoworkspace {cur_ws["id"]},address:{ cur["address"] }')
write_config_to(fullscreens,config)
