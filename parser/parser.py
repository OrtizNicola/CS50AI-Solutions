import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""


# I found this site helpful: https://guides.lib.uoguelph.ca/Grammar/SentenceStructure

# The sentences that we have to parse are either compound sentences
# or simple ones, so they are made from a clause or multiple
# clauses connected by conjunctions (for this project we just have
# two clauses at most).

# Each clause is usually a noun phrase and a verb phrase, but in some cases we don't 
# really need the noun (for example the second clause in "8.txt" the clause after the 
# conjunction is just "lit his pipe" => no noun!)

# The helper and the predicate terminals help us nest multiple adjectives, adverbs,
# noun phrases, etc

NONTERMINALS = """
S -> CLAUSE | CLAUSE Conj CLAUSE
CLAUSE -> NP VP | VP
NP -> N | HELPER N | NP P NP
HELPER -> Det | Adj | HELPER HELPER
VP -> V | VP PREDICATE | PREDICATE VP
PREDICATE -> NP | P | Adv | PREDICATE PREDICATE
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    words = nltk.tokenize.word_tokenize(sentence)
    # As the word_tokenize function already separates the punctuation symbols from the 
    # words, we won't have words with both alphabetical and alphanumerical symbols so 
    # we can use the isalpha() function 
    alphwords = [word.lower() for word in words if word.isalpha()]
    return alphwords


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    ans = []
    # We use the label and the subrees functions as in the recommendations
    # Because of how we defined our NONTERMINALS, we are not going to have a lot of 
    # NP's nested one inside another => We just need to print NP subtrees
    for subtree in tree.subtrees():
        if subtree.label() == "NP":
            ans.append(subtree)

    return ans


if __name__ == "__main__":
    main()
