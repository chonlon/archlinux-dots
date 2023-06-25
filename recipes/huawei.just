co *arg:
	@ ssh -i $HOME/.ssh/KeyPair-7a53.pem root@139.9.201.82 {{arg}}
cp *arg:
	@ scp -i $HOME/.ssh/KeyPair-7a53.pem {{arg}} root@139.9.201.82
