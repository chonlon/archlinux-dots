alias jj="python $HOME/.recipes/entry.py"
alias jw="jj workflow "
alias jk="jj k8s "
alias jd="jj dockers "
alias jg="jj git "


# complete -c jj -f -a "k8s k3s dockers git workflow"
complete -c jd -f -a "alist-password alist-start alist-stop apps frp-restart frp-start frp-stop_inner syncthing-start syncthing-stop"
complete -c jk -f -a "prod-k9s set-dev set-prod set-test test-k9s"
complete -c jg -f -a "remote-open worktree-add worktree-remove"
complete -c jw -f -a "achieve_all_files achieve_file achieve_folder clone_test create_test help"