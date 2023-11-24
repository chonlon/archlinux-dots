import typer
import os
from typing import List

args = os.sys.argv


def helm(conf: str, args: List[str]):
    args = [x for x in args if x != ""]  # convert to list and remove empty string

    if len(args) == 0:
        # ask for input
        args = typer.prompt("input helm args").split(" ")

    if args[0] == "helm":
        args = args[1:]

    cmd = f'helm --kubeconfig {conf} {" ".join(args)}'
    print("run for cmd:", cmd)
    os.system(cmd)


def ctl(conf: str, args: List[str]):
    args = [x for x in args if x != ""]  # convert to list and remove empty string

    if len(args) == 0:
        # ask for input
        args = typer.prompt("input kubectl args").split(" ")

    if args[0] == "kubectl":
        args = args[1:]

    cmd = f'kubectl --kubeconfig {conf} {" ".join(args)}'
    print("run for cmd:", cmd)
    os.system(cmd)
    
run = args[1]
conf = args[2]
args = args[3:]

if run == 'helm':
    helm(conf, args)
if run == 'ctl':
    ctl(conf, args)