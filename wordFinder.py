import json
from collections import Counter
import itertools

class WordFinder:
    # Input:
    #   - wlist: [list of lowercase words]
    #   - word size filter
    def __init__(self,wlist,wsize=6):
        # Filter words by size
        w6 = list(filter(lambda x: len(x) == wsize, wlist))

        # Get alphabet
        s = set()
        for w in w6:
            s.update(w)

        # Get containing dictionary
        self.letters_dict = dict([(k, set()) for k in s])
        for w in w6:
            for k in self.letters_dict:
                if k in w:
                    self.letters_dict[k].add(w)

    # Get words from list
    # Input:
    #   - startsWith: ""/"l" (l: letter)
    #   - contains: "listOfCharacters"
    # Output:
    #   - List of words
    #   - List of extra characters in the same order
    def findWords(self, startsWith,contains):
        # Base set
        if startsWith != "":
            ms = self.letters_dict[startsWith]
        else:
            ms = self.letters_dict[contains[0]]

        # Get intersection for every character
        for k in contains:
            ms = ms.intersection(self.letters_dict[k])

        # Counter for filtering
        cntr = Counter(contains+startsWith)

        # Get words starting with "startsWith"
        if startsWith != "":
            ml = list(filter(lambda x: x[0] == startsWith, ms))
        else:
            ml = ms

        # Filter words according to the Counter
        for k in cntr:
            ml = list(filter(lambda x: x.count(k) >= cntr[k], ml))

        # Get extra character
        extraC = [Counter(w) for w in ml]
        for c in extraC:
            c.subtract(Counter(startsWith+contains))
        # It fails if there is no word
        try:
            extraC = [list(filter(lambda x: c[x] != 0,list(c.keys())))[0] for c in extraC]
        except:
            extraC = None

        return ml,extraC

    # Solve a whole problem
    # Input:
    #   - listOfProblems: List of (beginsWith,contains) *See self.findWords() description*
    # Output:
    #   - List of ([words...],[extraCharacters...) *See self.findWords() description*
    #   - List of ('extraCharacters',[words...]) for every combination
    def wholeProblem(self,listOfProblems):
        res = [self.findWords(x, y) for x, y in listOfProblems]
        pos_letters = [x for x in zip(*res)][1]

        every_combination = itertools.product(*pos_letters)
        every_combination = map(lambda x: "".join(x), every_combination)

        comb_words = [(e, self.findWords("", e)[0]) for e in every_combination]
        comb_words = list(filter(lambda x: len(x[1]) > 0, comb_words))

        return res, comb_words

def main():
    with open("words.json") as ifile:
        j = json.load(ifile)

    wsolver = WordFinder(list(j.keys()))
    res, comb_words = wsolver.wholeProblem([("t","inpu"),("t", "aosy"),("t", "hory"),("t", "blmu"),("t", "ckry"),("t", "ahht")])

    def prettyPrint(l):
        print("###")
        for e in l:
            print(e)

    prettyPrint(res)
    prettyPrint(comb_words)


if __name__ == "__main__":
    main()


