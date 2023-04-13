
install-z4h:
    #!/usr/bin/env bash
    if command -v curl >/dev/null 2>&1; then
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"
    else
        sh -c "$(wget -O- https://raw.githubusercontent.com/romkatv/zsh4humans/v5/install)"
    fi

install-plugins:
    #!/usr/bin/env zsh
    git clone https://github.com/sukkaw/zsh-proxy.git $ZSH_CUSTOM/plugins/zsh-proxy
    git clone https://github.com/paulirish/git-open.git $ZSH_CUSTOM/plugins/git-open
    

echo:
    @echo "zsh4humans installed."

install: install-z4h install-plugins echo
    