from csp import CSP
import re
import copy


class Sudoku(CSP):
    """
    Constraint Satisfation Problem Sudoku solver class.
    The class is a sub-class of aima's CSP implementation.
    Modeling the Sudoku Game in variable, domains, neighbors and constraint method.
    """

    def __init__(self, grid):
        """
        Init method of Sudoku class. The parameter grid contains the definition of the sudoku board.
        This method is devoted to populate the __init_ method of CSP class, creating and passing
        variables, domains and neighbors from the grid parameter.
        """
        BLOCK_SIZE = 3
        BLOCKS_IN_ROW = 3
        ROW_SIZE = 9
        COL_SIZE = 9

        # Variables -
        # Variables definition. The varibles are an array with a sequence of indexes, from 0 to 80.

        self.variables = [x for x in range(ROW_SIZE * COL_SIZE)]
        # Domains -
        # Domains defintion. In this case of Sudoku CSP, the domains are '123456789' for empty cells and
        # the value of cell for cells with the default value.
        original_grid = list(iter(re.findall(r'\d|\.', grid)))
        domains = {}
        counter = 0
        for item in original_grid:
            if item == '.':
                domains[int(counter)] = '123456789'
            else:
                value = int(item)
                restricted_domain = [str(value)]
                domains[int(counter)] = restricted_domain
            counter += 1

        # Neighbors
        # Neighbors of binary-constraint definition. This dictionary contains the relations among a cell with its row,
        # column and block.
        neighbors = {}

        # rows
        # ∀ a
        # ∀ i ≠ j: xai ≠ xaj
        for a in range(ROW_SIZE):
            row_start = a * BLOCKS_IN_ROW * BLOCK_SIZE
            row_stop = a * BLOCKS_IN_ROW * BLOCK_SIZE + BLOCKS_IN_ROW * BLOCK_SIZE
            row_indexes = list(range(row_start, row_stop))
            for item in row_indexes:
                neighbors[int(item)] = list()
                item_neighbors = list(copy.copy(row_indexes))
                item_neighbors = [x for x in item_neighbors if x != item]
                neighbors[int(item)] += item_neighbors

        # columns
        # ∀ b
        # ∀ h ≠ k : xbh ≠ xbk
        for b in range(COL_SIZE):
            col_indexes = [ROW_SIZE * a + b for a in range(COL_SIZE)]
            for item in col_indexes:
                item_neighbors = list(copy.copy(col_indexes))
                item_neighbors = [x for x in item_neighbors if x != item]
                neighbors[int(item)] += item_neighbors

        # blocks
        # A block is a submatrix of sudoku grid:
        # a = {1, 4, 7}:  i, j = [a, a + 2]
        # b = {1, 4, 7}:  k, h = [b, b + 2]
        # {xpq} p = a...a + 2, q = b...b + 2 ∈ A ∈ N^(3x3)
        # where
        # ∀a:  i, j = [a, a + 2]
        # ∀b:  k, h = [b, b + 2]
        # ∀ h ≠ k or i ≠ j: xik ≠ xj, h
        a = b = [0, 3, 6]
        for b_row in a:
            for b_col in b:
                # block
                block_items = []
                for r in range(3):
                    for c in range(3):
                        block_items.append((b_row + r) * ROW_SIZE + b_col + c)

                for item in block_items:
                    item_neighbors = list(copy.copy(block_items))
                    item_neighbors = [x for x in item_neighbors if x != item]
                    neighbors[int(item)] += item_neighbors

        # remove duplicates
        for item in neighbors:
            neighbors[int(item)] = set(neighbors[int(item)])

        CSP.__init__(self, None, domains, neighbors, self.different_values_constraint)

    @staticmethod
    def different_values_constraint(A, a, B, b):
        """Constraint: neighbors has to have different value"""
        return a != b

    def display(self, assignment):
        """
        Override of CSP's method display, to present the Sudoku grid.

        :param assignment: assignment of variables
        :return:
        """
        output = "|-----------------------------|\n|"
        for item in self.variables:
            if item in assignment:
                output += " " + assignment[item] + " "
            else:
                output += " * "
            if not (item + 1) % 3: output += "|"
            if not (item + 1) % 9: output += "\n|"
            if not (item + 1) % 27 and item != (len(self.variables)-1): output += "-----------------------------|\n|"

        output += "-----------------------------|\n"
        print(output)
