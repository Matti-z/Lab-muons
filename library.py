import inspect
from collections.abc import Callable
from typing import SupportsIndex

import numpy as np
from iminuit import Minuit
from iminuit.cost import ExtendedBinnedNLL, ExtendedUnbinnedNLL
from IPython.display import display


#! Funzione per generalizzare la funzione usando la lunghezza del dataset
def function_generator_with_variable_N(func: Callable, N: int) -> Callable:
    sig = inspect.signature(func)
    if "x" not in sig.parameters or "N" not in sig.parameters:
        raise SyntaxError(
            "function defined wrong: it needs an x as first parameter and N as other parameter"
        )

    def wrapper(x, *args, **kwargs):
        return func(x, N, *args, **kwargs)

    wrapper.__signature__ = inspect.Signature(
        [inspect.Parameter("x", inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        + list(inspect.signature(func).parameters.values())[2:]
    )
    return wrapper


def function_generator_with_min_max(func: Callable, dataset: np.ndarray) -> Callable:
    """Wrap a model function to bind dataset min and max into its signature.

    The provided `func` is expected to accept at least the parameters
    (x, min, max, ...) where `min` and `max` denote the range of the
    dataset. This generator returns a new callable that takes `x` and the
    remaining model parameters, and internally calls `func(x, min(dataset),
    max(dataset), ...)` so callers don't need to supply the range.

    Parameters
    ----------
    func : Callable
        The original model function with signature (x, min, max, ...).
    dataset : np.ndarray
        Array of data; its minimum and maximum values will be passed to
        `func` as the `min` and `max` arguments.

    Returns
    -------
    Callable
        A wrapper function with signature (x, ...) where the `min` and
        `max` parameters have been bound to the dataset range.

    Raises
    ------
    SyntaxError
        If `func` does not have parameters named "x", "min", and "max".
    """
    sig = inspect.signature(func)
    if (
        "x" not in sig.parameters
        or "min" not in sig.parameters
        or "max" not in sig.parameters
    ):
        raise SyntaxError(
            "function defined wrong: it needs parameters 'x', 'min' and 'max'"
        )

    def wrapper(x, *args, **kwargs):
        return func(x, min(dataset), max(dataset), *args, **kwargs)

    wrapper.__signature__ = inspect.Signature(
        [inspect.Parameter("x", inspect.Parameter.POSITIONAL_OR_KEYWORD)]
        + list(inspect.signature(func).parameters.values())[3:]
    )
    return wrapper

def model_function_builder(creator:Callable , dataset):
    model_function = function_generator_with_variable_N(creator, len(dataset))
    sig_params = inspect.signature(model_function).parameters
    if "min" in sig_params and "max" in sig_params:
        model_function = function_generator_with_min_max(model_function, dataset)
    return model_function



def dataset_analysis(
    dataset: np.ndarray, creator: Callable, bins: SupportsIndex, args: dict , model_function = None
) -> Minuit:
    """Create a binned likelihood cost and initialize a Minuit minimizer.

    Parameters
    ----------
    dataset : np.ndarray
        One-dimensional array of observed data points.
    creator : Callable
        A function that builds the model. It must accept (x, N, ...) where
        N is the dataset length; optional `min` and `max` parameters are
        supported and will be supplied from the dataset when present.
    bins : SupportsIndex
        Number of bins or bin edges to use for the histogram.
    args : dict
        Dictionary of initial parameter values keyed by parameter name. The
        keys must match the parameter names of the model function (excluding
        the "x" argument).

    Returns
    -------
    iminuit.Minuit
        A Minuit instance constructed with the binned negative log-likelihood
        cost function and the provided initial parameter values. If the
        parameter "A" is present in args it will be fixed on the returned
        Minuit object.

    Raises
    ------
    KeyError
        If args is missing a key required by the model function.
    """
    if model_function is None:
        model_function = model_function_builder( creator , dataset)

    count, edges = np.histogram(dataset, bins=bins)
    cost = ExtendedBinnedNLL(count, edges, model_function)

    param_names = [
        name for name in inspect.signature(model_function).parameters if name != "x"
    ]
    missing = [name for name in param_names if name not in args]
    if missing:
        raise KeyError(f"args is missing keys: {missing}")

    minuit_element = Minuit(cost, **{name: args[name] for name in param_names})
    if "A" in param_names:
        minuit_element.fixed["A"] = True

    return minuit_element


def dataset_analysis_unbinned(
    dataset: np.ndarray, creator: Callable, args: dict
) -> Minuit:
    """Create an unbinned likelihood cost and initialize a Minuit minimizer.

    Parameters
    ----------
    dataset : np.ndarray
        One-dimensional array of observed data points.
    creator : Callable
        A function that builds the model. It must accept (x, N, ...) where
        N is the dataset length; optional `min` and `max` parameters are
        supported and will be supplied from the dataset when present.
    args : dict
        Dictionary of initial parameter values keyed by parameter name. The
        keys must match the parameter names of the model function (excluding
        the "x" argument).

    Returns
    -------
    iminuit.Minuit
        A Minuit instance constructed with the unbinned negative log-likelihood
        cost function and the provided initial parameter values. If the
        parameter "A" is present in args it will be fixed on the returned
        Minuit object.

    Raises
    ------
    KeyError
        If args is missing a key required by the model function.
    """

    model_function = function_generator_with_variable_N(creator, len(dataset))

    sig_params = inspect.signature(model_function).parameters
    if "min" in sig_params and "max" in sig_params:
        model_function = function_generator_with_min_max(model_function, dataset)

    cost = ExtendedUnbinnedNLL(dataset, model_function)

    param_names = [
        name for name in inspect.signature(model_function).parameters if name != "x"
    ]
    missing = [name for name in param_names if name not in args]
    if missing:
        raise KeyError(f"args is missing keys: {missing}")

    minuit_element = Minuit(cost, **{name: args[name] for name in param_names})
    if "A" in param_names:
        minuit_element.fixed["A"] = True

    return minuit_element


def end(m: Minuit, asym: bool = True) -> None:
    """Run the fit, compute uncertainties, and display the result."""
    m.migrad()
    m.hesse()
    if asym:
        m.minos()
    display(m)
