# Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only 
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary 
      all-different constraints for both the row and column constraints. 

'''
from cspbase import *
import itertools


def satisfied_tuples(inequality, variables):
    """
    precondition: variables is a ordered list of two variables
    """
    domain = [var.domain() for var in variables]
    permutations = itertools.product(*domain)
    result = []
    if inequality == "<":
        for permutation in permutations:
            # print(domain, permutation)
            i, j = permutation[0], permutation[1]
            if i < j:
                result.append(tuple([i, j]))
    elif inequality == ">":
        for permutation in permutations:
            # print(domain, permutation)
            i, j = permutation[0], permutation[1]
            if i > j:
                result.append(tuple([i, j]))
    elif inequality == "!=":
        for permutation in permutations:
            i, j = permutation[0], permutation[1]
            if i != j:
                result.append(tuple([i, j]))
    elif inequality == "All-diff":
        for permutation in permutations:
            if len(permutation) == len(set(permutation)):
                result.append(tuple(permutation))
    else:
        raise(TypeError("No such operator!"))
    # print(result)
    return result


def create_extra_constraints(futo_grid):
    size = len(futo_grid)
    var_array = [[0 for i in range(size)] for i in range(size)]
    c_lst = []  # constraint list
    cons_num = 0
    for i, row in enumerate(futo_grid):
        for j, num in enumerate(row[::2]):
            if num == 0:
                var_array[i][j] = Variable("V({0},{1})".format(i, j), [(a + 1) for a in range(size)])
            else:
                var_array[i][j] = Variable("V({0},{1})".format(i, j), [num])
        for j, constraint in enumerate(row[1::2]):
            if constraint != '.':
                variables = [var_array[i][j], var_array[i][j + 1]]
                new_con = Constraint("C({})".format(cons_num), variables)
                new_con.add_satisfying_tuples(satisfied_tuples(constraint, variables))
                # print(new_con.name, constraint, satisfied_tuples(constraint, variables))
                c_lst.append(new_con)
                cons_num += 1
    return var_array, c_lst, cons_num


def futoshiki_csp_model_1(futo_grid):
    ##IMPLEMENT
    size = len(futo_grid)
    var_array, c_lst, cons_num = create_extra_constraints(futo_grid)

    # row constraints
    for i in range(size):
        for j in range(size):
            for k in range(j + 1, size):
                variables = [var_array[i][j], var_array[i][k]]
                row_con = Constraint("C({0})".format(cons_num), variables)
                row_con.add_satisfying_tuples(satisfied_tuples("!=", variables))
                c_lst.append(row_con)
                cons_num += 1

    # column constraints
    for i in range(size):
        for j in range(size):
            for k in range(j + 1, size):
                variables = [var_array[j][i], var_array[k][i]]
                col_con = Constraint("C({0})".format(cons_num), variables)
                col_con.add_satisfying_tuples(satisfied_tuples("!=", variables))
                c_lst.append(col_con)
                cons_num += 1

    # create csp
    csp = CSP('futoshiki_model_1', [var for row in var_array for var in row])
    for c in c_lst:
        csp.add_constraint(c)

    return csp, var_array


def futoshiki_csp_model_2(futo_grid):
    ##IMPLEMENT
    size = len(futo_grid)
    var_array, c_lst, cons_num = create_extra_constraints(futo_grid)
    # print(var_array, c_lst)
    # row constraints
    for i in range(size):
        variables = var_array[i]
        row_con = Constraint("C({0})".format(cons_num), variables)
        row_con.add_satisfying_tuples(satisfied_tuples("All-diff", variables))
        c_lst.append(row_con)
        cons_num += 1

    # column constraints
    for i in range(size):
        variables = [var_array[j][i] for j in range(size)]
        row_con = Constraint("C({0})".format(cons_num), variables)
        row_con.add_satisfying_tuples(satisfied_tuples("All-diff", variables))
        c_lst.append(row_con)
        cons_num += 1

    # create csp
    csp = CSP('futoshiki_model_2', [var for row in var_array for var in row])
    for c in c_lst:
        csp.add_constraint(c)

    return csp, var_array