#!/usr/bin/env python

import pprint
import re
import argparse

class Phrase(object):
    def __init__(self, s=""):
        super(Phrase, self).__init__()
        self.p = s.lower().split()
    def append(self, a):
        self.p.append(a)
    def pop(self):
        return self.p.pop()
    def num_words(self):
        return len(self.p)
    def __len__(self):
        return len(self.p)
    def __str__(self):
        return ' '.join(self.p)
    def __hash__(self):
        return hash(str(self))
    def __repr__(self):
        return str(self)
    def __cmp__(self,other):
        return cmp(str(self), str(other))
                 
expando_words = re.compile('^[ankw].*[0-9][a-z]{1,3}$|^[0-9]{2,}$')
 
class Words(object):
    def __init__(self, str):
        super(Words, self).__init__()
        self.string = str.lower().split()
        self.__words = []
    def __iter__(self):
        self.__words = [x for x in self.string]
        return self
    def next(self):
        if self.__words:
            x = self.pop(0)
            if expando_words.match(x):
                self.push_letters(x)
                x = self.pop(0)
            return x
        else:
            raise StopIteration
    def push_letters(self, word):
        for i in word[::-1]:
            self.push(i)
    def push(self,v):
        self.__words.insert(0, v)
    def pop(self,v):
        return self.__words.pop(0)
    def __len__(self):
        return len(self.__words)
    def substrings(self):
        for i in range(len(self.string)-1):
            yield ' '.join(self.string[:i+1])

class Emitter(object):
    def __init__(self):
        super(Emitter, self).__init__()
        self.output = []
    def emit(self, s):
        self.output.append(s)
    def send(self):
        print " ".join(self.output)


class Application(object):

    def __init__(self):
        self.args = self.parse_args()
        self.terminals = {}
        self.nonterminals = set()

    def speak(self, q):
        phrase = Phrase()
        output = Emitter()
        words = Words(q)

        for word in words:
            phrase.append(word)

            if phrase in self.nonterminals and len(words) > 0:
                continue
            else:
                try:
                    tok = self.terminals[phrase]
                    output.emit(tok)
                    if self.args.verbose:
                        print '    Found:', tok, phrase
                except:
                    # walk back popping one token at a time from built up phrase
                    if len(phrase) > 1:
                        while len(phrase) > 1:
                            words.push(phrase.pop())
                            try:
                                tok = self.terminals[phrase]
                                output.emit(tok)
                                if self.args.verbose:
                                    print "    Found:", tok, phrase
                                break
                            except KeyError:
                                pass
                        else:
                            # we should never get here because at the very least the first token was valid
                            raise Exception("Parse walkback failed")
                    else:
                        if self.args.verbose:
                            print "Not Found:     ", phrase
            phrase = Phrase()
        return output


    def parse_args(self):
        parser = argparse.ArgumentParser(description="Generate speech codes for 7330 repeater")
        parser.add_argument('-v', dest='verbose', action='store_true',
                            help='Print parsing detail')
        parser.add_argument('-e', dest='expression', nargs='?', metavar="PHRASE",
                            help='speak PHRASE')
        return parser.parse_args()


    def main(self):

        with open('spoken_words.csv', 'r') as f:
            for l in f:
                code, string = l.strip().lower().split(',')
                self.terminals[Phrase(string)] = code

                for p in Words(string).substrings():
                    self.nonterminals.add(Phrase(p))

        if False:
            pprint(sorted(self.terminals))
            pprint(self.nonterminals)
            return

        if self.args.expression:
            self.speak(self.args.expression).send()
        else:
            while True:
                try:
                    q = raw_input("Enter phrase: ").strip().lower()
                    if q == "":
                        return
                except:
                    print
                    break
                output = self.speak(q)
                if self.args.verbose:
                    print "Result String:"
                output.send()


if __name__ == '__main__':
    Application().main()
