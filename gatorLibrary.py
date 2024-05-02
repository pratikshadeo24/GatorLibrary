import sys
import time
import re

class BinaryMinHeap:

    def __init__(self):
        # Initialize an empty heap with a maximum size of 20
        self.heap = []
        self.maxSize = 20

    @staticmethod
    def parent(idx):
        """
        Computes the index of the parent node given the index of a child node in the heap.

        Params:
            - idx (int): index of the child node

        Returns:
            int: Computed index of the parent node
        """
        return (idx - 1) // 2

    def insertReservation(self, res):
        """
        Inserts a reservation into the min-heap while maintaining the heap property.

        Params:
            - res (tuple): Reservation information represented as a tuple

        Returns:
            None
        """
        if len(self.heap) >= self.maxSize:
            # If the heap is full, print a message and return
            print("Reservation waitlist is full.")
            return

        # Append the reservation to the heap
        self.heap.append(res)
        i = len(self.heap) - 1

        # Maintain the heap property by swapping elements as needed
        while i != 0 and (
            self.heap[self.parent(i)][1] > self.heap[i][1]
            or (
                self.heap[self.parent(i)][1] == self.heap[i][1]
                and self.heap[self.parent(i)][2] > self.heap[i][2]
            )
        ):
            self.heap[i], self.heap[self.parent(i)] = (
                self.heap[self.parent(i)],
                self.heap[i],
            )
            i = self.parent(i)

    def heapify(self, idx):
        """
        Performs the heapify operation to maintain the min-heap property starting from a given index.

        Params:
            - i (int): Index from where the heapify operation should start

        Returns:
            None
        """
        smallest = idx
        lft = 2 * idx + 1
        rgt = 2 * idx + 2

        # Find the index of the smallest element among current node and its children
        if lft < len(self.heap) and self.heap[lft] < self.heap[idx]:
            smallest = lft
        if rgt < len(self.heap) and self.heap[rgt] < self.heap[smallest]:
            smallest = rgt

        # Swap elements if needed and recursively heapify the affected subtree
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self.heapify(smallest)

    def extractMin(self):
        """
        Extracts the minimum reservation from the heap based on the priority (and timestamp if priorities are equal).

        Params:
            None

        Returns:
            nextReservation (tuple): Information about the extracted reservation
        """
        nextReservation = min(self.heap, key=lambda x: (x[1], x[2]))
        self.heap.remove(nextReservation)
        return nextReservation


class Node:

    def __init__(self, bookID, bookName, authorNameName, availabilityStatus, borrowedBy=None):
        """
        Initialize a node in a Red-Black Tree.

        Params:
            - bookID (int): ID of the book
            - bookName (str): Name of the book
            - authorNameName (str): Name of the authorName of the book
            - availabilityStatus (str): Availability status of the book
            - borrowedBy (int): User who borrowed the book (default is None)
        """
        self.bookID = bookID
        self.bookName = bookName
        self.authorName = authorNameName
        self.availability = availabilityStatus
        self.borrowedBy = borrowedBy
        self.reservationHeap = BinaryMinHeap()
        self.color = 1
        self.left = None
        self.right = None
        self.parent = None


