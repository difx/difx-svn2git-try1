"""
from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/107747 
I added call method, by which it acts like a list

Not absolutely necessary, in fact the vex definition actually says that the
order shouldn't matter. So it would probably be better to do away with the
odict and properly sort everything (e.g. scans by start time, etc.)

Nevertheless, it's very convenient to use, for examples, the order the
telescopes occur in the vex file as the order for the various 

telescope tables.


TODO Another option would be to use the ordered dictionary module here:
http://www.voidspace.org.uk/python/odict.html
"""
from UserDict import UserDict
class Odict(UserDict):
    """
    Extended dictionary class which is ordered
    """

    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)

    def __call__(self, r1, r2 = 'default'):
        if r2 == 'default':
            return self.values()[r1]
        else:
            return self.values()[r1:r2]

    def __len__(self):
        return len(self.values())

class VexList(list):
    """
    Identical to list

    Used solely to distinguish lists generated by VexDict.__setitem__ from normal lists
    """
    pass

class VexDict(Odict):
    """
    Inherits everything from odict. Only refinement for vex files is that if
    you try to add an item to the dictionary which already exists, the existing
    item is converted into a list and the new item is added to that item as a list
    """

    def __setitem__(self, key, item):
        if not key in self._keys:
            Odict.__setitem__(self, key, item)
        else:
            if isinstance(self.__getitem__(key), VexList):
                self.__getitem__(key).append(item)
            else:
                Odict.__setitem__(self, key, VexList([self.__getitem__(key), item]))
