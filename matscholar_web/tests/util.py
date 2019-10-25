import inspect
import unittest

import dash_html_components as html


"""
Utilities for running tests.
"""


def get_all_functions_in_module(module):
    """
    Get all the functions in a module.

    Will only get functions defined _in that module_! If they are imported
    from elsewhere they will not be fetched!

    Args:
        module (python module): The module.

    Returns:
        functions ({str: function}): A dictionary of function names and the
            first-class function objects.
    """
    name_func_tuples = inspect.getmembers(module, inspect.isfunction)
    name_func_tuples = [t for t in name_func_tuples if
                        inspect.getmodule(t[1]) == module]
    functions = dict(name_func_tuples)
    return functions


class MatScholarWebBaseTest(unittest.TestCase):
    def run_test_for_all_functions_in_module(self, module, exclude):
        functions = get_all_functions_in_module(module)
        for fname, f in functions.items():
            if fname in exclude:
                print(f"Skip: {fname}")
                continue
            else:
                print(f"Test: {fname}")
                params = inspect.signature(f).parameters
                n_args = len(params)
                if n_args == 0:  # this function takes no args
                    o = f()
                    if "_html" in fname:
                        self.assertTrue(isinstance(o, html.Div))
                    else:
                        self.assertFalse(isinstance(o, html.Div))
                else:
                    fake_args = ["arg"] * n_args
                    o = f(*fake_args)
                    if "_html" in fname:
                        self.assertTrue(isinstance(o, html.Div))
                    else:
                        self.assertFalse(isinstance(o, html.Div))