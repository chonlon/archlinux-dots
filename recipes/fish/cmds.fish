set -x PATH $PATH $HOME/.local/bin

# Define aliases.
alias l='exa -lah'
alias ll='exa -lah'
alias c=clear
alias tree='tree -a -I .git'
alias dr='docker run --rm -it -v share_data:/root/data/ -v /mnt:/mnt'
alias db='docker build'
alias lls='logo-ls'
alias ls="exa --icons"
alias vi="nvim"
alias grep="rg"
alias du="dust"
alias ra="ranger"
alias rv="EDITOR=nvim ranger"
alias d=dolphin
alias g=gitui
alias ht="http"
alias cp="fcp"
alias hd="atuin search -i --filter-mode directory"
alias lzd="lazydocker"
alias k="k9s"
alias kc="kubectl"

function copy
    set -l dirn
    if test -z "$argv"
        set dirn (pwd)
    else
        set dirn (realpath $argv[1])
    end
    wl-copy $dirn
    echo "copied '$dirn' to clipboard"
end

function rga-fzf
    set -l RG_PREFIX "rga --files-with-matches"
    set -l file (env FZF_DEFAULT_COMMAND="$RG_PREFIX '$argv'" fzf --sort --preview='[[ ! -z {} ]] and rga --pretty --context 5 {q} {}' --phony -q "$argv" --bind 'change:reload:$RG_PREFIX {q}' --preview-window='70%:wrap')

    if test -n "$file"
        echo "opening $file"
        xdg-open "$file"
    else
        echo "No file selected"
    end
end

#######################
# docker
#######################

function de
    # docker exec
    # fzf select live container and open shell in it
    set container_desc (docker ps | awk '{print $1" "$2" "$4" "$5" "$6" "$10}' | sed '1d' | fzf)
    if test -z "$container_desc"
        return 0
    end

    set container_id (echo $container_desc | awk '{print $1}')
    # test if container has bash
    if test -z (docker exec $container_id which bash)
        docker exec -it $container_id sh
    else
        docker exec -it $container_id bash
    end
end

#########################
# git
#########################

function gw
    set dirnamev (git worktree list | awk '{print $1}' | fzf)
    if test -z $dirnamev
        return 0
    end
    cd $dirnamev
end

function cgw
    # create git worktree
    if test -z "$argv[1]"
        echo "Usage: cgw <branch> [<dir>]"
        return
    end

    if test -z "$GIT_WORKTREE_DIR"
        echo "GIT_WORKTREE_DIR is not set"
        return
    end

    set branch_name $argv[1]

    if test -z "$argv[2]"
        # get current repo name
        set repo_name (basename (git rev-parse --show-toplevel))

        set dirname "$GIT_WORKTREE_DIR/$repo_name/$branch_name"
        if test -d "$dirname"
            echo "Directory $dirname already exists"
            return
        end
    else
        set dirname "$argv[2]"
    end

    git worktree add "$dirname" "$branch_name"
end

complete -c cgw -f -a "(git branch | sed 's/ //g' | sed 's/*//g')"
