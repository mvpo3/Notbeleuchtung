"""LB (Leistungsbeschreibung) — 2. Engine-Input: Freitext → LBVorgabe (Enis).

Die projektspezifischen, EXPLIZITEN Auftraggeber-Vorgaben, die Norm-Defaults
übersteuern (CLAUDE.md-Hierarchie). `LbTextProvider.parse_lb` erfüllt das
`LBProvider`-Protocol.
"""
from notbeleuchtung.normwissen.lb.parser import LbTextProvider, parse_lb

__all__ = ["LbTextProvider", "parse_lb"]
