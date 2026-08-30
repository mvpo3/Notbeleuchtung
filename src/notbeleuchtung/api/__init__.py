"""api — dünne FastAPI-Hülle über der Engine (Nordstern-Auslieferungs-Naht).

`pipeline.run()` IST die Engine; diese Schicht macht sie nur über HTTP erreichbar
(Plan hoch → Notbeleuchtungsplan zurück). Kein Fach-Wissen hier.
"""
from .main import app, create_app

__all__ = ["app", "create_app"]