class RedBlackTree:

    def __init__(self):
        """Initialize the tree with a null node (TNULL) representing the end of the tree
        """
        self.TNULL = Node(0, None, None, False)
        self.TNULL.color = 0  # Set the initial color of the null node to black
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL  # Root of the tree is initially set to the null node
        self.colorFlips = 0

    def searchTreeHelper(self, node, bookID):
        """
        Helper for searching the tree for a specific BookID.

        Params:
            - node (Node): a node
            - bookID (int): ID of the book

        Returns:
            Node that has the BookID
        """
        # Base case: If the current node is the null node (TNULL) or the book ID matches
        if node == self.TNULL or bookID == node.bookID:
            return node

        # If the book ID is less than the current node's ID, search in the left subtree
        if bookID < node.bookID:
            return self.searchTreeHelper(node.left, bookID)

        # Otherwise, search in the right subtree
        return self.searchTreeHelper(node.right, bookID)

    def deleteFix(self, x):
        """
        Balances the tree after deletion of a Node.

        Params:
            - node (Node): a node
            - bookID (int): ID of a book

        Return:
             None
        """
        while x != self.root and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right  # Sibling node
                if s.color == 1:
                    # Case 1: Sibling is red, perform a color flip.
                    if s.color == 1:
                        self.colorFlips += 1
                    s.color = 0
                    if x.parent.color == 0:
                        self.colorFlips += 1
                    x.parent.color = 1
                    self.leftRotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    # Case 2: Both nephews are black, paint sibling red.
                    if s.color == 0:
                        self.colorFlips += 1
                    s.color = 1
                    x = x.parent
                else:
                    # Case 3: At least one nephew is red, perform rotations.
                    if s.right.color == 0:
                        if s.left.color == 1:
                            self.colorFlips += 1
                        s.left.color = 0
                        if s.color == 0:
                            self.colorFlips += 1
                        s.color = 1
                        self.rightRotate(s)
                        s = x.parent.right

                    if s.color != x.parent.color:
                        self.colorFlips += 1
                    s.color = x.parent.color
                    if x.parent.color == 1:
                        self.colorFlips += 1
                    x.parent.color = 0
                    if s.right.color == 1:
                        self.colorFlips += 1
                    s.right.color = 0
                    self.leftRotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left  # Sibling node
                if s.color == 1:
                    # Case 1: Sibling is red, perform a color flip.
                    if s.color == 1:
                        self.colorFlips += 1
                    s.color = 0
                    if x.parent.color == 0:
                        self.colorFlips += 1
                    x.parent.color = 1
                    self.rightRotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    # Case 2: Both nephews are black, paint sibling red.
                    s.color = 1
                    x = x.parent
                else:
                    # Case 3: At least one nephew is red, perform rotations.
                    if s.left.color == 0:
                        if s.right.color == 1:
                            self.colorFlips += 1
                        s.right.color = 0
                        if s.color == 0:
                            self.colorFlips += 1
                        s.color = 1
                        self.leftRotate(s)
                        s = x.parent.left

                    if s.color != x.parent.color:
                        self.colorFlips += 1
                    s.color = x.parent.color
                    if x.parent.color == 1:
                        self.colorFlips += 1
                    x.parent.color = 0
                    if s.left.color == 1:
                        self.colorFlips += 1
                    s.left.color = 0
                    self.rightRotate(x.parent)
                    x = self.root
            x.color = 0

    def __rbTransplant(self, u, v):
        """
        Replace one subtree rooted at node 'u' with another subtree rooted at node 'v'.

        Params:
            - u (Node): The node whose subtree is to be replaced
            - v (Node): The node whose subtree is to replace the subtree rooted at 'u'.

        Returns:
            None
        """
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def deleteNodeHelper(self, node, bookID):
        """
        Helper for single Node deletion.

        Params:
            - node (Node): a node
            - bookID (int): ID of a book

        Returns:
             None
        """
        z = self.TNULL
        while node != self.TNULL:  # Search for the node having that value/key and store it in 'z'
            if node.bookID == bookID:
                z = node

            if node.bookID <= bookID:
                node = node.right
            else:
                node = node.left

        # If Key is not present then deletion not possible so return
        if z == self.TNULL:
            print("Cannot find key in the tree")
            return

        y = z
        yOriginalColor = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rbTransplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rbTransplant(z, z.left)
        else:
            y = self.minimum(z.right)
            yOriginalColor = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rbTransplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rbTransplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if yOriginalColor == 0:
            self.deleteFix(x)

    def fixInsert(self, node):
        """
        Balance the tree after insertion of a Book

        Params:
            - node (Node): a node

        Returns:
            None
        """
        while node.parent.color == 1:  # While parent is red
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left  # Uncle node
                if u.color == 1:
                    # Case 1: Uncle is red, perform a color flip.
                    self.colorFlips += 1
                    u.color = 0  # Uncle becomes black
                    if node.parent.color == 1:
                        self.colorFlips += 1
                    node.parent.color = 0  # Parent becomes black
                    if node.parent.parent.color == 0:
                        self.colorFlips += 1
                    node.parent.parent.color = 1  # Grandparent becomes red
                    node = node.parent.parent
                else:
                    # Case 2: Uncle is black, perform rotations.
                    if node == node.parent.left:
                        node = node.parent
                        self.rightRotate(node)
                    if node.parent.color == 1:
                        self.colorFlips += 1
                    node.parent.color = 0  # Parent becomes black
                    node.parent.parent.color = 1  # Grandparent becomes red
                    self.leftRotate(node.parent.parent)
            else:
                u = node.parent.parent.right  # Uncle node

                if u.color == 1:
                    # Case 1: Uncle is red, perform a color flip.
                    self.colorFlips += 1
                    u.color = 0  # Uncle becomes black
                    if node.parent.color == 1:
                        self.colorFlips += 1
                    node.parent.color = 0  # Parent becomes black
                    if node.parent.parent.color == 0:
                        self.colorFlips += 1
                    node.parent.parent.color = 1  # Grandparent becomes red
                    node = node.parent.parent
                else:
                    # Case 2: Uncle is black, perform rotations.
                    if node == node.parent.right:
                        node = node.parent
                        self.leftRotate(node)
                    if node.parent.color == 1:
                        self.colorFlips += 1
                    node.parent.color = 0  # Parent becomes black
                    if node.parent.parent.color == 0:
                        self.colorFlips += 1
                    node.parent.parent.color = 1  # Grandparent becomes red
                    self.rightRotate(node.parent.parent)

            if node == self.root:
                break
            if self.root.color == 1:
                self.colorFlips += 1
        self.root.color = 0

    def minimum(self, node):
        """
        Finds the node with the smallest key in the subtree rooted at the given node.

        Params:
            - node (Node): root of the subtree

        Returns:
            node (Node): Node with the smallest key in the subtree
        """
        while node.left != self.TNULL:
            node = node.left
        return node

    def leftRotate(self, x):
        """
        Performs a left rotation around the specified node x

        Params:
            - x (Node): a node

        Returns:
            None
        """
        y = x.right  # Y = Right child of x
        x.right = y.left  # Change right child of x to left child of y
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent  # Change parent of y as parent of x
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rightRotate(self, x):
        """
        Performs a right rotation around the specified node x

        Params:
            - x (Node): a node

        Returns:
            None
        """
        y = x.left  # Y = Left child of x
        x.left = y.right  # Change left child of x to right child of y
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent  # Change parent of y as parent of x
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def addReservation(self, bookID, patronID, priorityNumber):
        """
        Adds a new reservation (PatronID) to the min-heap

        Params:
            - bookID (int): ID of Book
            - patronID (int): ID of Patron
            - priorityNumber (int): Priority

        Returns:
            None
        """
        node = self.searchTreeHelper(self.root, bookID)
        if node != self.TNULL:
            timestamp = time.time()  # High precision timestamp
            node.reservationHeap.insertReservation(
                (patronID, priorityNumber, timestamp)
            )
        else:
            print(f"Book {bookID} not found in the library\n")

    def inOrderPrintBooks(self, node, bookID1, bookID2):
        """
        In-order traversal of a binary search tree to print book details within a specified range.

        Params:
            - node (Node): The current node being processed
            - bookID1 (int): The lower bound of the bookID range
            - bookID2 (int): The upper bound of the bookID range

        Returns:
            None
        """
        if node is None or node == self.TNULL:
            return

        # Traverse left subtree if it might contain books within the range
        if bookID1 < node.bookID:
            self.inOrderPrintBooks(node.left, bookID1, bookID2)

        # Print the node's book if it's within the range
        if bookID1 <= node.bookID <= bookID2:
            self.printBookDetails(node)

        # Traverse right subtree if it might contain books within the range
        if bookID2 > node.bookID:
            self.inOrderPrintBooks(node.right, bookID1, bookID2)

    def printBook(self, bookID):
        """
        Print information about a specific book identified by its unique bookID.

        Params:
            - bookID (int): ID of the book

        Returns:
            None
        """
        node = self.searchTreeHelper(self.root, bookID)
        if node != self.TNULL:
            self.printBookDetails(node)
        else:
            print(f"Book {bookID} not found in the library\n")

    def printBooks(self, bookID1, bookID2):
        """
        Print information about all books with bookIDs in the given range.

        Params:
            - bookID1 (int): initial BookID
            - bookID2 (int): end BookID

        Returns:
             None
        """
        self.inOrderPrintBooks(self.root, bookID1, bookID2)

    def insertBook(self, bookID, bookName, authorName, availabilityStatus):
        """
        Insert a book as a Node.

        Params:
            - bookID (int): ID of the book
            - bookName (str): Name of the book
            - authorName (str): Name of the authorName
            - availability (str): Status of availability of the book

        Returns:
             None
        """
        node = Node(bookID, bookName, authorName, availabilityStatus)
        node.parent = None
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = 1  # Set root colour as Red

        y = None
        x = self.root

        while x != self.TNULL:  # Find position for new node
            y = x
            if node.bookID < x.bookID:
                x = x.left
            else:
                x = x.right

        node.parent = y  # Set parent of Node as y
        if y is None:
            self.root = node
        elif node.bookID < y.bookID:  # Check if it is right Node or Left Node by checking the value
            y.left = node
        else:
            y.right = node

        if node.parent is None:  # Root node is always Black
            node.color = 0
            return

        if node.parent.parent is None:  # If parent of node is Root Node
            return

        self.fixInsert(node)  # Else call for Fix Up

    def borrowBook(self, patronID, bookID, patronPriority):
        """
        Allow a patron to borrow a book that is available and update the status of the book.

        Params:
            - patronID (int): ID of the patron
            - bookID (int): ID of the book
            - patronPriority (int): Priority of the patron

        Returns:
             None
        """
        # Search for the book in the tree using its ID
        node = self.searchTreeHelper(self.root, bookID)
        if node != self.TNULL:
            # If the book is found and is available for borrowing
            if node.availability and (
                node.borrowedBy is None or node.borrowedBy != patronID
            ):  
                node.availability = False  # Set the book as borrowed and update the borrower's ID
                node.borrowedBy = patronID
                print(f"Book {bookID} Borrowed by Patron {patronID}\n")
            else:
                # If the book is not available, add the patron's reservation
                # The reservation is added to the book's min-heap based on priority
                self.addReservation(bookID, patronID, patronPriority)
                print(f"Book {bookID} Reserved by Patron {patronID}\n")
        else:
            # If the book is not found in the library
            print(f"Book {bookID} not found in the library\n")

    def returnBook(self, patronID, bookID):
        """
        Allow a patron to return a borrowed book. Update the book's status and assign the book to the patron with
        highest priority in the Reservation Heap.

        Params:
            - patronID (int): ID of the patron
            - bookID (int): ID of thr book

        Returns:
            None
        """
        node = self.searchTreeHelper(self.root, bookID)
        if node != self.TNULL:
            if node.borrowedBy == patronID:
                node.availability = True
                node.borrowedBy = None
                print(f"Book {bookID} Returned by Patron {patronID}\n")

                # Check if there are reservations and assign to the next patron
                if len(node.reservationHeap.heap) > 0:
                    nextReservation = node.reservationHeap.extractMin()
                    node.availability = False
                    node.borrowedBy = nextReservation[0]
                    print(f"Book {bookID} Allotted to Patron {nextReservation[0]}\n")
                else:
                    # print("No reservations for this book. It is now available for borrowing.")
                    pass
            else:
                print(f"Patron {patronID} cannot return a book they haven't borrowed")
        else:
            print(f"Book {bookID} not found in the library\n")

    def deleteBook(self, bookID):
        """
        Delete the book from the library and notify the patrons in the reservation list that the book is no longer
        available to borrow.

        Params:
            - bookID (int): ID of the book

        Returns:
            None
        """
        node = self.searchTreeHelper(self.root, bookID)  # Search for the node (book) in the tree by its book ID
        if node != self.TNULL:
            # If the book is found, process the reservation list
            patronList = []
            # Extract and collect patrons from the book's reservation heap
            while len(node.reservationHeap.heap) > 0:
                nextReservation = node.reservationHeap.extractMin()
                patronList.append(str(nextReservation[0]))
            # Notify the patrons that the book is no longer available
            if len(patronList) == 0:
                print(f"Book {bookID} is no longer available\n")
            else:
                if len(patronList) == 1:
                    print(
                        f"Book {bookID} is no longer available. Reservations made by Patrons {', '.join(patronList)} "
                        f"has been cancelled!\n"
                    )
                else:
                    print(
                        f"Book {bookID} is no longer available. Reservations made by Patrons {', '.join(patronList)} "
                        f"have been cancelled!\n"
                    )
            # Delete the book from the tree
            self.deleteNodeHelper(self.root, bookID)
        else:
            # Handle the case where the bookID is not found in the library
            print(f"Book {bookID} not found in the library\n")

    def findClosestBook(self, targetID):
        """
        Find the book with an ID closest to the given ID. Print all the details about the book.

        Params:
            - targetID (int): Target book ID

        Returns:
            None
        """
        current = self.root
        closestLower = None
        closestHigher = None

        # Traverse the tree to find the closest lower and higher book IDs
        while current != self.TNULL:
            if current.bookID < targetID:
                closestLower = current
                current = current.right
            elif current.bookID > targetID:
                closestHigher = current
                current = current.left
            else:
                # Exact match found
                self.printBookDetails(current)
                return

        # Determine the closest book(s) and print details
        if closestLower and closestHigher:
            diffLower = targetID - closestLower.bookID
            diffHigher = closestHigher.bookID - targetID
            if diffLower < diffHigher:
                self.printBookDetails(closestLower)
            elif diffHigher < diffLower:
                self.printBookDetails(closestHigher)
            else:
                # In case of a tie, print both, ordered by book IDs
                books = [closestLower, closestHigher]
                books.sort(key=lambda x: x.bookID)
                for book in books:
                    self.printBookDetails(book)
        elif closestLower:
            self.printBookDetails(closestLower)
        elif closestHigher:
            self.printBookDetails(closestHigher)
        else:
            print("No closest book found")

    def colorFlipCount(self):
        """
        Tracks the occurrence of color changes in the tree nodes during the operations.

        Returns:
            None
        """
        print(f"Colour Flip Count: {self.colorFlips}\n")

    @staticmethod
    def sortReservations(node):
        """
        Sort the reservations by Priority and timestamp.

        Params:
            - node (Node): a node

        Returns:
            None
        """
        return sorted(node.reservationHeap.heap, key=lambda x: (x[1], x[2]))

    def printBookDetails(self, node):
        """
        Print details of a Book

        Params:
            - node (Node): a node

        Returns:
            None
        """
        print(f"BookID = {node.bookID}")
        print(f'Title = "{node.bookName}"')
        print(f'Author = "{node.authorName}"')
        print(f"Availability = \"{'Yes' if node.availability == 'Yes' else 'No'}\"")
        print(
            f"BorrowedBy = {node.borrowedBy if node.borrowedBy is not None else 'None'}"
        )
        print(f"Reservations = {[res[0] for res in self.sortReservations(node)]}\n")


