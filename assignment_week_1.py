"""
author: Divyanshi Arora
date: 2025-06-25
description: This is code for the first assignment of the internship.
Problem Statement: Create lower triangular, upper triangular and pyramid containing the "*" character.
"""

#functions to print shapes
def print_upper_triangle(rows):
    for i in range(1, rows + 1):
        print('\t'+('*' * i))

def print_lower_triangle(rows):
    for i in range(rows, 0, -1):
        print('\t'+('*' * i))

def print_pyramid(rows):
    for i in range(1, rows + 1):
        space = ' ' * (rows - i)
        stars = '*' * (2 * i - 1)
        print('\t'+(space + stars))

#menu to choose shape
def menu():
    print("\n--- Menu ---")
    print("1. Print Upper Triangle")
    print("2. Print Lower Triangle")
    print("3. Print Pyramid")
    print("4. Exit")

while True:
    menu()
    choice = input("Enter your choice (1-4): ")
    if choice == '1':
        rows = int(input("Enter number of rows: "))
        print("\n\tUpper Triangle:\n")
        print_upper_triangle(rows)
    elif choice == '2':
        rows = int(input("Enter number of rows: "))
        print("\n\tLower Triangle:\n")
        print_lower_triangle(rows)
    elif choice == '3':
        rows = int(input("Enter number of rows: "))
        print("\n\tPyramid:\n")
        print_pyramid(rows)
    elif choice == '4':
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter a digit from 1 to 4.")
