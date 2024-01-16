import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]

# This function will help us to get how many genes a person has without 
# using too many ifs and elses in our main functions
def NumberOfGenesAndTrait(person, one_gene, two_genes, have_trait):
        if person in one_gene:
            NumberOfGenes = 1 
        elif person in two_genes:
            NumberOfGenes = 2
        else:
            NumberOfGenes = 0
        HasTrait = True if person in have_trait else False
        return NumberOfGenes, HasTrait

# When we know how many genes a parent has we can calculate the probability
# of that gene going to their son
def ProbOfGivingGene(numofgenes):
    # If the parent has only one gene, he/she can pass it to his/her son in just 
    # two different ways: They pass the safe gene with probability 0.5 and (multiplication) 
    # then it mutates with prob. PROBS["mutation"] or (sum) they pass the GJB2 gene with
    # prob. 0.5 and (multiplication) it doesnt mutate with prob. 1 - PROBS["mutation"]
    if numofgenes == 1:
        return 0.5 * (PROBS["mutation"]) + 0.5 * (1 - PROBS["mutation"]) # This adds up to just 0.5
    # If the parent has two genes then the they will always pass that gene unless it mutates 
    # with probability PROBS["mutation"]
    elif numofgenes == 2: 
        return 1 - PROBS["mutation"]
    else:
    # If the parent doesnt have the gene, the only way they will pass it is if it mutates
        return PROBS["mutation"]
        
def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Calculating a joint probability is just multiplying several values depending, in this
    # case, in the person, so we will initialize de prob. at 1 and iterate through the persons. 
    JointProb = 1
    for person in people:
        num, trait = NumberOfGenesAndTrait(person, one_gene, two_genes, have_trait)

        # Having the trait or not just depends on the amount of genes the person has so we can multiply
        # it just with nowing in which set the person is (1gene, 2 genes or 0genes)
        ProbOfTraitGivenGenes = PROBS['trait'][num][trait]
        JointProb *= ProbOfTraitGivenGenes

        # We separate cases, if the person has information about its parents we can use it, we just check
        # if the person has a father because in our data a person has both parents or neither
        if people[person]["father"]:
            numMother = NumberOfGenesAndTrait(people[person]["mother"], one_gene, two_genes, have_trait)[0]
            numFather = NumberOfGenesAndTrait(people[person]["father"], one_gene, two_genes, have_trait)[0]
            ProbGiveGeneMother = ProbOfGivingGene(numMother)
            ProbGiveGeneFather = ProbOfGivingGene(numFather)

            # We know how many genes the person has, so after getting the amount of genes the parents have
            # we can calculate the likelihood of this scenario

            # If the person has 0 genes we need the probability of neither of their parents passing the gene
            if num == 0:
                Prob = (1 - ProbGiveGeneMother) * (1 - ProbGiveGeneFather)
            # If the person has 1 gene we need the probability of the father or mother passing the gene but not both
            elif num == 1:
                Prob = (1 - ProbGiveGeneMother) * (ProbGiveGeneFather) + (ProbGiveGeneMother) * (1 - ProbGiveGeneFather)
            # If the person has 2 genes we need the probability of neither of both their parents passing the gene
            else:
                Prob = (ProbGiveGeneMother) * (ProbGiveGeneFather)
            
            # We add the probability ton our total
            JointProb *= Prob 

        else:
            # This case is easier as we just need the general likelihood of a person having or not the gene
            ProbOfHavingThatManyGenes = PROBS['gene'][num]
            JointProb *= ProbOfHavingThatManyGenes 
    return JointProb


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # In this function we add the probabilities of of all the possible 
    # ways we can have a certain result 
    for person in probabilities:
        num, trait = NumberOfGenesAndTrait(person, one_gene, two_genes, have_trait)
        probabilities[person]["gene"][num] += p
        probabilities[person]["trait"][trait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # for each person and for each observation (genes or traits) we get the sum
    # of the probabilities and then just divide each of thos values by the total
    for person in probabilities:
        for observation in ("gene", "trait"):
            total = sum(probabilities[person][observation].values())
            for i in probabilities[person][observation]:
                probabilities[person][observation][i] /= total


if __name__ == "__main__":
    main()
