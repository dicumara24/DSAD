import pandas as pd

def nan_replace_df(tabel):
    coloane_numerice = tabel.select_dtypes(include=['number']).columns
    for col in coloane_numerice:
        media = tabel[col].mean()
        tabel[col] = tabel[col].fillna(media)
    return tabel

def salvare_matrice(x, index_linie, index_coloana, fisier):
    df = pd.DataFrame(x, index=index_linie, columns=index_coloana)
    df.to_csv(fisier, sep=';')
    return df