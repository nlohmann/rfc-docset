all: $(shell seq -f "rfc%g.html" 1 9000)

rfc%:
	-wget -q https://tools.ietf.org/html/$@
