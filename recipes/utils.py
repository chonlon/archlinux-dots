import subprocess
import yaml
import pathlib
from rich import print
from sys import exit
import os


def run_command(command):
    """
    if command is a string, it will be split by space

    if command is failed, stdout and stderr will be printed and raise an error

    """

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(e)
        print(e.stdout)
        print(e.stderr)
        if "SyntaxError" in e.stderr:
            raise SyntaxError("Command contains syntax errors")
        else:
            raise RuntimeError("Command failed to execute")


def run_or_exit(command):
    try:
        output = run_command(command)
        print(output)
    except SyntaxError as e:
        print(":x: [bold red]Command failed, exit[/bold red]")
        print(f"command: {command}, output and error printed above")
        exit(-1)
    except RuntimeError as e:
        print(":x: [bold red]Command failed, exit[/bold red]")
        print(f"command: {command}, output and error printed above")
        exit(-1)
    except Exception as e:
        print(
            f":warning: [bold yellow]Command returned with some exception: {e} [/bold yellow]"
        )
        exit(-1)


def has_cmd(cmd: str):
    has = os.system(f"command -v {cmd} > /dev/null")
    return has == 0


def get_cmd(cmd: str):
    """
    get cmd path
    """
    if has_cmd(cmd):
        return cmd
    elif has_cmd(f"/usr/local/bin/{cmd}"):
        return f"/usr/local/bin/{cmd}"
    else:
        raise RuntimeError(f"command {cmd} not found")


def write_dict_to_yaml(dict, path):
    """
    write dict to yaml file
    """
    import yaml

    with open(path, "w") as f:
        yaml.dump(dict, f)


def write_str_to_file(str, path):
    """
    write str to file, try decode str to utf-8 and process \n
    """
    with open(path, "w") as f:
        f.write(str)


def merge_dicts(d1, d2):
    merged = d1.copy()

    for key, value in d2.items():
        if key in merged:
            if isinstance(merged[key], list) and isinstance(value, list):
                merged[key].extend(value)
            elif isinstance(merged[key], dict) and isinstance(value, dict):
                merged[key] = merge_dicts(merged[key], value)
            else:
                merged[key] = value
        else:
            merged[key] = value

    return merged


def is_deep_key_empty(data, key_path):
    keys = key_path.split(".")
    for key in keys:
        if key in data:
            data = data[key]
        else:
            return False
    return True


def load_build_config(path: pathlib.Path):
    """
    load build config
    """
    if not path.exists():
        raise RuntimeError(f"build config directory {path.absolute()} not found")
    print(path)
    print("config files: ")
    configs = {}
    for config_file in path.iterdir():
        print(config_file, end=" ")
        with open(config_file, "r") as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            if config is None:
                continue

            configs = merge_dicts(configs, config)
    print()
    print("config loaded: ")
    print(configs)
    return configs


def check_apps():
    apps = ["kubectl", "helm"]
    # check apps exists
    for app in apps:
        rst = os.system("which " + app)
        if rst != 0:
            print(f"[bold red]{app} not found[/bold red]")
            raise RuntimeError(f"[Check app]: {app} not found")
    return


def is_empty(istr):
    """
    check istr is none or all space or with \n \t
    """
    if istr is None:
        return True
    if isinstance(istr, str) and istr.strip() == "":
        return True
    return False


def choose_in_options(options: list, cmd="fzf"):
    options = [str(o) for o in options]
    options = "\n".join(options)
    options = options.encode("utf-8")
    if is_empty(options):
        return None
    proc = subprocess.run(
        [cmd],
        input=options,
        shell=False,
        stdout=subprocess.PIPE,
    )
    out = proc.stdout.decode("utf-8").strip()

    return out


def to_clipboard(text):
    """
    copy text to clipboard
    """
    cmd = f'wl-copy "{text}"'
    run_or_exit(cmd)


def add_logseq_note(note):
    import json

    method = "logseq.Editor.appendBlockInPage"
    date = run_command("date +%Y-%m-%d")
    data = {"method": method, "args": [date, note]}
    data = json.dumps(data)
    cmd = f"echo '{data}' | http post :12315/api Authorization:'Bearer '"
    run_or_exit(cmd)
    print(f'added note to {date}')


def add_node(note):
    add_logseq_note(note)
