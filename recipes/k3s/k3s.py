import os
import typer

app = typer.Typer()

@app.command(
    "uninstall-k3s",
    help="Uninstall k3s, Please make sure you really want to do this cause this will remove all your k8s data, not be able to recover.",
)
@app.command("uk3", help="alias of uninstall-k3s")
def uninstall_k3s():
    print("[bold red]Uninstalling k3s[/bold red]")

    user_op = typer.prompt("Are you sure to uninstall k3s? [Y/n]", default="n")
    if user_op.lower() != "y":
        print("[bold red]User canceled[/bold red]")
        return

    rst = os.system("/usr/local/bin/k3s-uninstall.sh")
    if rst != 0:
        print("[bold red]Error uninstalling k3s[/bold red]")
        return

    print("[bold green]k3s uninstalled[/bold green]")

@app.command("install")
def install_k3s(cilium=False):
  extra = 'INSTALL_K3S_VERSION="v1.26.10+k3s1" '
  exec_extra = ' INSTALL_K3S_EXEC="--write-kubeconfig-mode=644 --prefer-bundled-bin'
  if cilium:
      exec_extra += ' --disable-network-policy --flannel-backend none '
  exec_extra += '" '
  extra += exec_extra
  cmd = f"curl -sfL https://rancher-mirror.rancher.cn/k3s/k3s-install.sh | {extra} INSTALL_K3S_MIRROR=cn sh -"
  print("running cmd: ", cmd)
  os.system(cmd)
  os.system("sudo k3s kubectl config view --raw > ~/.kube/dev.config")
  os.system("sudo chown lon ~/.kube/dev.config")
  if cilium:
      os.system("cilium install")
      os.system("cilium hubble enable --ui")
      print("using cilium hubble ui to view it in web")
app()
