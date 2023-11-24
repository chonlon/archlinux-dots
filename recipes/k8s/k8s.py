import typer
import os
app = typer.Typer()
map = {
        "curl": "curl",
        "alpine": "alpine",
        "network": "rancher/network-manager:v0.7.22",
        "ubuntu": "ubuntu:22.04",
        "debian": "debian",
        "utils": "arunvelsriram/utils"
    }

def get_image(name):
  image = map.get(name, '')
  if len(image) == 0:
    print("valaid names is: ", " ".join(map.keys()))
  return image
@app.command()
def pod_debug(name):
    
    image = get_image(name)
    yaml_file = "debug-template.yaml"
    with open(yaml_file, 'r') as file:
        data = file.read()
    
    data = data.replace('__NAME__', name)
    data = data.replace('__IMAGE__', image)

    with open('pod.yaml', 'w') as file:
        file.write(data)
    os.system("kubectl apply -f pod.yaml")
    os.system("rm pod.yaml")

@app.command()
def exec_pod(name):
  image = get_image(name)
  cmd = f'kubectl run --rm utils -it --image {image} bash -n test'
  os.system(cmd)

app()