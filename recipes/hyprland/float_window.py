import typer

# import os
# import uvloop
import hyprlibs
import hyprland
import asyncio
from asyncio import run


app = typer.Typer()


@app.command()
def float():
    run(hyprland.Dispatch.toggle_floating())
    run(hyprland.Dispatch.pin())
    cur = hyprlibs.get_current_window()
    if cur["floating"]:
      move('right_down')


@app.command()
def focus_float():
    wins = hyprlibs.get_windows_cur_workspace()
    fwins = []
    for win in wins:
        if win["floating"] and len(win["title"]):
            fwins.append(win)
    cur = hyprlibs.get_current_window()
    idx = -1
    for _idx, win in enumerate(fwins):
        if win["address"] == cur["address"]:
            idx = _idx

    flen = len(fwins)
    if flen == 0:
      return
    idx = (idx + 1) % flen
    w = fwins[idx]
    print("focus: ", w["title"])

    run(hyprland.Dispatch.focus_window(f'address:{w["address"]}'))


@app.command()
def focus_tile():
  async def roo():
    wins = hyprlibs.get_windows_cur_workspace()
    nfwins = []
    for win in wins:
        if not win["floating"]:
            nfwins.append(win)
    cur = hyprlibs.get_current_window()
    idx = -1
    for _idx, win in enumerate(nfwins):
        if win["address"] == cur["address"]:
            idx = _idx

    flen = len(nfwins)
    idx = (idx + 1) % flen
    w = nfwins[idx]
    print("focus: ", w["title"])

    await hyprland.Dispatch.focus_window(f'address:{w["address"]}')
  run(roo())



@app.command()
def move(direction: str):
  async def roo():
    cur_win = hyprlibs.get_current_window()
    fm = hyprlibs.focused_monitor()
    (size_w, size_h) = cur_win["size"]
    scale = fm["scale"]
    (mw, mh) = [
        fm["width"] / scale,
        fm["height"] / scale,
    ]
    (tx,ty) = cur_win["at"]
    
    m_top = 60
    m_bottom = 90
    m_x = 30
    
    if size_h < 300:
      size_h = min((mh - 60) / 2, size_h)
    if 'left' in direction:
      tx = m_x
    if 'right' in direction:
      tx = mw - size_w - m_x
    if 'up' in direction:
      ty = m_top
    if 'down' in direction:
      ty = mh - m_bottom - size_h
    print(f"{size_w} {size_h} {tx} {ty}")
    await hyprland.Dispatch.resize_active(f"exact {int(size_w)}", f"{int(size_h)}")
    await hyprland.Dispatch.move_active(f"exact {int(tx)}", f"{int(ty)}")
  run(roo())

# @app.command()
# app()

# async def run():
#   await asyncio.sleep(1)
#   await float()
#   await move('up')

# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app()
# asyncio.run(app())
