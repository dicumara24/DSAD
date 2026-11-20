import pandas as pd
import os
from scipy.spatial.distance import cdist
from functii_online import nan_replace_df, salvare_matrice

os.makedirs('data_out', exist_ok=True)

df = pd.read_csv('data_in/winequality-red.csv', sep=';')
print("Cerinta 1 - Shape:", df.shape)
print(df.head())
print(df.dtypes)

df = nan_replace_df(df)
print("\nCerinta 2 - NaN ramase:", df.isna().sum().sum())

df_calitate = df[df['quality'] >= 7]
df_calitate.to_csv('data_out/vinuri_calitate_min7.csv', index=False, sep=';')

df_top50 = df.sort_values(by='alcohol', ascending=False).head(50)
df_top50.to_csv('data_out/top50_alcool.csv', index=False, sep=';')

df_medii = df.groupby('quality')[['alcohol', 'pH']].mean().reset_index()
df_medii.to_csv('data_out/medii_pe_calitate.csv', index=False, sep=';')

df['aciditate_totala'] = df['fixed acidity'] + df['volatile acidity'] + df['citric acid']
df_aciditate = df[['quality', 'alcohol', 'aciditate_totala', 'pH']]
df_aciditate.to_csv('data_out/vinuri_cu_aciditate.csv', index=False, sep=';')

medii_alcool = df.groupby('quality')['alcohol'].mean()
nota_max = medii_alcool.idxmax()
df_nota_max = pd.DataFrame({'quality': [nota_max]})
df_nota_max.to_csv('data_out/calitate_max_alcool.csv', index=False, sep=';')
print("\nCerinta 7 - Nota max:", nota_max)

coloane_corelatie = ['fixed acidity', 'volatile acidity', 'citric acid', 'alcohol', 'quality']
matrice_corelatie = df[coloane_corelatie].corr()
matrice_corelatie.to_csv('data_out/R.csv', sep=';')

df['alcohol_std'] = (df['alcohol'] - df['alcohol'].mean()) / df['alcohol'].std()
df_std = df[['alcohol', 'alcohol_std']]
df_std.to_csv('data_out/alcohol_standardizat.csv', index=False, sep=';')

df_20 = df.head(20).copy()
coloane_distanta = ['fixed acidity', 'volatile acidity', 'alcohol']
for col in coloane_distanta:
    df_20[col] = (df_20[col] - df_20[col].mean()) / df_20[col].std()

matrice_distante = cdist(df_20[coloane_distanta], df_20[coloane_distanta], metric='euclidean')
salvare_matrice(matrice_distante, df_20.index, df_20.index, 'data_out/d_euclid_20.csv')

print("\nToate cerintele au fost salvate in data_out.")