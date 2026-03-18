import numpy as np
import scipy.stats as sp
from typing import Callable
import inspect

def bootstrap( data: np.ndarray):
    return np.random.choice( data , size = len(data) , replace=True)

def likelyhood( data: np.ndarray , model: Callable , *args , **kwargs):
    sig = inspect.signature(model).parameters
    if len(args) != len(sig) and len(kwargs) != len(sig):
        raise ValueError("wrong number of params")

    likelyhood = np.prod( model( data , *args , **kwargs))
    return likelyhood


def NLL( data: np.ndarray , model: Callable , *args , **kwargs):
    sig = inspect.signature(model).parameters
    if len(args) != len(sig) and len(kwargs) != len(sig):
        raise ValueError("wrong number of params")

    NLL = np.sum( -np.log(model( data , *args , **kwargs)))
    return NLL 

