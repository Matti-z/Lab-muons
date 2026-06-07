import numpy as np
import matplotlib.pyplot as plt


# 2. Generazione del dataset (2 Esponenziali + 1 Uniforme)
N_events = 50000

# Componente 1: Segnale/Fondo a corto raggio (Esponenziale ripido)
data_exp1 = np.random.exponential(scale=10, size=int(N_events * 0.4))
# Componente 2: Fondo a lungo raggio (Esponenziale più piatto)
data_exp2 = np.random.exponential(scale=40, size=int(N_events * 0.4))
# Componente 3: Fondo combinatorio/rumore (Uniforme)
data_uniform = np.random.uniform(low=0, high=150, size=int(N_events * 0.2))

# Combiniamo tutto in un unico dataset per calcolare i bin complessivi
all_data = np.concatenate([data_exp1, data_exp2, data_uniform])

data_e1 = all_data
data_e2 = np.concatenate([data_exp2, data_uniform])

# 3. Configurazione del binning dell'istogramma
bin_edges = np.linspace(0, 150, 50)
bin_count = 50

# 4. Creazione del grafico
fig, ax = plt.subplots(figsize=(10, 8))

# Calcoliamo gli istogrammi per ogni singola componente
counts_exp1, _ = np.histogram(data_exp1, bins=bin_edges, range=(0, 150))
counts_exp2, _ = np.histogram(data_exp2, bins=bin_edges, range=(0, 150))
counts_unif, _ = np.histogram(data_uniform, bins=bin_edges, range=(0, 150))
bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

# Somma totale delle componenti
counts_total = counts_exp1 + counts_exp2 + counts_unif


ax.hist(data_e1 , bins = bin_count , range=(0, 150), label="exp1", color='yellow', alpha=0.25)
ax.hist(data_e2 , bins = bin_count , range=(0, 150), label="exp2", color='red', alpha=0.4)
ax.hist(data_uniform , bins = bin_count , range=(0, 150), label="uniform", color='green', alpha=0.6)

ax.scatter(bin_centers, counts_exp1 + counts_exp2 + counts_unif, label="exp1 points", color='goldenrod', s=25, zorder=3)
ax.scatter(bin_centers, counts_exp2 + counts_unif, label="exp2 points", color='navy', s=25, zorder=3)
ax.scatter(bin_centers, counts_unif, label="uniform points", color='darkgreen', s=25, zorder=3)



# Simulazione dei "Dati" sperimentali (punti con errore statistico poissoniano)
# Questo è molto comune nei plot di CMS per confrontare il modello (somma) con i dati stabili
data_obs = np.random.poisson(counts_total)
ax.errorbar(bin_centers, data_obs, yerr=np.sqrt(data_obs), fmt='ko', markersize=4, label='Pseudo-Data (Poisson)')

# 6. Decorazioni e Label in stile CMS
ax.set_xlabel('$t [\mu s]$ ', fontsize=22)
ax.set_ylabel('Events', fontsize=22)
ax.set_xlim(0, 150)

# Legenda ben posizionata
ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='none')

plt.tight_layout()
plt.show()

