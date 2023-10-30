import typer
from typing import Optional

app = typer.Typer()

@app.command()
def recipe(env: str, env2: str):
  print(env, env2)
  
@app.command()
def r2(env: str):
  print(env)

app()