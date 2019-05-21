<!-- -*- encoding: utf-8 -*- -->

pymztbas2txt.py
===============

Convert SP-5030 / MZ-700 S-BASIC / MZ-700 Hu-BASIC program to text.

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


```bat
> pymztbas2txt --help
usage: pymztbas2txt [-h] [--version] [--target {sp5030,hubasic,sbasic}] [--jp]
                    INFILE

Convert BASIC program in MZT file to text.

positional arguments:
  INFILE                .mzt file

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --target {sp5030,hubasic,sbasic}
                        target BASIC. SP-5030, S-BASIC, Hu-BASIC
  --jp                  output japanese character
```


Note
----

* ASCII code 0x00 - 0x1f : output "{00}" "{01}" ... "{1E}" "{1F}"
* ASCII code 0x5e - 0xff : output "{5E}" "{5F}" ... "{FE}" "{FF}"

When using --jp option, output using full-width katakana.


Testing environment
-------------------

* Windows 10 x64 1809
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
