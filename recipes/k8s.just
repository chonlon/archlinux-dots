ali-conf := "/home/lon/.kube/ali.config"

ali-k9s:
	k9s --kubeconfig {{ali-conf}}
ali-helm *args:
	helm --kubeconfig {{ali-conf}} {{args}}
ali-ctl *args:
	kubectl --kubeconfig {{ali-conf}} {{args}}
