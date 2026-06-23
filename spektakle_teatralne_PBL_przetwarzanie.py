import pandas as pd
import re

# =============================================================================
# 1. WCZYTANIE
# =============================================================================

df = pd.read_csv(
    "data/PBL_spektakle_teatralne_20260623.csv",
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
# 3. TYTUŁ CLEAN (bez "Prem.")
# =============================================================================

df["tytul_clean"] = (
    df["ZA_TYTUL"]
    .str.replace(r'\.\s*Prem\.?\s*(?:\d{4})\??', '', regex=True)
    .str.strip()
)

# =============================================================================
# 4. DATA PREMIERY 
# =============================================================================

df["data_premiery"] = (
    df["ZA_TYTUL"]
    .str.extract(r'Prem\.?\s*((?:18|19|20)\d{2})')[0]
)

df["data_premiery"] = pd.to_numeric(
    df["data_premiery"],
    errors="coerce"
)

# =============================================================================
# 5. UWAGI: niepewne lata
# =============================================================================

df["uwagi"] = None

maska_niepewne = df["ZA_TYTUL"].str.contains(
    r'\?\]|\?\s|Prem\.?\s*\d{4}\?',
    na=False
)

df.loc[maska_niepewne, "uwagi"] = "rok niepewny"

# =============================================================================
# 6. NORMALIZACJA TEATRÓW
# =============================================================================

df["TE_NAZWA"] = df["TE_NAZWA"].str.strip()

# =============================================================================
# 7. PODSTAWOWE STATYSTYKI NULLI
# =============================================================================

print("\nBrak tytułów:", df["ZA_TYTUL"].isna().sum())
print("Brak dat premiery:", df["data_premiery"].isna().sum())


# =============================================================================
# 8. ZAPIS
# =============================================================================

df.to_csv(
    "data/PBL_spektakle_teatralne_20260623_processed.csv",
    index=False,
    encoding="utf-8-sig"
)