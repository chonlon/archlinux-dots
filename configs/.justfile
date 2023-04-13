init-softlink:
    # ln -s $PWD/.xinitrc $HOME/.xinitrc
    # ln -s $PWD/.Xresources $HOME/.Xresources
    # ln -s $PWD/.xprofile $HOME/.xprofile
    ln -s $PWD/.z4hrc $HOME/.zshrc

    ln -s $PWD/dot-config $HOME/.config

switch-to-bspwm:
    @ mkdir -p $HOME/.local/
    @ mkdir -p $HOME/.scripts/
    @ mkdir -p $HOME/.cache/
    cp -r $PWD/dot-local/bspwm-local/* $HOME/.local
    cp -r $PWD/dot-scripts/bspwm-scripts/* $HOME/.scripts
    cp -r $PWD/dot-cache/bspwm-cache $HOME/.cache

    cp $PWD/.bspwm-xinitrc .xinitrc
    cp $PWD/.bspwm-gtkrc-2.0 .gtkrc-2.0

    sudo cp $PWD/etc/bspwm/slim.conf $PWD/etc/bspwm/environment /etc/
    sudo cp $PWD/usr/bspwm/* /usr/ -r
