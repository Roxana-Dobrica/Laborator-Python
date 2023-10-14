# 1. Find The greatest common divisor of multiple numbers read from the console.

def gcd(a, b):
    while(b != 0):
        temp = b
        b = a % b
        a = temp
    return a

input_string = input("Enter numbers separated by spaces: ")

numbers_as_strings = input_string.split()

numbers = [int(num) for num in numbers_as_strings]

result = gcd(numbers[0], numbers[1])
for num in numbers[2:]:
    result = gcd(result, num)

print(result)


#2. Write a script that calculates how many vowels are in a string.

input_string = input("Introduce a string: ")
num_of_vowels = 0
input_string = input_string.lower()
for letter in input_string:
    if letter in "aeiou":
        num_of_vowels += 1
print("Number of vowels in string:", num_of_vowels)


#3. Write a script that receives two strings and prints the number of occurrences of the first string in the second.

first_string = input("Introduce the first string: ")
second_string = input("Introduce the second string: ")

num_occurences = 0
n = len(first_string)

for i in range(len(second_string) - len(first_string) + 1):
    if second_string[i:i+len(first_string)] == first_string:
        num_occurences = num_occurences + 1

print("Number of occurences of the first string in the second:", num_occurences)


#4. Write a script that converts a string of characters written in UpperCamelCase into lowercase_with_underscores.

input_string = input("Introduce a string: ")

converted_string = input_string[0].lower()

previous_space = False

for letter in input_string[1:]:
    if letter.isupper():
        if previous_space:
            converted_string += letter.lower()
            previous_space = False
        else:
            converted_string += "_" + letter.lower()
    else:
        converted_string += letter

        previous_space = (letter == ' ')

print("Converted string:", converted_string)


#5. Given a square matrix of characters write a script that prints the string obtained by going through the matrix in spiral
# order (as in the example):

def matrix_spiral_order(matrix):

    if not matrix:
        return []
    top = 0
    left = 0
    right = len(matrix[0]) - 1
    bottom = len(matrix) - 1
    result = []

    while top <= bottom and left <= right:

        for j in range (left, right + 1):
            result.append(matrix[top][j])

        for i in range(top + 1, bottom + 1):
            result.append(matrix[i][right])

        if top < bottom:
            for j in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][j])

        if left < right:
            for i in range(bottom - 1, top, -1):
                result.append(matrix[i][left])

        top +=1
        right -= 1
        bottom -= 1
        left += 1

        return "".join(result)

matrix = [
    ['f', 'i', 'r', 's'],
    ['n', '_', 'l', 't'],
    ['o', 'b', 'a', '_'],
    ['h', 't', 'y', 'p']
]

print(matrix_spiral_order(matrix))

# 6. Write a function that validates if a number is a palindrome.

def is_palindrome(number):

    inverse = 0
    number_copy = number
    while number_copy > 0:
        inverse = inverse * 10 + number_copy % 10
        number_copy //= 10
    if inverse == number:
        return True
    else:
        return False

number = 12321
if(is_palindrome(number)):
    print("The number", number, "is a palindrome")
else:
    print("The number", number, "isn't a palindrome")

#7. Write a function that extract a number from a text (for example if the text is "An apple is 123 USD",
# this function will return 123, or if the text is "abc123abc" the function will extract 123).
# The function will extract only the first number that is found.

def extract_number(input_text):
    extracted_number = ""

    i = 0
    while i < len(input_text):
        if input_text[i] in "1234567890":
            extracted_number += input_text[i]
            i += 1
            while i < len(input_text) and input_text[i] in "1234567890":
                extracted_number += input_text[i]
                i += 1
            break
        i += 1

    return int(extracted_number) if extracted_number else None

print(extract_number("An apple is 123 USD 345"))
print(extract_number("abc123abc"))


#8. Write a function that counts how many bits with value 1 a number has.
# For example for number 24, the binary format is 00011000, meaning 2 bits with value "1"

def count_bits(number):
    return bin(number).count('1')

print(count_bits(24))


#9. Write a functions that determine the most common letter in a string. For example if the string is "an apple is not a tomato",
# then the most common character is "a" (4 times).
# Only letters (A-Z or a-z) are to be considered. Casing should not be considered "A" and "a" represent the same character.

def most_common_letter(input_string):

    input_string = input_string.lower()
    letters_frequencies = {}

    for letter in input_string:
        if letter.isalpha():
            if letter in letters_frequencies:
                letters_frequencies[letter] += 1
            else:
                letters_frequencies[letter] = 1

    result_most_common = max(letters_frequencies, key=letters_frequencies.get)

    print("The most common letter is: ", result_most_common)

most_common_letter("an apple is not a tomato")


#10. Write a function that counts how many words exists in a text. A text is considered to be form out of words that are
# separated by only ONE space. For example: "I have Python exam" has 4 words.

def count_words(input_text):

    return len(input_text.split(' '))

print(count_words("I have Python exam"))











