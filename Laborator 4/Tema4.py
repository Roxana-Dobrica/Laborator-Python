#1. Write a Python class that simulates a Stack. The class should implement methods like push, pop, peek (the last two
# methods should return None if no element is present in the stack).

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            last_item = self.items[-1]
            self.items = self.items[0:len(self.items) - 1]
            return last_item
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


#2. Write a Python class that simulates a Queue. The class should implement methods like push, pop, peek (the last two methods
# should return None if no element is present in the queue).

class Queue:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            first_item = self.items[0]
            self.items = self.items[1:]
            return first_item
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


#3. Write a Python class that simulates a matrix of size NxM, with N and M provided at initialization. The class should
# provide methods to access elements (get and set methods) and some methematical functions such as transpose, matrix
# multiplication and a method that allows iterating through all elements form a matrix an apply a transformation over
# them (via a lambda function).

class Matrix:

    def __init__(self, N, M, initial_value=0):
        self.rows = N
        self.columns = M
        self.data = [[initial_value for _ in range(M)] for _ in range(N)]

    def get(self, i, j):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            return self.data[i][j]
        else:
            raise ValueError("Index out of bounds")

    def set(self, i, j, value):
        if 0 <= i < self.rows and 0 <= j < self.columns:
            self.data[i][j] = value
        else:
            raise ValueError("Index out of bounds")

    def transpose(self):
        transposed_data = [list(row) for row in zip(*self.data)]
        result_matrix = Matrix(len(transposed_data), len(transposed_data[0]))
        result_matrix.data = transposed_data
        return result_matrix

    def multiply(self, other):
        if self.columns != other.rows:
            raise ValueError("Numbers of columns in the first matrix must be equal to the numbers of rows in the second matrix")

        result = Matrix(self.rows, other.columns)
        for i in range(self.rows):
            for j in range(other.columns):
                sum = 0
                for k in range(self.columns):
                    sum += self.get(i, k) * other.get(k, j)
                result.set(i, j, sum)
        return result

    def apply(self, funct):
        for i in range(self.rows):
            for j in range(self.columns):
                self.data[i][j] = funct(i, j, self.data[i][j])
        return self


if __name__ == '__main__':
    print("Stack:")
    stack = Stack()
    stack.push(7)
    stack.push(8)
    stack.push(9)
    print(stack)
    print("Size: ", stack.size())
    print("Pop: ", stack.pop())
    print("Peek: ", stack.peek())
    print(stack)
    print()

    print("Queue:")
    queue = Queue()
    queue.push(7)
    queue.push(8)
    queue.push(9)
    print(queue)
    print("Size: ", queue.size())
    print("Pop: ", queue.pop())
    print("Peek: ", queue.peek())
    print(queue)
    print()

    print("Matrix:")
    matrix = Matrix(2, 3, 3)
    print("Element at (1, 0):", matrix.get(1, 0))
    matrix.set(0, 2, 5)
    print("Element at (0, 2) after setting:", matrix.get(0, 2))
    print("Transpose of Matrix:")
    matrix_transpose = matrix.transpose()
    for i in range(matrix_transpose.rows):
        for j in range(matrix_transpose.columns):
            print(matrix_transpose.get(i, j), end=' ')
        print()

    matrix_2 = Matrix(3, 2)
    matrix_2.set(0, 0, 2)
    matrix_2.set(1, 0, 3)
    matrix_2.set(2, 0, 4)
    matrix_2.set(0, 1, 5)
    matrix_2.set(1, 1, 6)
    matrix_2.set(2, 1, 7)
    product = matrix.multiply(matrix_2)
    print("Result of Matrix multiplication:")
    for i in range(product.rows):
        for j in range(product.columns):
            print(product.get(i, j), end=' ')
        print()











