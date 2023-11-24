# cur swap to master.
# if cur is master, swap with last window in workspace.

import hyprlibs
import time
cur = hyprlibs.get_current_window()
hyprlibs.exec_or_remind("hyprctl dispatch layoutmsg swapwithmaster master")