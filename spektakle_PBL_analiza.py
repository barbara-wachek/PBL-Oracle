import pandas as pd

# =============================================================================
# WCZYTANIE DANYCH
# =============================================================================

df = pd.read_csv(
    "data/SPEKTAKLE_PBL_ORACLE_20260623.csv",
    dtype=str
)

print(f"Liczba rekordów: {df.shape[0]}")
print(f"Liczba kolumn: {df.shape[1]}")

# =============================================================================
# PODSTAWOWE INFORMACJE
# =============================================================================

print("\nKolumny:")
print(df.columns.tolist())

print("\nTypy danych:")
print(df.dtypes)

# =============================================================================
# ANALIZA PUSTYCH WARTOŚCI
# =============================================================================

raport_nulli = pd.DataFrame({
    "liczba_nulli": df.isna().sum(),
    "procent_nulli": round(df.isna().mean() * 100, 2)
})

print("\nRaport pustych wartości:")
print(
    raport_nulli.sort_values(
        "procent_nulli",
        ascending=False
    )
)

# =============================================================================
# KOLUMNY W 100% PUSTE
# =============================================================================

print("\nKolumny całkowicie puste:")

for col in df.columns[df.isna().all()]:
    print(col)

# =============================================================================
# KOLUMNY POWYŻEJ 90% PUSTYCH WARTOŚCI
# =============================================================================

print("\nKolumny z ponad 90% pustych wartości:")

procent_nulli = df.isna().mean() * 100

print(
    procent_nulli[
        procent_nulli > 90
    ].sort_values(ascending=False)
)

# =============================================================================
# KOLUMNY O JEDNEJ WARTOŚCI
# =============================================================================

print("\nKolumny o jednej wartości:")

for col in df.columns:
    if df[col].nunique(dropna=False) == 1:
        print(col)

# =============================================================================
# RZADKO WYPEŁNIONE KOLUMNY
# =============================================================================

for col in ["ZA_NAZWA_ADAPT_DZIELA", "ZA_TYTUL_CALOSCI"]:
    print(f"\n{col}")

    print(
        df[df[col].notna()][[col]]
        .head(20)
    )











