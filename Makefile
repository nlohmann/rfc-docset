all:
	@echo "download:        download RFCs (best using several jobs with '-j10')"
	@echo "rfc.docset       create the docset"
	@echo "rfc.docset.tgz   create compressed docset for docset feed"


clean:
	rm -fr rfc.docset rfc.docset.tgz

##############################################################################
# targets to download HTML versions of the RFCs
##############################################################################

download:
	mkdir -p html
	$(MAKE) $(shell seq -f "html/rfc%g.html" 1 9000)
	$(MAKE) $(shell seq -f "html/bcp%g.html" 1 300)
	find html -size 0 -delete

html/%:
	-wget -q https://tools.ietf.org/$@ --output-document=$@


##############################################################################
# target to create the docset
##############################################################################

rfc.docset:
	rm -fr rfc.docset
	python create_docset.py

rfc.docset.tgz: rfc.docset
	tar --exclude='.DS_Store' --options 'gzip:compression-level=9' -cvzf rfc.docset.tgz rfc.docset
