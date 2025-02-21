# CS 361 Microservice A
#
# This microservice receives a serialized list and an encoded string indicating how the list should be sorted
# It will sort the list as requested, serialize it, and send it back
#
# Sorting is not case-sensitive so pokemon names can be upper or lower case, and names can be more than one word
# The weights can be positive and negative numbers, can include decimals
#
# User choice is not case-sensitive but must be one of the following to indicate how the list will be sorted:
#       'A'  to sort alphabetically
#       'WI' to sort by weight in increasing order
#       'WD' to sort by weight in decreasing order
#
# If the program is unable to process the request, it will send an error message in the form of a list containing a
#   string with the error message


import zmq
import pickle

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

print("The sorting microservice is active.")
def sort_list():
    while True:
        try:
            received_info = socket.recv_multipart()                     # Receives [list, string]
                                                                        # list is serialized and the string is encoded

            unsorted_list = pickle.loads(received_info[0])              # deserialize the unsorted list sent to the microservice

            sort_type = received_info[1].decode()                       # decode the option for sorting type chosen by the user
            sort_type = sort_type.upper()                               # so user choice is not case-sensitive


            if sort_type == 'A':
                # unsorted_list.sort()                                  # can be used if we want sorting to be case-sensitive
                sorted_pokemon = sorted(unsorted_list, key=str.lower)   # sorting that is not case-sensitive
                sorted_list = pickle.dumps(sorted_pokemon)
                print("Your list was successfully sorted.")
                socket.send(sorted_list)

            elif sort_type == 'WI':
                # split at the last space in the string,
                # turn the number after the space into float value,
                # sort in ascending order based on number
                unsorted_list.sort(key = lambda wt: float(wt.rsplit(' ',1)[1]))
                sorted_list = pickle.dumps(unsorted_list)
                print("Your list was successfully sorted.")
                socket.send(sorted_list)

            elif sort_type == 'WD':
                # split at the last space in the string,
                # turn the number after the space into float value,
                # sort in descending order based on number
                unsorted_list.sort(key = lambda wt: float(wt.rsplit(' ',1)[1]), reverse = True)
                sorted_list = pickle.dumps(unsorted_list)
                print("Your list was successfully sorted.")
                socket.send(sorted_list)

            else:
                print("The sorting microservice was unable to process your request due to invalid input.")
                error_message = ["**Error** Please make sure the string sent to the sorting microservice is 'A', 'WD', or 'WI'"]
                error_message_serial = pickle.dumps(error_message)
                socket.send(error_message_serial)


        except:
            print("The sorting microservice was unable to process your request due to invalid input.")
            error_message = ['**Error** The sorting microservice was unable to process your request due to invalid input.']
            error_message_serial = pickle.dumps(error_message)
            socket.send(error_message_serial)

sort_list()