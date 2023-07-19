ali-conf := "/home/lon/.kube/ali.config"
huawei-conf := "/home/lon/.kube/huawei.config"

ali-k9s:
	k9s --kubeconfig {{ali-conf}}
ali-helm *args:
	helm --kubeconfig {{ali-conf}} {{args}}
ali-ctl *args:
	kubectl --kubeconfig {{ali-conf}} {{args}}

huawei-k9s:
	k9s --kubeconfig {{huawei-conf}}
[no-cd]
huawei-helm *args:
	helm --kubeconfig {{huawei-conf}} {{args}}

[no-cd]
huawei-ctl *args:
	kubectl --kubeconfig {{huawei-conf}} {{args}}


