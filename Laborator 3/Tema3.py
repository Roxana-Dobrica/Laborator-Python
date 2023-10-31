#1. Write a function that receives as parameters two lists a and b and returns a list of sets containing:
# (a intersected with b, a reunited with b, a - b, b - a)

def list_operations(a, b):
    set_a = set(a)
    set_b = set(b)

    intersection = set_a & set_b
    reunion = set_a | set_b
    a_minus_b = set_a - set_b
    b_minus_a = set_b - set_a

    return [intersection, reunion, a_minus_b, b_minus_a]

a = [1, 3, 6, 10, 16, 11]
b= [1, 10, 7, 9]
print(list_operations(a, b))


#2. Write a function that receives a string as a parameter and returns a dictionary in which the keys are
# the characters in the character string and the values are the number of occurrences of that character in the given text.

def num_of_occ_letters(input_string):
    letters_dictionary = {}

    for letter in input_string:
        if letter in letters_dictionary.keys():
            letters_dictionary[letter] += 1
        else:
            letters_dictionary[letter] = 1

    return letters_dictionary

input_string = "Ana has apples."
print(num_of_occ_letters(input_string))


#3. Compare two dictionaries without using the operator "==" returning True or False. (Attention, dictionaries must be
# recursively covered because they can contain other containers, such as dictionaries, lists, sets, etc.)


def compare_dictionaries(dict1, dict2):
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return False

    if set(dict1.keys()) != set(dict2.keys()):
        return False

    for key in dict1.keys():
        if not compare_values(dict1[key], dict2[key]):
            return False

    return True

def compare_values(value1, value2):
    if type(value1) != type(value2):
        return False

    if isinstance(value1, dict):
        return compare_dictionaries(value1, value2)

    if isinstance(value1, list):
        if len(value1) != len(value2):
            return False
        return all(compare_values(elem1, elem2) for elem1, elem2 in zip(value1, value2))

    if isinstance(value1, set):
        return value1 <= value2 and value2 <= value1

    elif value1 != value2:
        return False

    return True


dict1 = {
    "a": 1,
    "b": {"c": 2, "d": [3, 4, 5]},
    "e": [1, 5, 7],
    "f": {1, 2, 10}
}

dict2 = {
    "a": 1,
    "b": {"c": 2, "d": [3, 4, 5]},
    "e": [1, 5, 7],
    "f": {1, 2, 10}
}

print(compare_dictionaries(dict1, dict2))


#4. The build_xml_element function receives the following parameters: tag, content, and key-value elements given as
# name-parameters. Build and return a string that represents the corresponding XML element.

def build_xml_element(tag, content, **key_value_elem):
    attributes = ' '.join(f'{key}="{value}"' for key, value in key_value_elem.items())
    return f'<{tag} {attributes}> {content} </{tag}>'

    return corresponding_xml_elem

print(build_xml_element ("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid "))


#5.The validate_dict function that receives as a parameter a set of tuples ( that represents validation rules for a dictionary
# that has strings as keys and values) and a dictionary. A rule is defined as follows: (key, "prefix", "middle", "suffix").
# A value is considered valid if it starts with "prefix", "middle" is inside the value (not at the beginning or end) and ends
# with "suffix". The function will return True if the given dictionary matches all the rules, False otherwise.

def validate_dict(rules, dictionary_input):

     for rule in rules:
         key, prefix, middle, suffix = rule

         if key not in dictionary_input:
             return False

         elem = dictionary_input[key]

         if not elem.startswith(prefix) or not elem.endswith(suffix):
             return False

         start_index = len(prefix)
         end_index = -len(suffix) if suffix else None
         middle_content = elem[start_index:end_index]

         if middle in middle_content:
             if elem.startswith(middle) or elem.endswith(middle):
                 return False
         elif middle:
             return False

     return True

rules = {("key1", "", "inside", ""), ("key2", "start", "middle", "winter")}
d = {"key1": "come inside, it's too cold out", "key3": "this is not valid"}

result = validate_dict(rules, d)
print("5:", result)



#6. Write a function that receives as a parameter a list and returns a tuple (a, b), representing the number of unique
# elements in the list, and b representing the number of duplicate elements in the list (use sets to achieve this objective).

def num_of_elements(input_list):

    set_input_list = set(input_list)
    num_unique_elem = 0
    num_duplicate_elem = 0

    for element in set_input_list:
        if input_list.count(element) == 1:
            num_unique_elem += 1
        else:
            num_duplicate_elem += 1

    return (num_unique_elem, num_duplicate_elem)

print(num_of_elements([1, 2, 3, 3, 3, 4, 10, 10, 5, 7, 7]))


#7. Write a function that receives a variable number of sets and returns a dictionary with the following operations from
# all sets two by two: reunion, intersection, a-b, b-a. The key will have the following form: "a op b", where a and b are
# two sets, and op is the applied operator: |, &, -.


