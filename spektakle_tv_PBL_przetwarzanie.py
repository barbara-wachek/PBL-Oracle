import pandas as pd
import re
from parser_roles import parse_opis

# =============================================================================
# 1. WCZYTANIE
# =============================================================================

df = pd.read_csv(
    "data/PBL_spektakle_tv_20260623.csv",
    dtype=str
)

print("Rekordy:", df.shape[0])
print("Kolumny:", df.shape[1])

# =============================================================================
# 2. RAPORT BRAKÓW
# =============================================================================

raport = pd.DataFrame({
    "null_count": df.isna().sum(),
    "null_pct": (df.isna().mean() * 100).round(2)
}).sort_values("null_pct", ascending=False)

print("\nTOP braków:\n", raport.head(10))


# =============================================================================
# 3. TYTUŁ CLEAN (bez dopisków typu Prem., jeśli się zdarzą)
# =============================================================================

df["tytul_clean"] = (
    df["ZA_TYTUL"]
    .str.replace(r'\.\s*Prem\.?\s*(?:\d{4})\??', '', regex=True)
    .str.strip()
)

# =============================================================================
# 4. DATA PREMIERY (jeśli występuje - rzadziej, ale bywa)
#    UWAGA: to NIE jest główna data TV
# =============================================================================

df["data_premiery"] = (
    df["ZA_OPIS_ADAPT_DZIELA"]
    .str.extract(r'Prem\.?\s*((?:18|19|20)\d{2})')[0]
)

df["data_premiery"] = pd.to_numeric(
    df["data_premiery"],
    errors="coerce"
)

# =============================================================================
# 5. PROGRAM TV (I / II / III)
# =============================================================================

df["program_tv"] = (
    df["ZA_OPIS_ADAPT_DZIELA"]
    .str.extract(r'\s*(I{1,3}|IV|V)\s*,')[0]
)

# =============================================================================
# 6. DATA EMISJI (pierwsza emisja jako reprezentant)
# =============================================================================

def parse_emisje(text):
    if pd.isna(text):
        return []

    text = str(text)

    daty = re.findall(
        r'(\d{1,2}\s*[IVXLCDM]+\.?\s*\d{4}|\d{1,2}[.\-]\d{1,2}[.\-]\d{4})',
        text
    )

    czasy = re.findall(r"(\d{2,3})\s*'", text)

    return [
        {
            "data": daty[i],
            "czas_min": int(czasy[i]) if i < len(czasy) else None
        }
        for i in range(len(daty))
    ]

df["emisje"] = df["ZA_OPIS_ADAPT_DZIELA"].apply(parse_emisje)



# =============================================================================
# 7. ROLE (REŻYSER, TŁUMACZ ITP.)
# =============================================================================
#POPRAWIĆ BO NIE DZIAŁA

df["role"] = df["ZA_OPIS_ADAPT_DZIELA"].apply(parse_opis)



# =============================================================================
# 8. STATYSTYKI
# =============================================================================

print("\nBrak tytułów:", df["ZA_TYTUL"].isna().sum())
print("Brak programów TV:", df["program_tv"].isna().sum())

print("\nNajczęstsze programy TV:")
print(df["program_tv"].value_counts(dropna=False))


# =============================================================================
# 9. ZAPIS
# =============================================================================

df.to_csv(
    "data/PBL_spektakle_tv_20260623_processed.csv",
    index=False,
    encoding="utf-8-sig"
)















