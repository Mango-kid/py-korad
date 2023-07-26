# py-korad
Korad Test & Measurement Equipment Python Library

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)

This is the start of a repository to unify the Korad device drivers into a single repository. This is currently under development and notes will be shown below on what support is currently avaliable.

**Check out the Wiki for more info**

## KEL103 30A 120V DC Electronic Load
- Ethernet Interface: Currently a work in progress with many features tested and working
- USB Interface: WIP

## KA P Series Power Supplies (ie. KA6003P)
I will most likely pull this from one of the existing Korad Serial libraries.

## KD P Series Power Supplies
Once I have compared the SCPI command set between this device and the KA series hopefully we will just be able to unify these into a single class.
