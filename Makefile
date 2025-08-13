PREFIX ?= /usr/local
BINDIR = $(PREFIX)/bin
DOCDIR = $(PREFIX)/share/doc/Padmapper
PYTHON ?= python3

PKGNAME = padmapper
PKGFILES = padmapper/__init__.py padmapper/padmapper.py padmapper/padmapper_capture.py padmapper/Padmapper.py padmapper/Keyboard.py padmapper/Params.py padmapper/Mouse.py

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
	install -m 755 scripts/padmapper scripts/padmapper-capture "$(BINDIR)/"

	# Python module
	install -d "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)"
	install -m 644 $(PKGFILES) "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)/"

uninstall:
	rm -rf "$(DOCDIR)"
	rm -f "$(BINDIR)/padmapper" "$(BINDIR)/padmapper-capture"
	rm -rf "$(PREFIX)/lib/$(shell $(PYTHON) -c 'import sys; print("python%d.%d" % sys.version_info[:2])')/site-packages/$(PKGNAME)"

.PHONY: all install uninstall
