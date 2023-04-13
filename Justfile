
install-fonts:
    yay -S noto-fonts-extra noto-fonts-emoji noto-fonts-cjk noto-fonts nerd-fonts-jetbrains-mono nerd-fonts-ibm-plex-mono nerd-fonts-fira-code ttf-sarasa-gothic nerd-fonts-dejavu-sans-mono ttf-symbola

install-base-packages:
    sudo yay -S \
        base-devel git wget curl unzip zip tar gcc cmake make xmake \
        python python-pip \
        nvm \
        go \
        rustup \
        jetbrains-toolbox \
        visual-studio-code-bin sublime-text-4 \
        neovim zsh broot feh \
        alacritty kitty \
        openssh \
        zellij ranger ripgrep ripgrep-all btop htop fd zoxide wget bat exa lsd logo-ls \
        httpie curlie docker gdb \
        fcitx-sogoupinyin fcitx-configtool fcitx-qt5 \
        google-chrome rofi clash-for-windows-bin copyq \
        flameshot marktext \
        sddm \

    pacman -S amd-ucode # AMD CPU
    # pacman -S intel-ucode # Intel CPU

prepare-node:
    # echo 'source /usr/share/nvm/init-nvm.sh' >> ~/.zshrc
    nvm install --lts
    nvm use --lts
    npm install -g yarn pnpm

prepare-rust:
    rustup install stable
    rustup install nightly
    rustup default stable

prepare-cpp:
    pip install conan

prepare-ssh:
    ssh-keygen

prepare-locale:
    sed -i 's/#en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/g' /etc/locale.gen
    sed -i 's/#zh_CN.UTF-8 UTF-8/zh_CN.UTF-8 UTF-8/g' /etc/locale.gen
    locale-gen

prepare-docker:
    -sudo groupadd docker
    sudo systemctl enable docker
    sudo systemctl start docker
    sudo usermod -aG docker $USER
    @ echo "please logout and login again to make docker work."

prepare-common:
    just -f pacman.justfile
    just -f zsh.justfile install
    cd configs && just init-softlink
    just install-base-packages prepare-node prepare-rust prepare-cpp prepare-ssh prepare-docker

prepare-kde: prepare-common
    yay -S \
        layan-kde-git \
        sweet-kde-git \
        kin-bismuth-bin \
        plasma-meta kate
    

prepare-gnome: prepare-common
    yay -S gnome gnome-extra


prepare-bspwm: prepare-common
    just -f bspwm.justfile prepare-bspwm