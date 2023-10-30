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
def install_k3s():
  pass

app()