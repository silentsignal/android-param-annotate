Android parameter annotator for Dalvik/Smali disassembly
========================================================

Debugging applications without access to the source code always has its
problems, especially with debuggers that were built with developers in
mind, who obviously doesn't have this restriction.

The Dalvik implementation of JDWP refuses to give any information about
parameters at all if the DEX file was built without local variable
information, making debugging with JDB difficult.

This simple Python script reads each Smali file and populates this
metadata that can be extracted from the mangled function name found in
the Dalvik bytecode.

Read more in [our blog post about this script](https://blog.silentsignal.eu/2016/06/16/accessing-local-variables-in-proguarded-android-apps/)

Usage
-----

	python3 annotate.py <root directory of smali files>

Dependencies
------------

 - Python 3.x (tested on 3.5.1)

License
-------

The whole project is available under MIT license, see `LICENSE.txt`.
