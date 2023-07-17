import os
import subprocess


# paste = subprocess.run(["xclip", "-o", "-selection", "clipboard"], capture_output=True)
paste = "wl-paste -t image/png > /tmp/clipboard.png"

show = "qimgv /tmp/clipboard.png"

os.system(paste)
subprocess.run(show.split(" "))