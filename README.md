<!-- -*- encoding: utf-8 -*- -->

pymztbas2txt.py
===============

Convert SP-5030/S-BASIC/Hu-BASIC program to text.

Usage
-----

```bat
python pymztbas2txt.py --target sp5030 MZT_FILE
python pymztbas2txt.py --target sbasic MZT_FILE
python pymztbas2txt.py --target hubasic MZT_FILE

python pymztbas2txt.py --target hubasic --jp MZT_FILE

python pymztbas2txt.py --target hubasic MZT_FILE > temp.txt

python pymztinfo.py --help

python pymztinfo.py --verison
```

or

```bat
pymztbas2txt.exe --target sp5030 MZT_FILE
pymztbas2txt.exe --target sbasic MZT_FILE
pymztbas2txt.exe --target hubasic MZT_FILE
```

Testing environment
-------------------

* Windows 10 x64
* Python 2.7.16 32bit

Files
-----

* pymztbas2txt.py ... main script
* mkexe.bat ... make exe file, request py2exe
* setup.py ... py2exe config file

License
-------

pymztbas2txt.py : CC0 / Public Domain

Author
------

by mieki256
