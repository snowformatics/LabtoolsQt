# -*- coding: utf-8 -*-
# from distutils.core import setup
# setup(
#         name = "LabtoolsQt",
#         version = "1.0.1",
#         description = "LabtoolsQt",
#         author = "Stefanie Lück",
#         author_email = "luecks@gmail.com",
#         url = "",
#         package_dir = { "":"src" },
#         packages =  ["labtools_main", "labtools.ui"],
#         scripts = ["labtools_main"],
#         long_description = "bla"
#
#         )
#
#
#
        
from distutils.core import setup
import py2exe
# cd D:\Users\lueck\Google Drive\Python\Software projects\LabtoolsQt\
# python setup.py py2exe

setup(windows=[{"script": "labtools_main.py"}],

      options={"py2exe":
              {"includes": ['sip','decimal', "PyQt4.QtCore", "PyQt4.QtGui", "PyQt4.QtNetwork"],

      #"bundle_files":1,
      #"optimize": 2,
                        "dll_excludes": ["mswsock.dll", "powrprof.dll"]}})

#options = {"build_exe" : {"includes" : "atexit" }}