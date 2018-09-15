puzzle-tools
============

Some tools for solving MIT Mystery Hunt puzzles

Features
========
* Codes
	* `amino` - nucleotide and amino acid sequences
	* `braille` - Braille
	* `morse` - Morse code
	* `semaphore` - flag semaphore
	* `code_misc` - other codes (currently just military time zones)
* Data sets
	* `enumerations` - data sets: chemical elements, US states
	* `enumerations_web` - various data sets that can be downloaded from the web.  Includes lists of countries, resistor colors, zodiac symbols, currencies, languages, MIT classes, subway stations, airports, airlines, and stock symbols.
	* `subway` -  more lists of subway stations that can be downloaded from the web
* Properties of words
	* `word_properties` - functions for determining if a word has a particular property (e. g. being a cryptogram of a particular other word).
* Domain-specific wordlist generators
	* `wordlists.imdb` - generates lists of well-known actors, directors, movies, and television shows using data from IMDb
	* `wordlist.names` - generates lists of common American first names using data from the Social Security Administration

The following interactive web pages are included:
* `acrostic.html` - an aid for solving anacrostic puzzles

The features are mostly orthogonal to those of [rspeer/solvertools](https://github.com/rspeer/solvertools).

Required software
=================
The Python modules are written in Python 3.  They are tested with versions 3.5-3.6
but might also work with other versions.
