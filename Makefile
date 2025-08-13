PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
DOCDIR = $(PREFIX)/share/doc/Padmapper
PYTHON ?= python3

PKGNAME = Padmapper
PKGFILES = __init__.py padmapper.py padmapper_capture.py Padmapper.py Keyboard.py Params.py Mouse.py

all:
	@echo "Nothing to build, run 'make install' to install."

install:
	# Documentation
	install -d "$(DOCDIR)"
	install -m 644 config_template.json "$(DOCDIR)/"
	install -m 644 README.md "$(DOCDIR)/"
	cp -r configs "$(DOCDIR)/"

	# Main executable
	install -d "$(BINDIR)"
	install -m 755 padmapper padmapper-capture "$(BINDIR)/"

	# Python module
	install -d "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)"
	install -m 644 $(PKGFILES) "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)/"

uninstall:
	rm -rf "$(DOCDIR)"
	rm -f "$(BINDIR)/padmapper" "$(BINDIR)/padmapper-capture"
	rm -rf "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)"

.PHONY: all install uninstall
