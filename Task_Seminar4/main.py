import sys
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from seaborn import heatmap

from functii import nan_replace_df, acp, tabelare_varianta, salvare_ndarray
from grafice import plot_varianta, show, corelograma

os.makedirs("data_out", exist_ok=True)
os.makedirs("graphics", exist_ok=True)

set_date = pd.read_csv("data_in/Wholesale customers data.csv")

variabile_cheltuieli = ['Fresh', 'Milk', 'Grocery', 'Frozen', 'Detergents_Paper', 'Delicassen']
x = set_date[variabile_cheltuieli].values

x_, r_v, alpha, a = acp(x, scal=True)

r_v_df = pd.DataFrame(r_v, index=variabile_cheltuieli, columns=variabile_cheltuieli)

plt.figure("Matricea de Corelatie", figsize=(8, 6))
plt.title("Matricea de corelatie (Seaborn)", color="b", fontsize=14)
heatmap(r_v_df, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.tight_layout()
plt.savefig("graphics/Matrice_Corelatie.png")

t_varianta = tabelare_varianta(alpha)
print("\n--- Tabelul Variantei ---")
print(t_varianta.round(4))

t_varianta.round(4).to_csv("data_out/Varianta.csv")

procent_cumulat = t_varianta["Procent cumulat"].values
componente_necesare = np.where(procent_cumulat >= 80)[0][0] + 1

print(f"\nNumarul de componente necesare pentru 80% varianta: {componente_necesare}")

plot_varianta(alpha)
print("\nGata!")