def operations_dictionary(*sets):
    sets_list = list(sets)
    op_dictionary = {}
    for index_1 in range(len(sets_list)):
        for index_2 in range(index_1 + 1, len(sets_list)):
            a, b = sets_list[index_1], sets_list[index_2]
            union = f"{a} | {b}"
            op_dictionary[union] = a | b

            intersection = f"{a} & {b}"
            op_dictionary[intersection] = a & b

            a_minus_b = f"{a} - {b}"
            op_dictionary[a_minus_b] = a - b

            b_minus_a = f"{b} - {a}"
            op_dictionary[b_minus_a] = b - a

    return op_dictionary

result = operations_dictionary({1,2}, {2,3})

for key, value in result.items():
    print(f"{key}: {value}")


#10. Write a function that receives a single dict parameter named mapping. This dictionary always contains a string
# key "start". Starting with the value of this key you must obtain a list of objects by iterating over mapping in the
# following way: the value of the current key is the key for the next value, until you find a loop (a key that was visited
# before). The function must return the list of objects obtained as previously described

def mapping_loop(mapping):
    key = 'start'
    visited = set()
    result = []

    while key not in visited and key in mapping:
        visited.add(key)
        result.append(mapping[key])
        key = mapping[key]

    return result[:-1]

result = mapping_loop({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})
print(result)


#11. Write a function that receives a variable number of positional arguments and a variable number of keyword arguments
# and will return the number of positional arguments whose values can be found among keyword arguments values.

def num_of_args(*pos_args, **keyword_args):
    counter = 0
    for pos_arg in pos_args:
        if pos_arg in keyword_args.values():
            counter += 1
    return counter

print(num_of_args(1, 2, 3, 4, x=1, y=2, z=3, w=5))

#sau

def num_of_args2(*pos_args, **keyword_args):
    return sum(1 for pos_arg in pos_args if pos_arg in keyword_args.values())

print(num_of_args2(1, 2, 3, 4, x=1, y=2, z=3, w=5))

print("--------------------------")


def manhattan_distance(state):
    min_distance = float('inf')  # Vom seta inițial distanța la o valoare foarte mare

    for empty_i in range(3):
        for empty_j in range(3):
            distance = 0
            for i in range(3):
                for j in range(3):
                    if state[i][j] != 0:  # Ignoram celula goală
                        correct_i, correct_j = (state[i][j] - 1) // 3, (
                                    state[i][j] - 1) % 3  # Poziția corectă pentru valoarea curentă

                        # Modificăm poziția corectă dacă este acolo unde ar fi celula goală
                        while correct_i == empty_i and correct_j == empty_j:
                            correct_i, correct_j = (correct_i * 3 + correct_j + 1) // 3, (
                                        correct_i * 3 + correct_j + 1) % 3

                        distance += abs(i - correct_i) + abs(j - correct_j)
            min_distance = min(min_distance, distance)  # Actualizăm distanța minimă

    return min_distance


# Test
matrix = [
    [1, 3, 2],
    [4, 5, 8],
    [6, 7, 0]
]
print(manhattan_distance(matrix))


def hamming_distance_for_target(board, target):
    distance = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != target[i][j] and board[i][j] != 0:
                distance += 1
    return distance

def hamming_distance(board):
    # Generează toate pozițiile posibile pentru 0
    targets = [
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
        [[1, 0, 2], [3, 4, 5], [6, 7, 8]],
        [[1, 2, 0], [3, 4, 5], [6, 7, 8]],
        [[1, 2, 3], [0, 4, 5], [6, 7, 8]],
        [[1, 2, 3], [3, 0, 5], [6, 7, 8]],
        [[1, 2, 3], [3, 4, 0], [6, 7, 8]],
        [[1, 2, 3], [3, 4, 5], [0, 7, 8]],
        [[1, 2, 3], [3, 4, 5], [6, 0, 8]],
        [[1, 2, 3], [3, 4, 5], [6, 7, 0]]
    ]

    return min(hamming_distance_for_target(board, target) for target in targets)

# Exemplu de utilizare
board = [
    [1, 2, 3],
    [4, 6, 0],
    [7, 5, 8]
]

print(hamming_distance(board))


def generate_targets():
    # Matricea inițială
    initial = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    targets = []

    # Parcurgem fiecare poziție din matrice
    for i in range(3):
        for j in range(3):
            # Creăm o copie a configurației inițiale
            target = [row[:] for row in initial]
            # Mutăm 9 (care reprezintă caseta goală, sau 0) în poziția curentă
            target[i][j] = 0
            # Găsim poziția inițială a 9 și o înlocuim cu valoarea din poziția curentă
            for x in range(3):
                for y in range(3):
                    if initial[x][y] == 9:
                        target[x][y] = initial[i][j]
            # Adăugăm targetul generat la listă
            targets.append(target)

    return targets


targets = generate_targets()

# Afișăm targeturile generate
for target in targets:
    for row in target:
        print(row)
    print("\n")
















