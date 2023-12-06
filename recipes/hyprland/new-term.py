import hyprlibs
import os

cur = hyprlibs.get_current_window()
title = cur.get("title", "")
wclass = cur.get("class", "")
term = '/usr/bin/kitty'

def get_path():
  if "Code" in wclass and ' - ' in title:
    # vscode
    path = title.rsplit('-', 1)[0]
    return path

  return ''
path = get_path()
path = path if path else ''
# os.system(f'{term} {path} ')

os.system(f'cd {path};{term} -e fish -c "zellij -l compact options --on-force-close quit"')
# os.execv(f'{term}', [path])
