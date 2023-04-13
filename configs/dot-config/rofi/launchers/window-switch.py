import os
import sys

# dir="$HOME/.config/rofi/launchers/"
home = os.path.expanduser('~/.config/rofi/launchers/')
theme='style-5'

## Run
"""
echo -e "a\nb\nc" | rofi \
    -dmenu \
    -theme ${dir}/${theme}.rasi
"""

