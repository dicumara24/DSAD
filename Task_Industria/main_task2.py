import numpy as np
import pandas as pd
import os

os.makedirs('data_out', exist_ok=True)

def calcul_medie_ponderata(t: pd.DataFrame):
    x = t.values
    mp = np.average(x[:, :-1], axis=0, weights=x[:, -1])
    return pd.Series(mp, t.columns[:-1])

industria_alim = pd.read_csv("data_in/IndustriaAlimentara.csv", index_col=0)
populatie = pd.read_csv("data_in/PopulatieLocalitati.csv", index_col=0)
coduri_judete = pd.read_csv("data_in/Coduri_Judete.csv", index_col=0)

industrii = list(industria_alim)[1:]

angajati = industria_alim[industrii].sum(axis=1)
cerinta1 = industria_alim[angajati > 0]
cerinta1.to_csv("data_out/Cerinta1.csv")

cerinta2 = industria_alim[industrii].apply(lambda x: x * 100 / x.sum(), axis=1)
cerinta2.insert(0, "Localitate", industria_alim["Localitate"])
cerinta2.to_csv("data_out/Cerinta2.csv")

industria_alim_loc = industria_alim.merge(populatie, left_index=True, right_index=True)
industria_alim_judet = industria_alim_loc[industrii + ["Populatie", "Judet"]].groupby(by="Judet").sum()

cerinta3 = industria_alim_judet.apply(lambda x: x[industrii].sum() / x["Populatie"], axis=1)
cerinta3.name = "Pondere"
cerinta3 = cerinta3.sort_values(ascending=False)
cerinta3.to_csv("data_out/Cerinta3.csv")

cerinta4 = industria_alim_judet[industrii].apply(lambda x: x.index[x.argmax()], axis=1)
cerinta4.name = "Activitate"
cerinta4.to_csv("data_out/Cerinta4.csv")

industria_alim_loc_ = industria_alim_loc[industrii + ["Judet", "Populatie"]].merge(
    coduri_judete["Regiune"], left_on="Judet", right_index=True
)

cerinta5 = industria_alim_loc_[industrii + ["Populatie", "Regiune"]].groupby(by="Regiune").apply(
    func=calcul_medie_ponderata, include_groups=False
)
cerinta5.round(3).to_csv("data_out/Cerinta5.csv")

total_national = industria_alim_judet.sum(axis=0)
cerinta6 = industria_alim_judet.apply(
    lambda x: (x[industrii] / total_national[industrii]) / (x["Populatie"] / total_national["Populatie"]),
    axis=1
)
cerinta6.round(3).to_csv("data_out/Cerinta6.csv")

print("Toate cerintele au fost salvate in data_out.")