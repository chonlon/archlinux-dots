# install a gtk theme, optional but recommended
install-tokyo-night:
    #!/usr/bin/zsh
    cd $HOME/Downloads
    pwd && ls
    git clone https://github.com/Fausto-Korpsvart/Tokyo-Night-GTK-Theme.git
    cd Tokyo-Night-GTK-Theme/
    sudo cp -r themes/Tokyonight-Dark-BL /usr/share/themes/

# picom which currently can't be installed from the AUR
install-picom:
    #!/usr/bin/env zsh
    sudo pacman -S libconfig libev libxdg-basedir pcre pixman xcb-util-image xcb-util-renderutil hicolor-icon-theme libglvnd libx11 libxcb libxext libdbus asciidoc uthash

    cd $HOME/Downloads
    git clone https://github.com/pijulius/picom.git
    cd picom/
    meson --buildtype=release . build --prefix=/usr -Dwith_docs=true
    sudo ninja -C build install

    sudo usermod -aG adm $USER

install-eww:
    #!/usr/bin/zsh
    rustup default nightly

    cd $HOME/Downloads
    git clone https://github.com/elkowar/eww.git
    cd eww
    cargo build --release -j $(nproc)
    cd target/release
    sudo mv eww /usr/bin/eww

    rustup default stable

install-xqp:
    #!/usr/bin/zsh
    cd $HOME/Downloads
    git clone https://github.com/baskerville/xqp.git
    cd xqp
    make
    sudo make install

prepare-bspwm:
    yay -S \
        sxhkd \
        kitty polybar rofi bspwm-rounded-corners-git xdg-user-dirs nautilus xorg \
        pavucontrol blueberry xfce4-power-manager feh lxappearance papirus-icon-theme \
        file-roller gtk-engines gtk-engine-murrine neofetch imagemagick xclip \
        maim gpick curl jq tint2 zsh moreutils recode dunst plank python-xdg redshift \
        mate-polkit xfce4-settings mpv yaru-sound-theme fish alsa-utils slim xorg-xinit \
        brightnessctl acpi mugshot playerctl python-pytz glava wmctrl i3lock-color jgmenu \
        inter-font networkmanager-dmenu-git conky-lua bsp-layout zscroll-git noise-suppression-for-voice \
        starship system76-power lsof gamemode lib32-gamemode xdo bluez bluez-utils bluez-libs bluez-tools

    
    
    sudo systemctl enable NetworkManager
    sudo systemctl start NetworkManager
    sudo systemctl enable bluetooth
    sudo systemctl start bluetooth
    # sudo systemctl enable slim
    # sudo systemctl start slim

    just install-tokyo-night install-picom install-eww install-xqp
