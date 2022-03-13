"""
Created on 03/11/2021
@author jdh
"""

# I promise this isn't confusing on purpose

"""
Returns true if the given list is present in a list of lists. 
Can be used for tuples (just convert tuple to list on calling this function as
(X) != [X] even if X is identical
"""

def check_list_in_list_of_lists(list, list_of_lists):

    for list_element in list_of_lists:
        if list == list_element:
            return True
        else:
            continue

    return False

