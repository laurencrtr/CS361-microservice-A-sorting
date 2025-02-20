# CS 361 Microservice A Test File
#
# This is the test file to show an example of how to use the sorting microservice.
# It is designed to communicate with the file microserviceA_sorting.py using zero mq
#
# Sorting is not case-sensitive so pokemon names can be upper or lower case, and names can be more than one word
# The weights can be positive and negative numbers, can include decimals
#
# User choice is not case-sensitive


############################################################################################
# Setup:
# To use this microservice, both zmq and pickle must be imported to the program
# The number in "tcp://localhost:5556" can be changed only if it is changed to match in the microservice.
import zmq
import pickle

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")



############################################################################################
# Example function:
def request_sorted_list(unsorted_list, sorting_type):                           # list, string
    """
    This function is an example of how to use the sorting microservice.

    Arguments:
        unsorted_list must be a list where each item in the list is a name, followed by a space, then the pokemon weight
            Example: ['Pikachu 2', 'Squirtle 3', 'Clefairy 1']
        sorting_type must be one of the following strings: 'A' for alphabetical, 'WI' for weight increasing order,
            or 'WD' for weight decreasing order

    Returns:
        a list sorted by the microservice in the manner requested
        (the returned list is a new object, the original list remains intact)
    """

    # To request data from the microservice:
    serialized_unsorted_list = pickle.dumps(unsorted_list)                      # ['name 00', 'name 20', 'name 1.1']
    sorting_type_encoded = sorting_type.encode()                                # 'A', 'WI', or 'WD'
    socket.send_multipart([serialized_unsorted_list, sorting_type_encoded])


    # To receive data from the microservice:
    # The variable deserializedList will contain the newly sorted list in the same format as the original list
    sorted_list_serialized = socket.recv()
    deserialized_sorted_list = pickle.loads(sorted_list_serialized)

    return deserialized_sorted_list



############################################################################################
# Example of how to use the function
def test_function():
    test_list = ['Pikachu 2', 'Squirtle 3', 'Clefairy 1', 'Gastly .1', 'Groudon 2094', 'zubat 16.5',
                 'test  -28', 'two words 0', 'Abra 43', 'Zubat 17']

    print(f"\n\nThis is your original list of pokemon:\n{test_list}\n")

    test_choice = input("How would you like your list to be sorted? Please chose from the following options: "
                        "\n 'A':  to sort alphabetically"
                        "\n 'WI': to sort by weight in increasing order"
                        "\n 'WD': to sort by weight in decreasing order"
                        "\n Enter your selection here:  ")

    print("This is the sorted list: ")
    print(request_sorted_list(test_list,test_choice))
    test_function()

test_function()
