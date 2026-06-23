import re
import pandas as pd


def parse_opis(text):
    if not isinstance(text, str):
        return {}

    text = text.replace("\xa0", " ")

    result = {
        "reżyser": None,
        "tłumaczenie": None,
        "adapt_tytuł": None,
        "adapt_osoby": None
    }

    # =========================
    # REŻYSER (ODPORNY WZORZEC)
    # =========================
    m = re.search(r"Reż\.?\s*[:.]?\s*(.+?)(?=\.|Tł|Adapt|II,|I,|$)", text, re.IGNORECASE)
    if m:
        result["reżyser"] = m.group(1).strip()

    # =========================
    # TŁUMACZENIE
    # =========================
    m = re.search(r"Tł\.?\s*[:.]?\s*(.+?)(?=\.|Reż|Adapt|II,|I,|$)", text, re.IGNORECASE)
    if m:
        result["tłumaczenie"] = m.group(1).strip()

    # =========================
    # ADAPT - tytuł
    # =========================
    m = re.search(r'Adapt\.?\s*pt\.?\s*"?([^"\.]+)"?', text, re.IGNORECASE)
    if m:
        result["adapt_tytuł"] = m.group(1).strip()

    # =========================
    # ADAPT - osoby
    # =========================
    else:
        m = re.search(r"Adapt\.?\s*(.+?)(?=\.|Reż|Tł|II,|I,|$)", text, re.IGNORECASE)
        if m:
            result["adapt_osoby"] = m.group(1).strip()

    return result