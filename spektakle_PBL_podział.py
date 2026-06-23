import pandas as pd

# =============================================================================
# WCZYTANIE DANYCH
# =============================================================================

df = pd.read_csv(
    "data/SPEKTAKLE_PBL_ORACLE_20260623.csv",
    dtype=str
)

# =============================================================================
# USUNIĘCIE ZBĘDNYCH KOLUMN
# =============================================================================

kolumny_do_usuniecia = [
    "ZA_OPIS_CALOSCI",
    "ZA_TYTUL_ORYGINALU",
    "ZA_JEZYK_ORYGINALU",
    "ZA_TYTUL_ADAPT_DZIELA",
    "ZA_RZ_RODZAJ1_ID",
    "RZ_NAZWA"
]

df_final = df.drop(
    columns=kolumny_do_usuniecia
)


# =============================================================================
# OSOBNY DATAFRAME DLA SPEKTAKLI FABULARNYCH TV
# =============================================================================


df_tv = df_final[
    df_final["DZ_NAZWA"].str.contains(
        r"Spektakle fabularne TV",
        na=False
    )
].copy()


# =============================================================================
# OSOBNY DATAFRAME DLA SPEKTAKLI TEATRALNYCH
# ============================================================================

df_teatr = df_final[
    ~df_final["DZ_NAZWA"].str.contains(
        r"Spektakle fabularne TV",
        na=False
    )
].copy()

# =============================================================================
# SANITY CHECK 
# =============================================================================

print("TV:", len(df_tv))
print("Teatr:", len(df_teatr))
print("Suma:", len(df_tv) + len(df_teatr))
print("Oryginał:", len(df_final))



# =============================================================================
# ZAPIS DO PLIKÓW
# =============================================================================

df_tv.to_csv(
    "data/PBL_spektakle_tv_20260623.csv",
    index=False,
    encoding="utf-8-sig"
)

df_teatr.to_csv(
    "data/PBL_spektakle_teatralne_20260623.csv",
    index=False,
    encoding="utf-8-sig"
)






















# =============================================================================
# ROK PREMIERY
# =============================================================================

# 1. pełna data lub rok z OPISU (najbogatsze źródło)
data_z_opisu = (
    df_final["ZA_OPIS_ADAPT_DZIELA"]
    .str.extract(
        r'(\d{1,2}\s*[.\-]?\s*[IVXLCDM]+\.?\s*\d{4}|'   # 5 XII 1988
        r'\d{1,2}[.\-]\d{1,2}[.\-]\d{4}|'              # 05.12.1988
        r'((?:18|19|20)\d{2}))'                        # sam rok
    )[0]
)

# 2. rok z TYTUŁU (fallback)
data_z_tytulu = (
    df_final["ZA_TYTUL"]
    .str.extract(r'((?:18|19|20)\d{2})')[0]
)

# 3. połączenie: OPIS ma priorytet
df_final["data_premiery"] = data_z_opisu.fillna(data_z_tytulu)



# =============================================================================
# OCZYSZCZONY TYTUŁ
# =============================================================================

df_final["tytul_clean"] = (
    df_final["ZA_TYTUL"]
    .str.replace(
        r'\.\s*Prem\.?\s*(?:18|19|20)\d{2}(?:\s*\[\?\]|\?)?$',
        '',
        regex=True
    )
    .str.strip()
)

# =============================================================================
# UWAGI
# =============================================================================

df_final["uwagi"] = None

maska_niepewny_rok = (
    df_final["ZA_TYTUL"]
    .str.contains(
        r'(?:18|19|20)\d{2}\s*(?:\[\?\]|\?)',
        regex=True,
        na=False
    )
)

df_final.loc[
    maska_niepewny_rok,
    "uwagi"
] = "rok niepewny"

# =============================================================================
# Program TV i data emisji dla spektakli telewizyjnych 
# =============================================================================


df_final["program_tv"] = (
    df_final["ZA_OPIS_ADAPT_DZIELA"]
    .str.extract(r'^\s*(I{1,3}|IV|V)\s*,')[0]
)


df_final["data_emisji"] = (
    df_final["ZA_OPIS_ADAPT_DZIELA"]
    .str.extract(
        r'(\d{1,2}\s*[IVXLCDM]{3,4}\.?\s*\d{4}|'   # 15 XII 1988
        r'\d{1,2}[.\-]\d{1,2}[.\-]\d{4})'
    )[0]
)














# =============================================================================
# RAPORT KONTROLNY
# =============================================================================

print(f"Liczba rekordów: {len(df_final)}")

print(
    "Rok premiery znaleziony dla:",
    df_final["rok_premiery"].notna().sum(),
    "rekordów"
)

print(
    "Rok premiery nieznany dla:",
    df_final["rok_premiery"].isna().sum(),
    "rekordów"
)

print(
    "Niepewny rok:",
    (df_final["uwagi"] == "rok niepewny").sum(),
    "rekordów"
)

# =============================================================================
# ZAPIS
# =============================================================================

df_final.to_csv(
    "data/SPEKTAKLE_PBL_20260623_processed.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nZapisano:")
print("data/SPEKTAKLE_PBL_20260623_processed.csv")