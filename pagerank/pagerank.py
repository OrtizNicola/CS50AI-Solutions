import os
import random
import re
import sys

# Will help us create a dictionary of appearences initialized at 0
from collections import defaultdict

# Will help us use a dictionary without modifying it
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    mapping = {}
    LinkedPages = corpus[page]
    n = len(LinkedPages)
    N = len(corpus.keys())

    # We take 2 cases: 

    # If the page has at least one link
    if n != 0:

        # Calculating the probabilities for the linked pages
        for pages in LinkedPages:
            mapping[pages] = damping_factor / n + (1 - damping_factor) / N

        # Calculating the probabilities for the pages that are not linked
        NotLinkedPages = set(corpus.keys()) - LinkedPages
        for pages in NotLinkedPages:
            mapping[pages] = (1 - damping_factor) / N

    # If the pages has zero links
    else:

        # We asign each page an equal probability
        for pages in corpus.keys():
            mapping[pages] = 1 / N

    return mapping

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # "Repetitions" will help us count how many times we arrive 
    # to each page
    Repetitions = defaultdict(int)

    # Initialize the page randomly between all of the options and count it
    ActualPage = random.choice(list(corpus.keys()))
    Repetitions[ActualPage] += 1

    # Now for each sample we take the actual page and calculate the next 
    # one considering the probabilities for the actual page and keeping 
    # track of all appearences
    for _ in range(1, n):
        probs = transition_model(corpus, ActualPage, damping_factor)
        ActualPage = random.choices(list(probs.keys()), list(probs.values()), k=1)[0]
        Repetitions[ActualPage] += 1
    
    # We have a dictionary with the number of appearences, to take the 
    # ranks we have to divide by the number of samples
    for page in Repetitions:
        Repetitions[page] /= n 

    return dict(Repetitions)

# This function will help us to get the pages that link to a certain page 
def PagesThatLinkTo(corpus, page):
    ans = set()
    for i in corpus:
        # By adding "not corpus[i]" we are treating pages with no links 
        # as they have links to every page in the corpus
        if page in corpus[i] or not corpus[i]:
            ans.add(i)
    return ans

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probs = copy.deepcopy(corpus)
    N = len(probs)

    # Initializing the ranks for each page at 1 / N
    for p in probs:
        probs[p] = 1 / N

    # We want to keep updating all of the probabilities until "flag" indicates
    # us that we're not getting closer than 0.001 for some value in our ranks.
    while True:
        flag = True
        for p in probs:
            
            # To calcutate the second term we have to iterate through all 
            # of the pages that link to the page whose rank we want to calculate
            SecondTerm = 0
            PagesThatLinkTo_i = PagesThatLinkTo(corpus, p)
            for i in PagesThatLinkTo_i:

                # As there might be pages with no links because of the way our function
                # PagesThatLinkTo works, we would like to take care of this case and treat 
                # it as if that page with no links, links to every single page
                try:
                    SecondTerm += probs[i] / len(corpus[i])
                except ZeroDivisionError:
                    SecondTerm += probs[i] / N
            NewProb = (1 - damping_factor) / N + damping_factor * SecondTerm

            # We check if the values aren't changing that much
            if abs(probs[p] - NewProb) > 0.001:
                flag = False
                
            # Updating the values of the ranks
            probs[p] = NewProb
        if flag:
            break
    return probs

if __name__ == "__main__":
    main()
