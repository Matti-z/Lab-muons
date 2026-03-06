import numpy as np
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL, ExtendedUnbinnedNLL
from scipy.stats import expon, norm, uniform, chi2
from collections.abc import Callable
import plotly.graph_objects as go
import inspect

#! Funzione per generalizzare la funzione usando la lunghezza del dataset
def function_generator_with_variable_N(func: Callable, N: int):
    sig = inspect.signature(func)
    if "x" not in sig.parameters or "N" not in sig.parameters:
        raise SyntaxError("function defined wrong: it needs an x as first parameter and N as other parameter")
    def wrapper(x, *args, **kwargs):
        return func(x, N, *args, **kwargs)

    wrapper.__signature__ = inspect.Signature(
        [inspect.Parameter('x', inspect.Parameter.POSITIONAL_OR_KEYWORD)] +
        list(inspect.signature(func).parameters.values())[2:]
    )


    return wrapper

def dataset_analysis(dataset: np.ndarray , creator: Callable, bins: int , args: dict) -> Minuit:
    model_function = function_generator_with_variable_N( creator , len(dataset))
    count, edges = np.histogram( dataset , bins=bins) 
    cost = ExtendedBinnedNLL(count, edges, model_function)

    # Snippet to fix a different order between the function definition and args
    sig = str(inspect.signature(model_function))
    sig_list = sig.removeprefix("(").removesuffix(")").split(", ")
    keys = list(args.keys())


    
    if( not all([k in sig_list for k in keys])):
        print( sig_list)
        print(keys) 
        raise KeyError("args is missing a key")
    sig_list.remove("x")
    sorted_args = {k: args[k] for k in sig_list}


    minuit_element =  Minuit(cost, *sorted_args.values())
    
    if "A" in args.keys():
        minuit_element.fixed["A"] = True

    return minuit_element

def unbinned_data_analysis(dataset: np.ndarray , creator: Callable, args: dict) -> Minuit:
    model_function = function_generator_with_variable_N( creator , len(dataset))
    cost = ExtendedUnbinnedNLL(dataset , model_function)

    # Snippet to fix a different order between the function definition and args
    sig = str(inspect.signature(model_function))
    sig_list = sig.removeprefix("(").removesuffix(")").split(", ")
    keys = list(args.keys())


    
    if( not all([k in sig_list for k in keys])):
        print( sig_list)
        print(keys) 
        raise KeyError("args is missing a key")
    sig_list.remove("x")
    sorted_args = {k: args[k] for k in sig_list}


    minuit_element =  Minuit(cost, *sorted_args.values())
    
    if "A" in args.keys():
        minuit_element.fixed["A"] = True

    return minuit_element


def end(m:Minuit) -> None:
    m.migrad()
    m.hesse()
    display(m)


def find_best_chi2_pvalue( min_bin_range:int , max_bin_range:int , step_bin: int,  f:Callable , dataset:np.ndarray , f_args:dict):
    range_bins = np.arange(min_bin_range , max_bin_range , step_bin , dtype=int)

    p_value_list = []
    chi2_list = []
    for bin in range_bins:
        n = dataset_analysis( dataset , f , bins = bin , args=f_args)
        n.migrad()
        n.hesse()
        p_value_list.append(1 - chi2.cdf(n.fval, df=n.ndof))
        chi2_list.append(n.fval/n.ndof)
    return p_value_list , chi2_list