let zoxide_completer = {|spans|
    $spans | skip 1 | zoxide query -l $in | lines | where {|x| $x != $env.PWD}
}

{
    z: $zoxide_completer
    zi: $zoxide_completer
}