import sys

from crossword import *


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

        for variable in self.crossword.variables:
            for word in self.crossword.words:
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
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            i, j = overlap
            to_remove = set()
            for x_ in self.domains[x]:
                possible_overlap = False
                for y_ in self.domains[y]:
                    if x_ != y_ and x_[i] == y_[j]:
                        possible_overlap = True
                        break
                # if there is no value in y's domain satifies the constraints
                if not possible_overlap:
                    to_remove.add(x_)

            if to_remove:
                self.domains[x] -= to_remove
                revised = True

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:
            # select only those variables which have an overlap
            queue = []
            for variable1 in self.crossword.variables:
                for variable2 in self.crossword.neighbors(variable1):
                    queue.append((variable1, variable2))
        else:
            queue = list(arcs)
        while queue:
            x, y = queue.pop(0)
            set_y = set()
            set_y.add(y)
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x) - set_y:
                    queue.append((z, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment.keys():
                return False
            if assignment[variable] not in self.crossword.words:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for var in assignment.keys():
           # Check the unary constraint
            if len(assignment[var]) != var.length:
                return False

            # Check if the neighbor is well placed (depending on the overlap)
            for neighbor in self.crossword.neighbors(var):
                i,j = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment:
                    if assignment[var][i] != assignment[neighbor][j] or assignment[var] == assignment[neighbor]:
                        return False
            
            # Check if there is 2 words the same
            for var2 in assignment.keys():
                if var2 != var and assignment[var] == assignment[var2]:
                    return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        # "Note that any variable present in assignment already has a value, and therefore shouldn’t be counted when computing the number of values ruled out for neighboring unassigned variables."
        for variable in assignment:
            if variable in neighbors:
                neighbors.remove(variable)

        # result: list compose of (value,out) --> value is all values of the domain of var
        result = []
        for value in self.domains[var]:
            out = 0
            for var2 in neighbors:
                for value2 in self.domains[var2]:
                    if self.crossword.overlaps[var, var2]:
                        i,j = self.crossword.overlaps[var, var2]
                        if value[i] != value2[j]:
                            out+=1
            result.append((value,out))

        def myFunc(item):
            return item[1]

        # sort depending on the second value of the tuple
        result.sort(key=myFunc)

        # return list with first item of each tuple in result (value)
        return [val[0] for val in result]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables_list = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                variables_list.append((variable, len(self.domains[variable]), len(self.crossword.neighbors(variable))))

        def myFunc(item):
            return (item[1], -item[2])

        if variables_list != []:
            variables_list.sort(key=myFunc)
            return variables_list[0][0]
        return

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            new_assigment = assignment.copy()
            new_assigment[var] = value
            if self.consistent(new_assigment):
                result = self.backtrack(new_assigment)
                if result:
                    return result
        return

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
