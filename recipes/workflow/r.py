import typer

from pathlib import Path
import sys

sys.path.append("/home/lon/.recipes/")
import utils

app = typer.Typer()

focus_folder = Path.home() / "2_focus"
test_folder = Path.home() / "4_test"
achieved_folder = Path.home() / "6_data"


@app.command()
def help():
    help_text = f"""
  focus is folder for focus at {focus_folder}
  test is folder for test at {test_folder}
  achieve is folder for achieved data at {achieved_folder}
  """
    print(help_text)


def process_exists(target: Path) -> str:    
    import datetime

    if Path(target).exists():
        typer.confirm(f"{target} exists, continue?", default=True)
        target_name = typer.prompt("new target name, left empty for auto", default="")
        if target_name == "":
            target_name = (
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + target.name
            )
        target = target.absolute().parent / target_name

    return target


@app.command()
def achieve_folder(
    src_folder: str = typer.Argument(default=".", help="achieve folder"),
):
    src_folder: Path = Path(src_folder)
    if not src_folder.exists():
        raise RuntimeError(f"folder {src_folder} not exists")
    target_prefix = typer.prompt("target prefix", default="")

    target_folder = (
        achieved_folder / target_prefix if target_prefix != "" else achieved_folder
    )
    target_folder = process_exists(target_folder)

    confirm = typer.confirm(
        f"move {src_folder.absolute()} to {target_folder}", default=True
    )
    if confirm:
        if not target_folder.exists():
            utils.run_or_exit(f"mkdir -p {target_folder}")

        utils.run_or_exit(f"mv {src_folder} {target_folder}")
    notes = typer.prompt("notes", default="")
    notes = f"tag:: #[[achieve folder]]\nachieve [{src_folder.name}](file://{target_folder.absolute()/src_folder.name})\n----\n{notes}"
    utils.add_node(notes)
    print(f'Achieve folder "{target_folder}/{src_folder.name}"')


def achieve_files(
    src_files=typer.Argument(..., help="achieve file"),
):
    map_file = {
        "png": "image",
        "jpg": "image",
        "jpeg": "image",
        "gif": "image",
        "mp4": "video",
        "mkv": "video",
        "avi": "video",
        "pdf": "doc",
        "txt": "doc",
        "md": "doc",
        "html": "doc",
        "doc": "word",
        "docx": "word",
        "ppt": "ppt",
        "pptx": "ppt",
        "xls": "excel",
        "xlsx": "excel",
        "zip": "packed",
        "rar": "packed",
        "7z": "packed",
        "gz": "packed",
        "tar": "packed",
        "bz2": "packed",
        "iso": "packed",
        "json": "code",
        "yaml": "code",
        "stl": "3d",
        "step": "3d",
        "obj": "3d",
        "exe": "app/win",
        "apk": "app/android",
    }
    achieved_file = []
    achieved_file_str = ""
    confirm = typer.confirm(
        f"move {src_files} to {achieved_folder}", default=True, abort=True
    )

    def achieve_one(src_file):
        src_file: Path = Path(src_file)
        if not src_file.exists():
            raise RuntimeError(f"file {src_file} not exists")

        target_prefix = map_file.get(src_file.suffix[1:].lower(), "other")

        target_folder = (
            achieved_folder / target_prefix if target_prefix != "" else achieved_folder
        )
        target_file = target_folder / src_file.name
        target_file = process_exists(target_file)

        if confirm:
            if not target_folder.exists():
                utils.run_or_exit(f"mkdir -p {target_folder}")

        utils.run_or_exit(f"mv '{src_file}' '{target_file}'")
        achieved_file.append(src_file)
        return f"\n[{src_file.name}](file://{target_file})"

    for src_file in src_files:
        achieved_file_str += achieve_one(src_file)

    notes = typer.prompt("notes", default="")

    notes = f"tag:: #[[achieve folder]]\n{achieved_file_str}\n----\n{notes}"
    utils.add_node(notes)


@app.command()
def achieve_file(src_files: str = typer.Argument(..., help="achieve file")):
    achieve_files([src_files])


@app.command()
def achieve_all_files(
    src_folder: str = typer.Argument(default=".", help="achieve file")
):
    src_folder: Path = Path(src_folder)
    if not src_folder.exists():
        raise RuntimeError(f"folder {src_folder} not exists")
    files = [str(f) for f in src_folder.iterdir()]
    achieve_files(files)


@app.command()
def clone_test(repo: str = typer.Argument(default="", help="repo to clone")):
    if repo.strip() == "":
        repo = typer.prompt("repo", default="")
    notes = typer.prompt("notes", default="")
    notes = f"tag:: #[[test folder]]\nadded [{repo}](file://{test_folder}/{repo})\n{notes}"
    utils.add_node(notes)
    utils.run_or_exit(f"cd {test_folder} && git clone {repo}")
    print("folder copied to clipboard")
    utils.to_clipboard(f"{test_folder}/{repo.split('/')[-1]}")


@app.command()
def create_test(test_name: str = typer.Argument(default="", help="test name")):
    if test_name.strip() == "":
        test_name = typer.prompt("test name", default="")
    notes = typer.prompt("notes", default="")
    notes = f"tag:: #[[test folder]]\nadded [{test_name}](file://{test_folder}/{test_name})\n{notes}"
    utils.add_node(notes)
    utils.run_or_exit(f"cd {test_folder} && mkdir {test_name}")
    print("folder copied to clipboard")
    utils.to_clipboard(f"{test_folder}/{test_name}")


app()
