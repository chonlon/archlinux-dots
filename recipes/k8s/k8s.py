import typer
import os
from typing import Annotated, Optional

app = typer.Typer()
map = {
    "curl": "quay.io/curl/curl:latest",
    "alpine": "alpine",
    "network": "rancher/network-manager:v0.7.22",
    "ubuntu": "ubuntu:22.04",
    "debian": "debian",
    "utils": "arunvelsriram/utils",
}


def get_image(name):
    image = map.get(name, "")
    if len(image) == 0:
        print("valaid names is: ", " ".join(map.keys()))
    return image


@app.command()
def pod_debug(name):
    image = get_image(name)
    yaml_file = "debug-template.yaml"
    with open(yaml_file, "r") as file:
        data = file.read()

    data = data.replace("__NAME__", name)
    data = data.replace("__IMAGE__", image)

    with open("pod.yaml", "w") as file:
        file.write(data)
    os.system("kubectl apply -f pod.yaml")
    os.system("rm pod.yaml")


@app.command()
def attach_debug(
    name: str,
    target: Optional[str] = typer.Option(
        None,
        "--target",
        "-t",
        help="target container name, left empty to choose one",
    ),
    namespace: Optional[str] = typer.Option(
        None,
        "--namespace",
        "-n",
        help="namespace, left empty will find in all namespaces",
    ),
):
    image = get_image(name)
    if namespace is None or len(namespace) == 0:
        namespace = ""
    else:
        namespace = f"-n {namespace}"
    if target is None or len(target) == 0:
      cmd = """
      kubectl get pods --template='{{{{range .items}}}}{{{{.metadata.name}}}}{{{{"\\n"}}}}{{{{end}}}}' {namespace} | fzf
      """.format(
          namespace=namespace
      )
      pod = os.popen(cmd).read().strip()
      if len(pod) == 0:
          print("no pod choosen, exit")
          return
    else:
      pod = f"{target}"
    print("debug pod: ", pod)
    cmd = f"kubectl debug -it {pod} --image {image} {namespace}"

    print("run: ", cmd)
    os.system(cmd)


@app.command()
def exec_pod(name):
    image = get_image(name)
    cmd = f"kubectl run --rm {name} -it --image {image} sh -n test"
    os.system(cmd)


app()
