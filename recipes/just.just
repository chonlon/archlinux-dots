HELP_PAGE:="https://just.systems/man/zh/"

# open help page in default browser
open-help:
  @echo "Opening help page in default browser"
  @python -mwebbrowser {{HELP_PAGE}} 1>/dev/null 2>&1