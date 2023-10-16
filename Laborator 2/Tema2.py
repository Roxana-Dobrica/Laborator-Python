#1. Write a function to return a list of the first n numbers in the Fibonacci string.
import math

def first_numbers_fibonacci(n):
    if n == 0:
        return []
    if n == 1:
        return [0]

    fibonacci_string = [0, 1]
    for i in range(2, n):
        next_fibonacci_number = fibonacci_string[i-1] + fibonacci_string[i-2]
        fibonacci_string.append(next_fibonacci_number)

    return fibonacci_string

print(first_numbers_fibonacci(10))


#2. Write a function that receives a list of numbers and returns a list of the prime numbers found in it.
def is_prime(number):
    if number <= 1:
        return False
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    for div in range(5, int(math.sqrt(number)) + 1):
        if number % div == 0:
            return False
    return True


def prime_numbers_in_list(list_numbers):
    prime_numbers = []
    for number in list_numbers:
        if is_prime(number):
            prime_numbers.append(number)
    return prime_numbers

print(prime_numbers_in_list([23, 5, 34, 7, 12, 56, 11]))


# 3. Write a function that receives as parameters two lists a and b and returns:
# (a intersected with b, a reunited with b, a - b, b - a)

def operations_lists(a, b):
    intersection =[]
    reunion = []
    a_minus_b = []
    b_minus_a = []
    for num in a:
        if num in b:
            intersection.append(num)
    for num in a:
        if num not in b:
            a_minus_b.append(num)
    for num in b:
        if num not in a:
            b_minus_a.append(num)
    for num_a in a:
        if num_a not in reunion:
            reunion.append(num_a)
    for num_b in b:
        if num_b not in reunion:
            reunion.append(num_b)
    intersection.sort()
    reunion.sort()
    a_minus_b.sort()
    b_minus_a.sort()
    return {
        "a intersected with b": intersection,
        "a reunited with b": reunion,
        "a-b": a_minus_b,
        "b-a": b_minus_a
    }

print(operations_lists([1, 2, 3, 4, 5, 6, 10, 12, 14], [1, 2, 3, 7, 11]))

#sau, utilizand seturi:

def operations_lists_using_sets(a, b):
    set_a = set(a)
    set_b = set(b)

    intersection = list(set_a & set_b)
    reunion = list(set_a | set_b)
    a_minus_b = list(set_a - set_b)
    b_minus_a = list(set_b - set_a)

    intersection.sort()
    reunion.sort()
    a_minus_b.sort()
    b_minus_a.sort()

    return {
        "a intersected with b": intersection,
        "a reunited with b": reunion,
        "a-b": a_minus_b,
        "b-a": b_minus_a
    }

print(operations_lists_using_sets([1, 2, 3, 4, 5, 6, 10, 12, 14], [1, 2, 3, 7, 11]))


#4. Write a function that receives as a parameters a list of musical notes (strings), a list of moves (integers) and a start
# position (integer). The function will return the song composed by going
# though the musical notes beginning with the start position and following the moves given as parameter.

def compose(musical_notes, moves, start_position):
    song = []
    song.append(musical_notes[start_position])
    current_position = start_position

    for move in moves:
        current_position = (current_position + move) % len(musical_notes)
        song.append(musical_notes[current_position])
    return song

print(compose(["do", "re", "mi", "fa", "sol"], [1, -3, 4, 2], 2))


#5. Write a function that receives as parameter a matrix and will return the matrix obtained by replacing all the elements
# under the main diagonal with 0 (zero).

def replace_matrix_elements(matrix):
    n = len(matrix)
    for i in range(0, n):
        for j in range(0, n):
            if (i > j):
                matrix[i][j] = 0
    return matrix

matrix = [
    [1, 2, 3, 10],
    [5, 6, 7, 8],
    [8, 9, 2, 12],
    [1, 8, 6, 3]
]

matrix = replace_matrix_elements(matrix)

for row in matrix:
    for element in row:
        print(element, end=" ")
    print()


#6. Write a function that receives as a parameter a variable number of lists and a whole number x. Return a list containing
# the items that appear exactly x times in the incoming lists.