def readInputFile(inputFile):
    """
    Read the input file and store all the lines in a list.

    Params:
    - inputFile (str): input file name

    Returns:
        A list with input file content

    Raises:
        FileNotFoundError: If the file does not exists
    """
    try:
        with open(inputFile, "r") as file:
            # Read the lines of the file and store them in a list
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"File not found: {inputFile}")
        return None


def parseLine(line):
    """
    Parse an input file line and extract method name and arguments.

    Params:
    - line (str): single line of the input file

    Returns:
        - methodName (str): extracted method name
        - argsList (list): list of arguments

    Raises:
        ValueError: If the line format is incorrect
    """
    # Regular expression to match the pattern
    pattern = r"(\w+)\((.*?)\)"
    match = re.match(pattern, line.strip())

    if match:
        methodName, args = match.groups()

        # Split arguments by comma and strip extra spaces and quotes
        # Handle both quoted and unquoted arguments
        argsList = [
            arg.strip().strip('"') for arg in re.split(r',\s*(?![^"]*"\B)', args)
        ]

        return methodName, argsList
    else:
        raise ValueError("Line format is incorrect")


def main(inputFile):
    # Create object of Red-Black Tree class
    bst = RedBlackTree()

    # Read the input file
    fileContents = readInputFile(inputFile)

    # Open the output file in append mode
    outputFileName = inputFileName.split(".")[0] + "_output_file.txt"
    with open(outputFileName, "w") as outputFile:
        # Redirect standard output to the output file
        sys.stdout = outputFile

        # Iterate over the input file content
        for operation in fileContents:
            # Separate method and arguments
            methodName, argsList = parseLine(operation)

            # Check the method and process
            if methodName == "InsertBook":
                bookID, bookName, authorName, availabilityStatus = (
                    int(argsList[0]),
                    argsList[1],
                    argsList[2],
                    argsList[3],
                )
                bst.insertBook(bookID, bookName, authorName, availabilityStatus)
            elif methodName == "PrintBook":
                bookID = int(argsList[0])
                bst.printBook(bookID)
            elif methodName == "PrintBooks":
                bookID1, bookID2 = int(argsList[0]), int(argsList[1])
                bst.printBooks(bookID1, bookID2)
            elif methodName == "BorrowBook":
                patronID, bookID, patronPriority = (
                    int(argsList[0]),
                    int(argsList[1]),
                    int(argsList[2]),
                )
                bst.borrowBook(patronID, bookID, patronPriority)
            elif methodName == "ReturnBook":
                patronID, bookID = int(argsList[0]), int(argsList[1])
                bst.returnBook(patronID, bookID)
            elif methodName == "DeleteBook":
                bookID = int(argsList[0])
                bst.deleteBook(bookID)
            elif methodName == "FindClosestBook":
                targetID = int(argsList[0])
                bst.findClosestBook(targetID)
            elif methodName == "ColorFlipCount":
                bst.colorFlipCount()
            elif methodName == "Quit":
                print("Program Terminated!!")
                break

        # Reset standard output to original
        sys.stdout = sys.__stdout__


if __name__ == "__main__":
    # Get input file name from command-line argument
    if len(sys.argv) != 2:
        print("Usage: python app.py inputFileName")
        sys.exit(1)

    inputFileName = sys.argv[1]

    # Call the main function with the input file
    main(inputFileName)
