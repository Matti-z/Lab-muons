from scipy.stats import expon, uniform
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit

class plots:
    def __init__(self, dataset , m:Minuit , label_x , label_y) -> None:
        self.dataset = dataset
        self.interp = m

        self.range = (min(dataset), max(dataset))
        self.fig = plt.figure( figsize=(10,8))
        self.ax = self.fig.add_subplot()
        self.ax.set_xlim(*self.range)
        self.ax.set_ylabel( label_y )
        self.ax.set_xlabel( label_x )
        self.fig.tight_layout()
        self.exp_n = (len(self.interp.values)-1)/2
        pass

    def __generate_dataset__(self , loc , scale , sp_func , prob):
        return sp_func.rvf(loc, scale , int(prob*len(self.dataset)))
    
    def __single_exp_colour_incremental_plot__(self , bin_count , density = False):
        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"])

        bin_edges = np.linspace(*self.range , bin_count)


        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="yellow")
        





    def colour_plot_incremental(self , bin_count, density):
        if self.exp_n == 1:
            return self.__single_exp_colour_incremental_plot__(bin_count, density)
        




