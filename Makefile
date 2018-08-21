# The available translation languages.
# When starting a new translation, add a language code here.

SHELL := /bin/bash

.PHONY: all clean sync public distclean en

all: en

en: book-en book-en/default.css book-en.html # book-en.pdf book-en.epub

# The book consists of these text files in the following order:

TXTFILES := preface.txt intro.txt basic.txt clone.txt branch.txt history.txt \
    multiplayer.txt grandmaster.txt secrets.txt drawbacks.txt translate.txt

book-en.xml: $(addprefix en/,$(TXTFILES))
	# Concatenate the text files and feed to AsciiDoc.
	# If a file has not yet been translated for the target language,
	# then substitute the English version.
	# Kludge to support any translation of "Preface".
	echo '[specialsections]' > conf ; \
	sed -n '/^== .* ==$$/p' en/preface.txt | sed 's/^== \(.*\) ==$$/^\1$$=preface/' >> conf ; \
	( for FILE in $^ ; do \
		if [ -f $$FILE ]; then \
			cat $$FILE; \
		else \
			cat en/$$(basename $$FILE); \
		fi; \
		echo ; \
	done ) | \
	asciidoc -a lang=en -d book -b docbook -f conf - > $@

# Ignore tidy's exit code because Asciidoc generates section IDs beginning with
# "_", which xmlto converts to "id" attributes of <a> tags. The standard
# insists that "id" attributes begin with a letter, which causes tidy to
# print a warning and return a nonzero code.
#
# When Asciidoc 8.3.0+ is widespread, I'll use its idprefix attribute instead
# of ignoring return codes.

book-en: book-en.xml
	xmlto -m custom-html.xsl -o book-en html book-en.xml
	sed -i'' -e 's/xmlns:fo[^ ]*//g' book-en/*.html
	-ls book-en/*.html | xargs -n 1 tidy -utf8 -m -i -q
	./makeover en

book-en/default.css: book.css
	-mkdir -p book-en
	rsync book.css book-en/default.css

book-en.html: book-en.xml
	pandoc -s -f docbook -t html5 -o $@ $^

book-en.pdf: book-en.xml
	pandoc -s -f docbook -o $@ --latex-engine xelatex $^

book-en.epub: book-en.xml
	pandoc -s -f docbook -o $@ $^

clean:
	-rm -rf book-en.pdf book-en.xml book-en.html book-en *.fo *.log *.out *.aux conf
