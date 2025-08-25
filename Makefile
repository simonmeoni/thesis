clean: 
	latexmk -C

sync: 
	latexmk -C
	latexmk -pdf -pvc
