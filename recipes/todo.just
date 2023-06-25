todo := "/home/lon/.todo"

edit:
	subl {{todo}}

e: edit

clear:
	rm {{todo}} && touch {{todo}}

c: clear
