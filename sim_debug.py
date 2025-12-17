from sim import sim
import numpy as np
import csv
import matplotlib.pyplot as plt

doppie_vec = []
triple_vec = []
flag_vec = []
for i in range(100):
    doppie, triple, flag = sim()
    print("\n")
    print("\r", doppie , triple , flag , flush=True)
    print("\n")
    doppie_vec.append(doppie)
    triple_vec.append(triple)
    flag_vec.append(flag)

# save to CSV
with open('sim_results.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['doppie', 'triple', 'flag'])
    for d, t, fl in zip(doppie_vec, triple_vec, flag_vec):
        writer.writerow([d, t, fl])



# convert to numpy arrays
d_arr = np.array(doppie_vec, dtype=float)
t_arr = np.array(triple_vec, dtype=float)
f_arr = np.array(flag_vec)
# normalize flag to ints if boolean-like
try:
    f_num = f_arr.astype(int)
except Exception:
    # fallback: map truthy values to 1, others to 0
    f_num = np.array([1 if x else 0 for x in f_arr], dtype=int)

# safe ratio (avoid divide-by-zero)
ratio = np.where(d_arr == 0, np.nan, t_arr / d_arr)

# small helper to print basic stats
def print_stats(name, a):
    a_clean = np.asarray(a, dtype=float)
    n = a_clean.size
    mean = np.nanmean(a_clean)
    std = np.nanstd(a_clean)
    mn = np.nanmin(a_clean)
    mx = np.nanmax(a_clean)
    med = np.nanmedian(a_clean)
    p25 = np.nanpercentile(a_clean, 25)
    p75 = np.nanpercentile(a_clean, 75)
    print(f"{name}: n={n}, mean={mean:.4f}, std={std:.4f}, min={mn:.4f}, 25%={p25:.4f}, med={med:.4f}, 75%={p75:.4f}, max={mx:.4f}")

# print stats
print_stats("Doppie", d_arr)
print_stats("Triple", t_arr)
print_stats("Triple/Doppie (ratio)", ratio)
# for flag show counts and fraction true
total = f_num.size
true_count = int(np.sum(f_num))
false_count = total - true_count
print(f"Flag: total={total}, true={true_count}, false={false_count}, fraction_true={true_count/total:.4f}")

# Plots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))

# Doppie histogram
axes[0, 0].hist(d_arr[~np.isnan(d_arr)], bins=20, color='C0', alpha=0.7)
axes[0, 0].set_title("Doppie distribution")
axes[0, 0].set_xlabel("Doppie")
axes[0, 0].set_ylabel("Count")

# Triple histogram
axes[0, 1].hist(t_arr[~np.isnan(t_arr)], bins=20, color='C1', alpha=0.7)
axes[0, 1].set_title("Triple distribution")
axes[0, 1].set_xlabel("Triple")
axes[0, 1].set_ylabel("Count")

# Ratio histogram
axes[1, 0].hist(ratio[~np.isnan(ratio)], bins=20, color='C2', alpha=0.7)
axes[1, 0].set_title("Triple / Doppie ratio")
axes[1, 0].set_xlabel("Ratio")
axes[1, 0].set_ylabel("Count")

# Flag bar chart
labels = ['False', 'True']
counts = [false_count, true_count]
axes[1, 1].bar(labels, counts, color=['C3', 'C4'], alpha=0.8)
axes[1, 1].set_title("Flag counts")
axes[1, 1].set_ylabel("Count")

plt.tight_layout()
plt.savefig("sim_stats_summary.png", dpi=150)

# additional scatter: triple vs doppie
plt.figure(figsize=(6, 5))
plt.scatter(d_arr, t_arr, alpha=0.7)
plt.title("Triple vs Doppie")
plt.xlabel("Doppie")
plt.ylabel("Triple")
plt.grid(True)
plt.savefig("sim_triple_vs_doppie.png", dpi=150)

plt.show()