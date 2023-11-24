starship init fish | source
zoxide init fish | source
source ~/.config/fish/autin.fish
# atuin init fish | source

string match -q "$TERM_PROGRAM" "vscode"
and . (code --locate-shell-integration-path fish)