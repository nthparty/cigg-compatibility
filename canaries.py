"""Library for loading dynamic library files.

Python library for choosing and loading dynamic library
files compatible with the operating environment.
"""

import doctest
import sys
import platform
import ctypes

class canaries():
    """
    Wrapper class for static methods.
    """

    @staticmethod
    def canary(system, path):
        """
        Attempt to load a library file at the supplied path
        and verify that its exported functions work.
        """
        lib = None

        try:
            # Load the library.
            if system == 'Windows':
                lib = ctypes.windll.LoadLibrary(path)
            else:
                lib = ctypes.cdll.LoadLibrary(path)

            if lib is not None:
                try:
                    # Confirm that the library's exported functions work.
                    treat = ctypes.create_string_buffer(5)
                    for (i, c) in enumerate(["t", "r", "e", "a", "t"]):
                        treat[i] = c
                    chirp = ctypes.create_string_buffer(5)
                    r = lib.canary(chirp, treat)
                    if r != 0 or\
                       chirp.raw != 'chirp':
                        print("return:", r)
                        print("chirp:", chirp.raw, 'chirp')
                        lib = None
                except:
                    lib = None
                    print('Error: {}. {}, line: {}'.format(
                        sys.exc_info()[0],
                        sys.exc_info()[1],
                        sys.exc_info()[2].tb_lineno
                    ))
        except:
            pass
            print('Error: {}. {}, line: {}'.format(
                sys.exc_info()[0],
                sys.exc_info()[1],
                sys.exc_info()[2].tb_lineno
            ))

        return lib

    @staticmethod
    def load(paths):
        """
        Attempt to load a library at one of the supplied
        paths based on the platform.
        """
        if not isinstance(paths, (str, list, dict)):
            raise ValueError(
                "input must be a string, list, or dictionary"
            )

        if isinstance(paths, dict) and\
           not all(isinstance(p, (str, list)) for p in paths.values()):
            raise ValueError(
                "path values in dictionary must be strings or lists"
            )

        lib = None
        system = platform.system()
        if isinstance(paths, str):
            lib = canary(system, paths)

        elif isinstance(paths, list):
            for path in paths:
                lib = canary(system, path)
                if lib is not None:
                    break

        elif isinstance(paths, dict):
            if system in paths:
                ps = paths[system]
                for path in [ps] if isinstance(ps, str) else ps:
                    lib = canary(system, path)
                    if lib is not None:
                        break

        return lib

# Provide direct access to methods.
canary = canaries.canary
load = canaries.load

if __name__ == "__main__":
    doctest.testmod()
