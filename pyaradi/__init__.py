"""
aradi encryption

a simple python package of the NSA ARADI algorithm
"""

from pyaradi.aradi import (
    aradi_ctr_mode,
    encrypt,
    decrypt,
    aradi_process_file,
    aradi_test,
    aradi_test_default,
)

__version__ = "0.1.0"
__author__ = ("A. Purim, G. Praciano",)
