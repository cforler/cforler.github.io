PROG=./pagebuild.sh
BASICS=footer.html header.html navigation.html

all: index.html crashkurs.html leitfaden.html abschlussarbeiten.html oral_examination.html

index.html: content_index.html $(BASICS)
	$(PROG) $< $@
	tidy -q $@  > /dev/null

leitfaden.html: content_leitfaden.html $(BASICS)
	$(PROG) $< $@ 
	tidy -q $@  > /dev/null

abschlussarbeiten.html: content_abschlussarbeiten.html $(BASICS)
	$(PROG) $< $@
	tidy -q $@  > /dev/null

crashkurs.html: content_crashkurs.html $(BASICS)
	$(PROG) $< $@
	tidy -q $@  > /dev/null

oral_examination.html: content_oral_examination.html $(BASICS)
	$(PROG) $< $@
	tidy -q $@  > /dev/null

clean:
	$(RM) *~  index.html leitfaden.html abschlussarbeiten.html crashkurs.html oral_examination.html
