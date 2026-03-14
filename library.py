from collections.abc import Callable
from typing import SupportsIndex
import inspect
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL, ExtendedUnbinnedNLL
import numpy as np
from IPython.display import display


#! Funzione per generalizzare la funzione usando la lunghezza del dataset
def function_generator_with_variable_N(func: Callable, N: int) -> Callable:
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

def function_generator_with_min_max( func:Callable , dataset:np.ndarray) -> Callable:
    sig = inspect.signature(func)
    if "x" not in sig.parameters or "min" not in sig.parameters or "max" not in sig.parameters:
        raise SyntaxError("function defined wrong: it needs an x as first parameter and N as other parameter")
    def wrapper(x, *args, **kwargs):
        return func(x, min(dataset), max(dataset), *args, **kwargs)

    wrapper.__signature__ = inspect.Signature(
        [inspect.Parameter('x', inspect.Parameter.POSITIONAL_OR_KEYWORD)] +
        list(inspect.signature(func).parameters.values())[3:]
    )
    return wrapper

def dataset_analysis(dataset: np.ndarray , creator: Callable, bins: SupportsIndex, args: dict) -> Minuit:
    model_function = function_generator_with_variable_N( creator , len(dataset))
    sig_params = inspect.signature(model_function).parameters
    if "min" in sig_params and "max" in sig_params:
        model_function = function_generator_with_min_max( model_function , dataset)
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
    
    if "A" in sorted_args.keys():
        minuit_element.fixed["A"] = True

    return minuit_element


def dataset_analysis_unbinned(dataset: np.ndarray , creator: Callable, args: dict) -> Minuit:
    model_function = function_generator_with_variable_N( creator , len(dataset))

    sig_params = inspect.signature(model_function).parameters
    if "min" in sig_params and "max" in sig_params:
        model_function = function_generator_with_min_max( model_function , dataset)

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
    
    if "A" in sorted_args.keys():
        minuit_element.fixed["A"] = True

    return minuit_element


def end(m:Minuit, asym: bool = True) -> None:
    m.migrad()
    m.hesse()
    if asym:
        m.minos()
    display(m)