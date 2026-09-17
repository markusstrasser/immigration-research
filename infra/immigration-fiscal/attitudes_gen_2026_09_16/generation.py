"""Birthplace generation coding; unknown parent branches stay unknown."""
import numpy as np
import pandas as pd


def gss_generation(born, parborn):
    """GSS PARBORN: 1/2/4/6/8 establish a foreign-born parent; 3/5/7 do not."""
    generation = pd.Series(np.nan, index=born.index)
    generation.loc[born.eq(2)] = 1
    generation.loc[born.eq(1) & parborn.isin([1, 2, 4, 6, 8])] = 2
    generation.loc[born.eq(1) & parborn.eq(0)] = 3
    return generation
