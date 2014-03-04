Bond valence parameter tools
============================

These are some simple tools for working with bond valence parameters, based on the values accumulated by David I. Brown, available online here: http://www.iucr.org/resources/data/datasets/bond-valence-parameters

Reading a CIF file in Python
----------------------------

The `bvparm.py` script contains a class that makes it easy to read a CIF file containing bond valence parameters and use them from within Python. The extracted data is stored in a nested dictionary attribute, with the cation, anion and their oxidation states being the keys on consecutive levels. Literature references are also parsed, into another dictionary
