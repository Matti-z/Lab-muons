
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import os
from pathlib import Path
from numba import jit


path = str(Path("Lab-muons/pippo"))
out_path =str(Path('Lab-muons/pippo_out')) 
delta_val = 500
n = int(1e5)
i = 0
frequency = 2.5e8




def normalize_data(x: np.ndarray):
    """Restituisce un array binario dove 1 indica valori sotto la soglia.

    NOTA: questa funzione non viene usata nella versione corretta
    perché rende difficile rilevare i fronti quando si calcola
    nuovamente `max(data)` su un array già binarizzato.
    """
    return np.where(x < (max(x) - delta_val), 1, 0)

def debug( timestamp, event , time):
    plt.vlines(timestamp , 0 , 2)
    plt.plot(time , event)
    plt.show()


def timestamp_calculator(path: str):
    """Legge tutti i CSV in `path` ed estrae i timestamp dei fronti.

    Ritorna un array `timestamp_list` pieno di valori (float32).
    """
    timestamp_list = np.empty(n, dtype=np.float32)
    i = 0
    file_list = os.listdir(path)
    for id in file_list:
        data = np.genfromtxt(path + "/" + id, delimiter=',', dtype=np.uint16)
        # passiamo i parametri necessari alla funzione di estrazione
        i = extract_timestamps(data, timestamp_list, i, delta_val, frequency)
        perc: int = int(round(int(id.removesuffix(".csv")) /  int(file_list[-1].removesuffix(".csv")) * 30))
        string: str = (
            "[" + "#" * perc + "-" * (30 - perc) + "]\t" + id + "\t" + str(i))
        print("\r" + string, end="", flush=True)
    return timestamp_list

def extract_timestamps(data: np.ndarray, timestamp_list: np.ndarray, i: int, delta_val: int, frequency: float):
    """Estrae i timestamp dei fronti dal vettore `data`.

    Problema originale: il codice binarizzava `data` e poi usava `max(data)`
    sulle stesse quantità binarie (0/1). Poiché `max(data)` diventava 1,
    l'espressione `max(data) - delta_val` era negativa e le condizioni
    per rilevare i fronti non si verificavano mai, quindi `i` non veniva
    mai incrementato (tutti gli elementi rimanevano a 0).

    Soluzione: calcolo esplicitamente il valore massimo originale, ricavo
    la soglia `threshold = maxv - delta_val` e cerco il fronte di discesa
    (da sopra-soglia a sotto-soglia).
    """
    # calcolo manuale del massimo per compatibilità e chiarezza
    maxv = 0
    for idx in range(data.shape[0]):
        if data[idx] > maxv:
            maxv = data[idx]
    threshold = maxv - delta_val

    step = False
    for idx in range(data.shape[0]):
        point = data[idx]
        if point > threshold:
            step = True
        elif point <= threshold and step:
            # fronte di discesa rilevato
            step = False
            timestamp_list[i] = idx / frequency
            i += 1
            if i == timestamp_list.shape[0]:
                raise ValueError("array too small")
    return i


def save_csv(timestamp_list , out_path, out_name):
    csv_filename = str(Path(out_path)) + "/" + out_name
    np.savetxt( csv_filename , timestamp_list , delimiter=",")
            
def timestamp_parser(path , out_path, out_name):
    a = timestamp_calculator( path )
    save_csv(a, out_path, out_name)


