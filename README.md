# greek_scansion

greek_scansion is designed to automatically annotate Ancient Greek hexameter. That is, it tries, for any valid hexameter verse, to find the correct sequence of long and short syllables.

The repository contains the program code and two evaluation scripts. Further information on both is provided in the appropriate folders. Since this project is the result of academic work, the folder **thesis** contains a long explanation on the project's motivation, background, and implementation details (in German). English readers in search of more detailed documentation can try their luck on some of the visuals in section 4.4 of the thesis document.

The project is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike license.

If you use the program, please, don't forget to cite this website or the thesis provided in the like-named folder.

## Requirements and setup

### Machine

The project has been developed and tested on a Windows 10 machine, using Python 3.6.4.

### Obligatory requirements

The finite-state automata have been implemented using the [transitions module by Alexander Neuman](https://github.com/pytransitions/transitions).

The finite-state transducer uses the  [Helsinki Finite-State Tools](https://github.com/hfst/python/wiki).

### If needed

I exported my Greek verses from a heritage MySQL database, using a [MySQL Python Connector](https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html). If you have a similar requirement, you might consider trying this. Otherwise, you obviously don't need to bother.

I also tried out the [syllabification module by James Tauber](https://github.com/jtauber/greek-accentuation). In the end, I didn't use it for my annotations, so if you don't want to install it, you can get rid of this part of the code.

The baseline script references the [Classical Language Toolkit (CLTK)](http://docs.cltk.org/en/latest/). On my machine, I managed to run this only from the Ubuntu subsystem. AND it actually does not properly annotate hexameter verses. So this dependency is very much an optional one.

A reasonable baseline can be got from [Hope Ranker's hexameter library](https://github.com/epilanthanomai/hexameter).