"""
author: Divyanshi Arora
date: 2025-06-01
description: This is code for the second assignment of the internship.
Problem Statement: Create a Python program that implements a singly linked list using Object-Oriented Programming (OOP) principles. Your implementation should include the following: A Node class to represent each node in the list. A LinkedList class to manage the nodes, with methods to: Add a node to the end of the list Print the list Delete the nth node (where n is a 1-based index) Include exception handling to manage edge cases such as: Deleting a node from an empty list Deleting a node with an index out of range Test your implementation with at least one sample list.
"""
import json
#Node and LinkedList classes to implement singly linked list
class Node:
    def __init__(self, data):
        self.data=data
        self.next=None

class LinkedList:
    def __init__(self):
        self.head=None
    
    def add(self, data):
        try:
            new_node=Node(data)
            if not self.head:
                self.head=new_node
            else:
                current=self.head
                while current.next:
                    current=current.next
                current.next=new_node
        except Exception as e:
            print(f"Error adding node: {e}")
    
    def show(self):
        try:
            if not self.head:
                print("Empty Linked List")
                return
            current=self.head
            result=[]
            while current:
                result.append(str(current.data))
                current=current.next
            print("->".join(result))
        except Exception as e:
            print(f"Error showing list: {e}")
    
    def delete(self, pos):
        try:
            if not self.head:
                print("Nothing to delete")
                return
            if pos < 1:
                print("Invalid position")
                return
            if pos==1:
                self.head=self.head.next
                return
            current=self.head
            for i in range(pos - 2):
                if not current.next:
                    print("Position doesn't exist")
                    return
                current=current.next
            if not current.next:
                print("Position doesn't exist")
                return
            current.next=current.next.next
        except Exception as e:
            print(f"Error deleting node: {e}")


# Function to run test cases from a JSON file added a json file which contains test cases
def run_test_cases(filename, linked_list):
    print("Running test cases from file:", filename)
    print("The following operations will be performed on the linked list:")
    try:
        with open(filename, 'r') as f:
            test_cases=json.load(f)
    except Exception as e:
        print("Error reading test cases file:", e)
        return

    for i, case in enumerate(test_cases, 1):
        try:
            op=case.get("operation")
            print(f"\nTest case {i}: Operation={op}")
            if op=="add":
                val=case.get("value")
                print(f"Adding value: {val}")
                linked_list.add(val)
            elif op=="show":
                print("Current list:")
                linked_list.show()
            elif op=="delete":
                pos=case.get("position")
                print(f"Deleting node at position: {pos}")
                linked_list.delete(pos)
            else:
                print("Unknown operation:", op)
        except Exception as e:
            print(f"Error in test case {i}: {e}")

# Main function to allow user to run operations or run test cases from a file
def main():
    while True:
        print("Choose an option:")
        print("1.Run test cases from file")
        print("2.Try linked list interactively")
        print("3.Exit")
        choice=input("? ")
        print("Initializing empty linked list")
        if choice=="1":
            lnklst_test=LinkedList()
            run_test_cases("test_cases.json", lnklst_test)
        elif choice=="2":
            lnklst=LinkedList()
            while True:
                print("\n1.Add\n2.Show\n3.Delete\n4.Exit")
                choice=input("? ")

                if choice=="1":
                    val=input("Value: ")
                    try:
                        val=int(val)
                    except Exception as e:
                        print(f"Invalid input for value: {e}")
                        continue
                    lnklst.add(val)
                    print("Added")
                    lnklst.show()

                elif choice=="2":
                    lnklst.show()

                elif choice=="3":
                    try:
                        pos=int(input("Position: "))
                        lnklst.delete(pos)
                    except Exception as e:
                        print(f"Invalid input for position: {e}")
                    lnklst.show()

                elif choice=="4":
                    break
                else:
                    print("Invalid")
        elif choice=="3":
            break
        else:
            print("Invalid choice")

if __name__=="__main__":
    main()
