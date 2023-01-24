###############################################################################
# Copyright 2019 StarkWare Industries Ltd.                                    #
#                                                                             #
# Licensed under the Apache License, Version 2.0 (the "License").             #
# You may not use this file except in compliance with the License.            #
# You may obtain a copy of the License at                                     #
#                                                                             #
# https://www.starkware.co/open-source-license/                               #
#                                                                             #
# Unless required by applicable law or agreed to in writing,                  #
# software distributed under the License is distributed on an "AS IS" BASIS,  #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    #
# See the License for the specific language governing permissions             #
# and limitations under the License.                                          #
###############################################################################


from itertools import dropwhile, starmap, zip_longest

"""
remove_trailing_elements(list_of_elements, element_to_remove)

This function takes in a list of elements, "list_of_elements", and an element "element_to_remove", and returns a new list of elements with the trailing elements that match "element_to_remove" removed.

The function first reverses the order of the elements in the input list using the slice operator [::-1], this is done in order to make it easy to remove trailing elements.
Then, it uses the dropwhile() function to remove elements from the beginning of the list while they match "element_to_remove". dropwhile() is a built-in Python function that takes in two arguments, a function and an iterable, and returns an iterator that drops elements from the iterable as long as the function returns True for those elements. In this case, the function passed to dropwhile() is a lambda function that takes in an element x and returns x == element_to_remove. This function returns True for any element that matches "element_to_remove", and False for any other element, so dropwhile() will remove elements from the beginning of the list as long as they match "element_to_remove".

Finally, the function converts the iterator returned by dropwhile() to a list using the built-in list() function, and then reverses the order of elements in the list back to its original order using the slice operator [::-1].

In the context of this function, "trailing elements" refers to elements that are located at the end of the list. These elements are the last elements in the list before the last element. In other words, elements that come after all the other elements in the list except the last one.
"""

def remove_trailing_elements(list_of_elements, element_to_remove):
    return list(dropwhile(lambda x: x == element_to_remove, list_of_elements[::-1]))[::-1]


def two_lists_tuple_operation(f, g, operation, fill_value):
    return list(starmap(operation, zip_longest(f, g, fillvalue=fill_value)))


def scalar_operation(list_of_elements, operation, scalar):
    return [operation(c, scalar) for c in list_of_elements]
