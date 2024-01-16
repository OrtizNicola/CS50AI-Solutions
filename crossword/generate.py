import sys

from crossword import *

import copy


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Create copy to iterate through domains
        domains = copy.deepcopy(self.domains)

        # Then we check if each value for every variable is the 
        # right size
        for variable in domains:
            for word in domains[variable]:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initialize with no revisions made
        RevisionMade = False

        # if the variables overlap
        if self.crossword.overlaps[x, y]:
            domainx = copy.copy(self.domains[x])
            i, j = self.crossword.overlaps[x, y]
            # check for each value in x if it has a possible value in y
            for word1 in domainx:
                possible = False
                for word2 in self.domains[y]:
                    if word1[i] == word2[j]:
                        # if there's at least one possible value, we don't
                        # touch x's domain
                        possible = True
                # if it wasn't possible to find a possible value in y, we
                # remove that value from x's domain and change the return
                # value: RevisionsMade
                if not possible:
                    self.domains[x].remove(word1)
                    RevisionMade = True
        # note that if there wasn't an overlap, the function returns false
        # but if there was, we check every word          
        return RevisionMade

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # define the queue that we're going to use
        if arcs:
            queue = arcs
        else:
            queue = list(self.crossword.overlaps.keys())
        
        # while the queue has elements
        while queue:
            # revise each arc in the queue
            x, y = queue.pop(0)
            if self.revise(x, y):
                # if there was a change made, we add variables that
                # should be revised again to the queue
                if not self.domains[x]:
                    # return false if the crossword is infeasable
                    return False
                for z in self.crossword.neighbors(x) - {y}:
                    queue.append((z, x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # if a variable is missing in the assignment, it's not complete
        if set(assignment.keys()) != self.crossword.variables:
            return False
        # we check if there's values in the assignment with no word assigned
        for var in assignment:
            if not assignment[var]:
                return False
        # if none of the previous cases happened, the assignment is 
        # complete
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # if there's repeated values, it's not consistent
        if len(list(assignment.values())) != len(set(assignment.values())):
            return False
        # if a variable has addigned a word with a different size
        # it's not consistent
        for var in assignment:
            if var.length != len(assignment[var]):
                return False
        # if there's variables that overlap but don't have the same 
        # letter at the overlap, it's not consistent
        for var1 in assignment:
            for var2 in assignment:
                if var1 != var2 and self.crossword.overlaps[var1, var2]:
                    i, j = self.crossword.overlaps[var1, var2]
                    if assignment[var1][i] != assignment[var2][j]:
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # define a new criteria to sort the possible values of variables
        def criteria(word):
            TotalChanges = 0
            for neighbor in self.crossword.neighbors(var):
                ChangesInNeighbor = 0
                if neighbor not in assignment:
                    for words in self.domains[neighbor]:
                        i, j = self.crossword.overlaps[var, neighbor]
                        if word[i] != words[j]:
                            ChangesInNeighbor += 1
                TotalChanges += 1
            # we want to sort based on the amount of changes that
            # assignment makes.
            return TotalChanges
        # return the new sorted list
        return sorted(list(self.domains[var]), key = criteria)

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # initialize the best value for the amount of words in a domain
        # as a big value
        best = float("infinity")
        for var in self.crossword.variables:
            # if the variable doesn't have an assgnment yet
            if var not in assignment:
                # if the amount of possible values it has is less than the 
                # previous best, now we choose that variavle as the best
                if best > len(self.domains[var]):
                    bestvar = var
                    best = len(self.domains[var])
                # if it has the same amount of possible values as the 
                # previous best, we choose the new best based on the
                # amount of neighbors
                if best == len(self.domains[var]):
                    if len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(bestvar)):
                        bestvar = var
                        best = len(self.domains[var])
        return bestvar

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # when the assignment is complete, we've finished
        if self.assignment_complete(assignment):
            return assignment
        # if it's not finished we choose a new variable to assign a value
        var = self.select_unassigned_variable(assignment)
        # we order the possible values of the variable to start
        # trying with the best values
        ordered_values = self.order_domain_values(var, assignment)
        # we go through the possible values and assigning the
        # new values and calling backtracking for each new assignment
        for values in ordered_values:
            nextassign = copy.deepcopy(assignment)
            nextassign[var] = values
            if self.consistent(nextassign):
                result = self.backtrack(nextassign)
                if result:
                    return result
        # if the assignment is not consistent, we return none
        return None
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
