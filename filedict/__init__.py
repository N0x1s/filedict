"""
Dict like file to store data(dict) on hard disk for multi access or cache
mainly made for the cproperty project


Classes:

    FileDict

Misc variables:

    __version__
"""
from collections.abc import MutableMapping
from contextlib import suppress
import shutil
import pickle
import os

__version__ = '0.1b'


class FileDict(MutableMapping):
    """
    A class to represent a FileDict.

    ...

    Attributes
    ----------
    dirname : str
        dir name that gonna be used to store data

    _agressive : bool
        if set to True every dict gonna be treated as FileDict even the once
            inside the Parent FileDict
            Example -> exa['persons']['elia']['age']
                all those dict are FileDict
                and has there own dir inside the parent dir
            default -> True

    cached : bool
        if set to True the dir won't be deleted at the end. default -> True


    """

    def __init__(self, dirname, pairs=(), *,
                 agressive=True, hidden=False, cached=True, **kwargs):
        """
        Constructs all the necessary attributes for the person object.

        Parameters
        ----------
        dirname : str
            dir name that gonna be used to store data

        pairs : dict
            a dict to convert to FileDict, this also can be passed as **kw

        agressive : bool
            if set to True every dict gonna be treated as FileDict even
                the once inside the Parent FileDict
                Example -> exa['persons']['elia']['age'] all those dict
                    are FileDict and has there own dir inside the parent dir
                default -> True

        hidden : bool
            if set to True the dir will be hidden. default -> False

        cached : bool
            if set to True the dir won't be deleted at the end. default -> True


        """
        self.dirname = f'.{dirname}' if hidden and dirname[0] != '.' else dirname
        self._agressive = agressive
        self.cached = cached
        with suppress(FileExistsError):
            if os.path.isfile(self.dirname):
                os.remove(self.dirname)
            os.mkdir(self.dirname)
        self.update(pairs, **kwargs)

    def __getitem__(self, key):
        fullname = os.path.join(self.dirname, key)
        try:
            if self._agressive and os.path.isdir(fullname):
                return FileDict(fullname)
            with open(fullname, 'rb') as f:
                return pickle.loads(f.read())
        except FileNotFoundError:
            raise KeyError(key) from None

    def __setitem__(self, key, value):
        fullname = os.path.join(self.dirname, key)
        with suppress(KeyError):
            del self[key]
        if self._agressive and isinstance(value, (dict)):
            FileDict(fullname, **value)
            return
        with open(fullname, 'wb') as f:
            f.write(pickle.dumps(value))

    def __del__(self):
        if not self.cached:
            shutil.rmtree(self.dirname)

    def __delitem__(self, key):
        fullname = os.path.join(self.dirname, key)
        try:
            if os.path.isfile(fullname):
                return os.remove(fullname)
            return shutil.rmtree(fullname)
        except FileNotFoundError:
            raise KeyError(key) from None

    def __len__(self):
        return len(os.listdir(self.dirname))

    def __iter__(self):
        return iter(os.listdir(self.dirname))

    def __str__(self):
        return str(dict(self.items()))

    def __repr__(self):
        return str(self)
