"""hauptengine.dwg_input — DWG-Architekturpläne via ODA File Converter lesen.

ezdxf liest kein DWG nativ; `ezdxf.addons.odafc` delegiert an den kostenlosen
ODA File Converter (externes Programm). Dieses Modul kapselt zwei Probleme:

1. **Discovery:** odafc erwartet die Exe unter dem unversionierten Default-Pfad
   ``C:\\Program Files\\ODA\\ODAFileConverter\\ODAFileConverter.exe`` — der
   Installer legt aber versionierte Ordner an (``ODAFileConverter 27.1.0``).
   `oda_verfuegbar()` sucht die Exe per Glob und registriert sie in den
   ezdxf-Optionen, damit odafc sie findet.
2. **Eingangs-Konvertierung:** `stelle_dxf_bereit()` ist der eine Einstiegspunkt
   für die Pipeline/API — DXF geht unverändert durch (bit-identisches Verhalten
   für den bestehenden Pfad), DWG wird in ein Arbeitsverzeichnis konvertiert.
   Fehlt der Konverter, bricht das mit `OdaKonverterFehlt` und einem
   Installations-Hinweis ab statt mit einem kryptischen ezdxf-Fehler.
"""
from __future__ import annotations

import re
from collections.abc import Iterable
from pathlib import Path

# Versionierte Installations-Wurzeln des ODA File Converter unter Windows.
_ODA_SUCH_WURZELN = (
    Path("C:/Program Files/ODA"),
    Path("C:/Program Files (x86)/ODA"),
)
_ODA_EXE_NAME = "ODAFileConverter.exe"
_ODA_DOWNLOAD = "https://www.opendesign.com/guestfiles/oda_file_converter"

_verfuegbar_cache: bool | None = None


class OdaKonverterFehlt(RuntimeError):
    """DWG-Input angefordert, aber kein ODA File Converter auffindbar."""

    def __init__(self, pfad: Path) -> None:
        super().__init__(
            f"'{pfad.name}' ist eine DWG-Datei — ezdxf liest DWG nicht nativ und der "
            f"ODA File Converter wurde nicht gefunden. Kostenloser Download: {_ODA_DOWNLOAD} "
            "(nach Installation wird die Exe automatisch unter "
            "'C:/Program Files/ODA/…' gefunden). Alternativ den Plan als DXF exportieren."
        )


def _versions_schluessel(exe: Path) -> tuple[int, ...]:
    """Sortier-Schlüssel aus dem versionierten Ordnernamen (`ODAFileConverter 27.1.0`)."""
    return tuple(int(z) for z in re.findall(r"\d+", exe.parent.name)) or (0,)


def finde_oda_exe(such_wurzeln: Iterable[Path] = _ODA_SUCH_WURZELN) -> Path | None:
    """Neueste ODAFileConverter.exe unter den versionierten Installations-Ordnern."""
    kandidaten = [
        exe
        for wurzel in such_wurzeln
        if wurzel.is_dir()
        for exe in wurzel.glob(f"*/{_ODA_EXE_NAME}")
        if exe.is_file()
    ]
    if not kandidaten:
        return None
    return max(kandidaten, key=_versions_schluessel)


def oda_verfuegbar() -> bool:
    """True, wenn odafc den Konverter nutzen kann; registriert gefundene Exe bei ezdxf."""
    global _verfuegbar_cache
    if _verfuegbar_cache is not None:
        return _verfuegbar_cache
    import ezdxf
    from ezdxf.addons import odafc

    if not odafc.is_installed():
        exe = finde_oda_exe()
        if exe is not None:
            # odafc liest den Pfad aus den ezdxf-Optionen (Anführungszeichen wegen
            # Leerzeichen im Ordnernamen — odafc strippt sie selbst wieder).
            ezdxf.options.set("odafc-addon", "win_exec_path", f'"{exe}"')
    _verfuegbar_cache = odafc.is_installed()
    return _verfuegbar_cache


def stelle_dxf_bereit(pfad: str | Path, arbeits_dir: str | Path) -> Path:
    """Liefert einen von ezdxf lesbaren Plan-Pfad: DXF unverändert, DWG konvertiert.

    Die Konvertierung schreibt `<stem>.dxf` nach `arbeits_dir`; der Aufrufer besitzt
    das Verzeichnis und räumt es auf (Pipeline: TemporaryDirectory, API: Workdir).
    """
    quelle = Path(pfad)
    if quelle.suffix.lower() != ".dwg":
        return quelle
    if not oda_verfuegbar():
        raise OdaKonverterFehlt(quelle)
    from ezdxf.addons import odafc

    ziel = Path(arbeits_dir) / f"{quelle.stem}.dxf"
    odafc.convert(quelle, ziel, version="R2018", replace=True)
    return ziel
