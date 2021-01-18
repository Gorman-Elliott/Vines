# 5/1/2020
# Elliott Gorman
# ITSW 1359
# VINES - STACK ABSTRACT DATA TYPE

class Stack():

    def __init__(self):
        self.stack = []

        #set stack size to -1 so when first object is pushed
        # its reference is correct at 0
        self.size = -1

    def push(self, object):
        self.stack.append(object)
        self.size += 1

    def pop(self):
        if (self.isEmpty()):
            raise EmptyStackException('The Stack is already Empty.')
        else:
            removedElement = self.stack.pop(self.size)
            self.size -= 1
            return removedElement

    def peek(self):
        if (not self.isEmpty()):
            return self.stack[self.size]

    def isEmpty(self):
        return self.size == -1

    def clear(self):
        self.stack.clear()

        #set size back to -1
        self.size = -1
