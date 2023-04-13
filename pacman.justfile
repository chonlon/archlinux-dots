# Archlinuxcn
init:
    # if no archlinuxcn found in pacman.conf, add it.
    if ! grep -q "archlinuxcn" /etc/pacman.conf; then \
        printf "\n\n[archlinuxcn]\nServer = https://repo.archlinuxcn.org/\$arch" | sudo tee -a /etc/pacman.conf; \
    fi
    sudo pacman -Syyu
    sudo pacman -S yay
    yay -S archlinuxcn-keyring

