PROG=./pagebuild.sh
BASICS=footer.html header.html navigation.html
PAGES=index.html crashkurs.html leitfaden.html abschlussarbeiten.html oral_examination.html

all: $(PAGES)

%.html: content_%.html $(BASICS)
	$(PROG) $< $@
	tidy -q $@  > /dev/null


clean:
	$(RM) *~  $(PAGES)
