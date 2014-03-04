Bond valence parameter tools
============================

These are some simple tools for working with bond valence parameters, based on the values accumulated by David I. Brown, available online here: http://www.iucr.org/resources/data/datasets/bond-valence-parameters

Reading a CIF file in Python
----------------------------

The `bvparm.py` script contains a class that makes it easy to read a CIF file containing bond valence parameters and use them from within Python. The extracted data is stored in a nested dictionary attribute, with the cation, anion and their oxidation states being the keys on consecutive levels. Literature references are also parsed, into another dictionary.

An example of basic usage:
```python
import bvparm
>>> bv = bvparm.BondValenceParameters()
Reading parameters from bvparm2013.cif
>>> print bv.source
bvparm2013.cif
>>> print "Oxidation states for iron:", bv['Fe'].keys()
Oxidation states for iron: [9, 2, 3, 4, 6]
>>> print "Anions available for potassium:", bv['K'][1].keys()
Anions available for potassium: ['Cl', 'I', 'H', 'F', 'As', 'O', 'N', 'P', 'S', 'Br', 'Te', 'Se']
>>> print "Parameters available for K-N bonds:", bv['K'][1]['N'][-3]
Parameters available for K-N bonds: [{'ref': 'b', 'b': 0.37, 'r0': 2.26, 'details': '?'}, {'ref': 'e', 'b': 0.37, 'r0': 2.3, 'details': 'unchecked'}]
>>> import math
>>> params = bv['K'][1]['N'][-3][0]
>>> print "This would be the bond valence for K-N at 2.5A: %.3f" % math.exp((params['r0']-2.5)/params['b'])
This would be the bond valence for K-N at 2.5A: 0.523
>>> print "Literature reference for the parameters:", bv.references[params['ref']]
Literature reference for the parameters: Brese and O
```
