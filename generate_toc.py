#!/usr/bin/env python3
"""
generate_toc.py
Generiert das Inhaltsverzeichnis für content_abschlussarbeiten.html.

Verwendung:
    python3 generate_toc.py content_abschlussarbeiten.html

Das Skript liest die Datei und extrahiert:
  - <h2>-Überschriften (ohne id) als Abschnittsköpfe
  - <h4 id="...">-Überschriften als verlinkbare Einträge

<h2>Inhaltsverzeichnis</h2> und <h3>-Überschriften werden ignoriert.
Das fertige Inhaltsverzeichnis wird auf stdout ausgegeben.
"""

import re
import sys
from html.parser import HTMLParser
from html import unescape


class Entry:
    def __init__(self, level: int, anchor: str | None, text: str):
        self.level = level        # 2 oder 4
        self.anchor = anchor      # id-Attribut (nur bei h4)
        self.text = text          # sichtbarer Titeltext


class HeadingParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries: list[Entry] = []
        self._cur_level: int | None = None
        self._cur_anchor: str | None = None
        self._cur_text: list[str] = []
        self._inner_depth = 0

    # ------------------------------------------------------------------ #
    # Parsen                                                               #
    # ------------------------------------------------------------------ #
    def handle_starttag(self, tag: str, attrs):
        level = self._level(tag)
        if level in (2, 4) and self._cur_level is None:
            anchor = dict(attrs).get("id")  # None wenn kein id
            self._cur_level = level
            self._cur_anchor = anchor
            self._cur_text = []
            self._inner_depth = 0
        elif self._cur_level is not None:
            self._inner_depth += 1

    def handle_endtag(self, tag: str):
        level = self._level(tag)
        if level == self._cur_level and self._inner_depth == 0:
            text = " ".join(unescape("".join(self._cur_text)).split())
            # Inhaltsverzeichnis-Überschrift selbst überspringen
            if text.lower() != "inhaltsverzeichnis":
                self.entries.append(
                    Entry(self._cur_level, self._cur_anchor, text)
                )
            self._cur_level = None
            self._cur_anchor = None
            self._cur_text = []
        elif self._cur_level is not None and self._inner_depth > 0:
            self._inner_depth -= 1

    def handle_data(self, data: str):
        if self._cur_level is not None:
            self._cur_text.append(data)

    def handle_entityref(self, name: str):
        if self._cur_level is not None:
            self._cur_text.append(f"&{name};")

    def handle_charref(self, name: str):
        if self._cur_level is not None:
            self._cur_text.append(f"&#{name};")

    @staticmethod
    def _level(tag: str) -> int | None:
        m = re.fullmatch(r"h([24])", tag.lower())
        return int(m.group(1)) if m else None


# ------------------------------------------------------------------ #
# TOC-Ausgabe                                                          #
# ------------------------------------------------------------------ #
def build_toc(entries: list[Entry]) -> str:
    lines: list[str] = ["<h2>Inhaltsverzeichnis</h2>", ""]
    in_section = False

    for entry in entries:
        if entry.level == 2:
            if in_section:
                lines.append("        </ul>")
                lines.append("")
            lines.append(f"        <h3>{entry.text}</h3>")
            lines.append('        <ul class="list">')
            in_section = True
        elif entry.level == 4:
            if entry.anchor:
                link = f'<a href="#{entry.anchor}">{entry.text}</a>'
            else:
                link = entry.text
            lines.append(f"          <li>{link}</li>")

    if in_section:
        lines.append("        </ul>")

    return "\n".join(lines)


# ------------------------------------------------------------------ #
# Hauptprogramm                                                        #
# ------------------------------------------------------------------ #
def main():
    if len(sys.argv) != 2:
        print(f"Verwendung: {sys.argv[0]} <html-datei>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"Fehler: Datei nicht gefunden: {path}", file=sys.stderr)
        sys.exit(1)

    parser = HeadingParser()
    parser.feed(html)

    h4_count = sum(1 for e in parser.entries if e.level == 4)
    if not parser.entries or h4_count == 0:
        print("Warnung: Keine passenden Überschriften gefunden.", file=sys.stderr)
        sys.exit(1)

    print(build_toc(parser.entries))


if __name__ == "__main__":
    main()
