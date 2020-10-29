import os
import unittest
import tempfile
from filedict import FileDict
import pathlib
dirname = None


class TestFileDict(unittest.TestCase):
    testdict = dict(zip(map(str, range(5)), range(5, 1, -1)))
    testdict['1'] = testdict.copy()

    def test_dict(self):
        tmpdict = FileDict(tempfile.mkdtemp(), pairs=self.testdict)
        self.assertDictEqual(dict(tmpdict), self.testdict)

        tmpdict = FileDict(tempfile.mkdtemp(), **self.testdict)
        self.assertDictEqual(dict(tmpdict), self.testdict)

    def test_items(self):
        tmpdict = FileDict(tempfile.mkdtemp(), **self.testdict)
        self.assertEqual(tmpdict.items(), self.testdict.items())

    def test_hidden_mode(self):
        tmpdir = tempfile.mkdtemp()
        tmpdict = FileDict(tmpdir, hidden=True)
        tmpdir = pathlib.Path(tmpdir)
        hiddendir = os.path.join(tmpdir.parent,
                                 f'.{tmpdir.name}')
        self.assertEqual(str(tmpdict.dirname), hiddendir)
        self.assertTrue(os.path.isdir(hiddendir) and os.path.exists(hiddendir))

    def test_cached_mode(self):
        tmpdir = tempfile.mkdtemp()
        tmpdict = FileDict(tmpdir, cached=False)
        self.assertTrue(os.path.exists(tmpdir))
        del tmpdict
        self.assertFalse(os.path.exists(tmpdir))
        # agressive=True, hidden=False, cached=True,

    def test_cache(self):
        tmpdir = tempfile.mkdtemp()
        tmpdict = FileDict(tmpdir, **self.testdict)
        tmpdict1 = FileDict(tmpdir)
        self.assertDictEqual(dict(tmpdict), dict(tmpdict1))
        del tmpdict['2']
        self.assertDictEqual(dict(tmpdict), dict(tmpdict1))

    def test_agressive_mode(self):
        tmpdict = FileDict(tempfile.mkdtemp(), **self.testdict)
        tmpdict1 = FileDict(tempfile.mkdtemp(), agressive=False)
        subdict = os.path.join(tmpdict.dirname, '1')
        subdict1 = os.path.join(tmpdict1.dirname, '1')

        self.assertTrue(os.path.exists(subdict) and os.path.isdir(subdict))
        self.assertFalse(os.path.exists(subdict1) and os.path.isdir(subdict1))


if __name__ == '__main__':
    unittest.main()