def find_items(*lists, x):
    counts = {}
    result = []

    for list_ in lists:
        for item in list_:
            counts[item] = counts.get(item, 0) + 1

    for item, count in counts.items():
        if count == x:
            result.append(item)

    return result

print(find_items([1, 2, 3], [2, 3, 4], [3, 4, 5], x=2))


#7. Write a function that receives as parameter a list of numbers (integers) and will return a tuple with 2 elements.
# The first element of the tuple will be the number of palindrome numbers found in the list and the second element will be
# the greatest palindrome number.

def is_palindrome(number):
    string_number = str(number)
    return string_number == string_number[::-1]

def find_palindromes(list_numbers):
    num_of_palindromes = 0
    max = -1
    for number in list_numbers:
        if is_palindrome(number):
            num_of_palindromes += 1
            if number > max:
                max = number
    return num_of_palindromes, max

print(find_palindromes([12321, 34, 567, 717, 23, 89898, 121]))


#8. Write a function that receives a number x, default value equal to 1, a list of strings, and a boolean flag set to True.
# For each string, generate a list containing the characters that have the ASCII code divisible by x if the flag is set to
# True, otherwise it should contain characters that have the ASCII code not divisible by x.

def find_characters(x=1, list_strings=None, flag=True):
    if list_strings is None:
        list_strings = []

    result = []

    for string_ in list_strings:
        current_list = []
        for letter in string_:
            ascii_code = ord(letter)
            if (ascii_code % x == 0 and flag) or (ascii_code % x != 0 and not flag):
                current_list.append(letter)
        result.append(current_list)

    return result

print(find_characters(x = 2, list_strings = ["test", "hello", "lab002"], flag = False))


# 9. Write a function that receives as paramer a matrix which represents the heights of the spectators in a stadium and will
# return a list of tuples (line, column) each one representing a seat of a spectator which can't see the game. A spectator
# can't see the game if there is at least one taller spectator standing in front of him. All the seats are occupied. All the
# seats are at the same level. Row and column indexing starts from 0, beginning with the closest row from the field.

def spectator_seats(matrix):
    spectators = []

    for row in range(len(matrix)):
        for column in range(len(matrix[0])):
            for row_front in range(row):
                if matrix[row][column] < matrix[row_front][column]:
                    spectators.append((row, column))
                    break
    return spectators

matrix = [
    [1, 2, 3, 2, 1, 1],
    [2, 4, 4, 3, 7, 2],
    [5, 5, 2, 5, 6, 4],
    [6, 6, 7, 6, 7, 5]
]

print(spectator_seats(matrix))


#10. Write a function that receives a variable number of lists and returns a list of tuples as follows: the first tuple
# contains the first items in the lists, the second element contains the items on the position 2 in the lists, etc. Ex: for
# lists [1,2,3], [5,6,7], ["a", "b", "c"] return: [(1, 5, "a ") ,(2, 6, "b"), (3,7, "c")].

def tuples_elements(*lists):
    result = []

    for items in zip(*lists):
        result.append(tuple(items))

    return result

lists1 = [1,2,3]
lists2 = [5,6,7]
lists3 = ["a", "b", "c"]
print(tuples_elements(lists1, lists2, lists3))


#11. Write a function that will order a list of string tuples based on the 3rd character of the 2nd element in the tuple.
# Example: ('abc', 'bcd'), ('abc', 'zza')] ==> [('abc', 'zza'), ('abc', 'bcd')]

def order_list(tuples_list):
    return sorted(tuples_list, key=lambda x: x[1][2])

tuples_list = [('abc', 'bcd'), ('abc', 'zza')]
sorted_list = order_list(tuples_list)
print(sorted_list)

#12. Write a function that will receive a list of words as parameter and will return a list of lists of words, grouped by
# rhyme. Two words rhyme if both of them end with the same 2 letters.

def group_by_rhyme(words_list):
    rhyme_dictionary = {}

    for word in words_list:
        key = word[-2:]

        if key not in rhyme_dictionary:
            rhyme_dictionary[key] = []

        rhyme_dictionary[key].append(word)

    result = list(rhyme_dictionary.values())

    return result

print(group_by_rhyme(['ana', 'banana', 'carte', 'arme', 'parte']))













