note_dir := '/home/lon/3_lon/notes'

pull:
  cd {{note_dir}} && git pull

push:
  cd {{note_dir}} && git push

code:
  cd {{note_dir}} && code .

