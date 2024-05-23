# -*- coding: utf-8 -*-
"""
Created on Thurs May 23 10:11 2024
Snippet for extracting RDKit chemical features
@author: Joe Raso
"""

import numpy as np
from rdkit.Chem import Descriptors

# The list of available features is in Descriptors.descList, as
# (name, function) tuples. This includes the fragments.
# Let's repackackage as dicts for convienience.
FEATURES = {
    name:func for name, func in Descriptors.descList if "fr_" not in name}
FRAGMENTS = {
    name:func for name, func in Descriptors.descList if "fr_" in name}


def rdkit_features(mol, ipc_avg=True, array=False):
    """Return the non-fragment RDKit features of a molecule, as a
    dictionary, or as an array if requested."""

    # "IPC" features can be extremely large. Adding the "avg" Keyword
    # can help.
    def feature(name, func):
        if name == "Ipc" and ipc_avg = True:
            return func(mol, avg=True)
        else: return func(mol)

    features = {
        name:feature(name, func) for name, func in FEATURES.items()}

    if array:
        return np.array([v for _, v in features.items()])
    else: return features

def rdkit_fragments(mol):
    """Returns the molecular fragments in a moleule"""
    # Let's also strip off the "fr_" prefix
    return {name.strip("fr"):func(mol) for name, func in FRAGMENTS.items()}
