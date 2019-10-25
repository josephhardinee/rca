# -*- coding: utf-8 -*-
"""
==========================
Mapping (:mod:`rca`)
==========================
.. current modules:: rca
Py-ART has a robust function for mapping radar data from the collected radar
coordinates to Cartesian coordinates.
.. autosummary::
    :toctree: generated/
    plot
"""

from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
