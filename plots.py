from scipy.stats import expon, uniform
import numpy as np
import matplotlib.pyplot as plt
from iminuit import Minuit
from matplotlib.ticker import FuncFormatter


class plots:
    def __init__(self, dataset , m:Minuit , label_x , label_y) -> None:
        self.dataset = dataset
        self.interp = m
        self.label_x = label_x
        self.label_y = label_y
        self.range = (min(dataset), max(dataset))
        self.exp_n = (len(self.interp.values)-1)/2
        self.fig = plt.figure()
        self.fig.tight_layout()
        self.setup_figure()
        pass

    def setup_figure(self):
        self.ax = self.fig.add_subplot()
        print(self.fig.get_children())
        self.ax.set_xlim(*self.range)
        self.ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p: f'{x*1e6:.1f}'))
        self.ax.set_ylabel( self.label_y )
        self.ax.set_xlabel( self.label_x )
        
        

    def __generate_dataset__(self , loc , scale , sp_func , prob):
        # do not generate data if probability is non-positive
        if prob <= 0:
            prob = 0
        return sp_func.rvs(loc, scale , int(prob*len(self.dataset)))
    
    def __single_exp_colour_incremental_plot__(self , bin_count , density = False ):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        a = np.random.poisson(total_count)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="orange" , alpha = 0.2)
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , alpha = 0.5)
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen")

    def __single_exp_colour_plot__( self, bin_count, density = False , label = []):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()
        
        str = '''3 labels are needed:
        1) dataset
        2) exponential
        3) uniform'''

        if len(label)<3:
            raise ValueError(str)

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"])

        bin_edges = np.linspace(*self.range , bin_count+1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


        total_count , _ = np.histogram(self.dataset , bins = bin_count , range = self.range , density=density)
        exp_count , _ = np.histogram(data_exp1 , bins = bin_count , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_count , range = self.range , density=density)
        print( len(total_count) , len(bin_centers) , bin_count)
        a = np.random.poisson(total_count)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="black" , histtype="step", linestyle="-")
        self.ax.hist(data_exp1 , bins = bin_count , range = self.range , density = density, color="orange" , alpha = 0.2)
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , alpha = 0.5)
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black" , label = label[0])
        self.ax.errorbar( bin_centers , exp_count , np.sqrt(exp_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkorange" , label = label[1])
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen" , label = label[2])
        self.fig.legend()


    def __single_exp_bar_incremental_plot__(self , bin_count , density = False):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="orange" , histtype="step", linestyle="--")
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , histtype="step", linestyle=":")
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black")
        self.ax.errorbar( bin_centers , exp_count , np.sqrt(exp_count) , 12e-9 , fmt="o" , markersize=3 , color="darkorange")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen")

    def __single_exp_bar_plot__(self , bin_count , density = False):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(data_exp1 , bins = bin_count , range = self.range , density = density, color="orange" , histtype="step", linestyle="--")
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , histtype="step", linestyle=":")
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black")
        self.ax.errorbar( bin_centers , exp_count , np.sqrt(exp_count) , 12e-9 , fmt="o" , markersize=3 , color="darkorange")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen")

    def __double_exp_colour_incremental_plot__(self , bin_count , density = False):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_exp2 = self.__generate_dataset__( 0 , self.interp.values["tau2"], expon , self.interp.values["freq_exp2"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"]-self.interp.values["freq_exp2"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2


        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp1_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        exp2_count , _ = np.histogram(data_exp2 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="orange" , alpha = 0.2)
        self.ax.hist( np.concatenate([data_exp2 , data_unif]) , bins = bin_count , range = self.range , density = density, color="violet" , alpha = 0.4)
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , alpha = 0.6)
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black")
        self.ax.errorbar( bin_centers , exp2_count+unif_count , np.sqrt(exp2_count+unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen")

    def __double_exp_colour_plot__(self , bin_count , density = False , label = []):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        str = '''3 labels are needed:
        1) dataset
        2) bigger exponential
        3) smaller exponential
        3) uniform'''

        if len(label)<4:
            raise ValueError(str)

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp"]*(1-self.interp.values["relative_freq"]))
        data_exp2 = self.__generate_dataset__( 0 , self.interp.values["tau2"], expon , self.interp.values["freq_exp"]*self.interp.values["relative_freq"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp"])

        bin_edges = np.linspace(*self.range , bin_count+1)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        total_count , _ = np.histogram(self.dataset , bins = bin_count , range = self.range , density=density)
        exp1_count , _ = np.histogram(data_exp1 , bins = bin_count , range = self.range , density=density)
        exp2_count , _ = np.histogram(data_exp2 , bins = bin_count , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_count , range = self.range , density=density)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="black" , histtype="step", linestyle="-")
        self.ax.hist(data_exp1 , bins = bin_count , range = self.range , density = density, color="orange" , alpha = 0.2)
        self.ax.hist(data_exp2 , bins = bin_count , range = self.range , density = density, color="violet" , alpha = 0.4)
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , alpha = 0.5)
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , fmt = "o" , markersize=3 , color = "black" , label = label[0])
        self.ax.errorbar( bin_centers , exp1_count , np.sqrt(exp1_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkorange", label = label[1])
        self.ax.errorbar( bin_centers , exp2_count , np.sqrt(exp2_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkviolet", label = label[2])
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , fmt = "o" , markersize=3 , color = "darkgreen", label = label[3])
        self.fig.legend()
        

    def __double_exp_bar_incremental_plot__(self , bin_count , density = False):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_exp2 = self.__generate_dataset__( 0 , self.interp.values["tau2"], expon , self.interp.values["freq_exp2"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"]-self.interp.values["freq_exp2"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp1_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        exp2_count , _ = np.histogram(data_exp2 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(self.dataset , bins = bin_count , range = self.range , density = density, color="orange" , histtype="step")
        self.ax.hist( np.concatenate([data_exp2 , data_unif]) , bins = bin_count , range = self.range , density = density, color="violet" , histtype="step")
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , histtype="step")
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , markersize=3, fmt = "o" , color = "black")
        self.ax.errorbar( bin_centers , exp2_count+unif_count , np.sqrt(exp2_count+unif_count) , 12e-9 , markersize=3, fmt = "o" , color = "darkviolet")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , markersize=3, fmt = "o" , color = "darkgreen")

    def __double_exp_bar_plot__(self , bin_count , density = False):
        if len(self.fig.get_children())<1:
            self.fig.clear()
            self.setup_figure()

        data_exp1 = self.__generate_dataset__( 0 , self.interp.values["tau1"] , expon , self.interp.values["freq_exp1"])
        data_exp2 = self.__generate_dataset__( 0 , self.interp.values["tau2"], expon , self.interp.values["freq_exp2"])
        data_unif = self.__generate_dataset__( *self.range , uniform , 1-self.interp.values["freq_exp1"]-self.interp.values["freq_exp2"])

        bin_edges = np.linspace(*self.range , bin_count)
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        total_count , _ = np.histogram(self.dataset , bins = bin_edges , range = self.range , density=density)
        exp1_count , _ = np.histogram(data_exp1 , bins = bin_edges , range = self.range , density=density)
        exp2_count , _ = np.histogram(data_exp2 , bins = bin_edges , range = self.range , density=density)
        unif_count , _ = np.histogram(data_unif , bins = bin_edges , range = self.range , density=density)

        self.ax.hist(data_exp1 , bins = bin_count , range = self.range , density = density, color="orange" , histtype="step", linestyle="--")
        self.ax.hist(data_exp2 , bins = bin_count , range = self.range , density = density, color="violet" , histtype="step", linestyle=":")
        self.ax.hist( data_unif, bins = bin_count , range = self.range , density = density, color="green" , histtype="step", linestyle=":")
        self.ax.hist( self.dataset , bins = bin_count , range = self.range , density=density , color= "black" , histtype="step")
        self.ax.errorbar( bin_centers , total_count , np.sqrt(total_count) , 12e-9 , markersize=3, fmt = "o" , color = "black")
        self.ax.errorbar( bin_centers , exp1_count , np.sqrt(exp1_count) , 12e-9 , markersize=3, fmt="o" , color="darkorange")
        self.ax.errorbar( bin_centers , exp2_count , np.sqrt(exp2_count) , 12e-9 , markersize=3, fmt = "o" , color = "darkviolet")
        self.ax.errorbar( bin_centers , unif_count , np.sqrt(unif_count) , 12e-9 , markersize=3, fmt = "o" , color = "darkgreen")

    def colour_plot_incremental(self , bin_count, density , labels):
        if self.exp_n == 1:
            self.__single_exp_colour_incremental_plot__(bin_count, density )
        if self.exp_n == 2:
            self.__double_exp_colour_incremental_plot__(bin_count, density)
        return self.fig

    def colour_plot(self , bin_count, density, label):
        if self.exp_n == 1:
            self.__single_exp_colour_plot__(bin_count, density, label)
        if self.exp_n == 2:
            self.__double_exp_colour_plot__(bin_count, density , label)
        return self.fig

    def bar_plot_incremental(self , bin_count, density):
        if self.exp_n == 1:
            self.__single_exp_bar_incremental_plot__(bin_count, density)
        if self.exp_n == 2:
            self.__double_exp_bar_incremental_plot__(bin_count, density)
        return self.fig

    def bar_plot(self , bin_count, density):
        if self.exp_n == 1:
            self.__single_exp_bar_plot__(bin_count, density)
        if self.exp_n == 2:
            self.__double_exp_bar_plot__(bin_count, density)
        return self.fig
        


if __name__ == "__main__":

    from library import dataset_analysis, end

    def normalization( model, min_dataset: int , max_dataset:int) -> float:
        cdf_diff = model.cdf(max_dataset) - model.cdf(min_dataset)
        return float(np.asarray(cdf_diff).item())

    def exp_unif(x, N , min , max , freq_exp1, tau1, A):
        exp = expon( loc = A , scale = tau1)
        return freq_exp1 * N * exp.cdf(x)/normalization(exp , min , max) + (1-freq_exp1) * N * uniform.cdf(x, min, max)

    def double_exp_unif( x , N , min , max,  freq_exp1 , freq_exp2 , tau1 , tau2 , A ):
        exp1 = (expon( loc = A , scale = tau1)) 
        exp2 = expon( loc = A , scale = tau2)
        return freq_exp1 * N * exp1.cdf(x)/normalization( exp1 , min , max) + (freq_exp2) * N * exp2.cdf(x)/normalization(exp2, min , max) + (1 - freq_exp1 - freq_exp2) * N * (uniform.cdf(x, min, max))




    salt_1 = np.genfromtxt("Data/timestamp/salt_27_03_2026_16_36.csv" , delimiter=",")
    salt_2 = np.genfromtxt("Data/timestamp/salt_31_03_2026_11_01.csv" , delimiter=",")
    salt_3 = np.genfromtxt("Data/timestamp/salt_08_04_2026_11_16.csv" , delimiter=",")
    salt_4 = np.genfromtxt("Data/timestamp/salt_10_04_2026_17_02.csv" , delimiter=",")
    salt_5 = np.genfromtxt("Data/timestamp/salt_13_04_2026_12_15.csv" , delimiter=",")

    data_0 = np.concatenate([salt_1, salt_2, salt_3, salt_4, salt_5])
    # ensure monodimensional array
    if data_0.ndim > 1:
        # if there's an extra column, drop it (keep first column)
        if data_0.shape[1] > 1:
            data_0 = data_0[:, 0]
            # collapse shape (N,1) to (N,)
            data_0 = data_0.ravel()

    
    data_0 = data_0[data_0>2.5e-7]
    double_exp_unif_args = {"freq_exp1": 0.1, "freq_exp2":0.9,  "tau1": 2e-6 , "tau2":2e-6, "A":0}

    # call dataset_analysis with positional args in correct order
    full_analysis = dataset_analysis(data_0, double_exp_unif, 80, double_exp_unif_args)
    # set parameter limits individually
    full_analysis.limits["freq_exp1"] = (0, 1)
    full_analysis.limits["freq_exp2"] = (0, 1)
    full_analysis.limits["tau1"] = (2e-6, 3e-6)
    end(full_analysis , False)


    a = plots(data_0 , full_analysis , "time" , "count")
    fig1 = a.colour_plot_incremental(80 , False)

    b = plots(data_0 , full_analysis , "time" , "count")
    fig2 = b.colour_plot(80,False)

    c = plots(data_0 , full_analysis , "time" , "count")
    fig3 = c.bar_plot_incremental(80 , False)

    d = plots(data_0 , full_analysis , "time" , "count")
    fig4 = d.bar_plot(80,False)
    plt.show()




