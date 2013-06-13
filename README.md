# python-speak7330


This project will host a set of tools to aid in the programming of the SCOM 7330 repeater.

## Installation

Put speak7330.py and spoken_words.csv in the same directory.

## Files

<dl>
<dt><i>speak7330.py:</i></dt>
<dd>a program which takes a sentance and translates it into command codes for the SCOM 7330 repeater.  Run `speak7330.py -h` for usage informmation.</dd>

<dt><i>spoken_words.csv:</i></dt>
<dd>a CSV file dictionary of phrases to codes.  You may add extra associations to this file.</dd>
</dl>

## Usage

speak7330.py can take the phrase to translate either from the command line (with -e flag) or with no arguments will start a loop reading phrases from the console and translating them to 7330 codes.

Numbers: this progam will recognize numbers such as 12345 and translate it as if you had entered:
"1 2 3 4 5"

Callsigns: this program can recognize american callsigns and will spell them out in the output code.  For example, AI4UR will be output as if you entered "A I 4 U R"
