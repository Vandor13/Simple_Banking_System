# Write your code here
import random
import sqlite3
import textwrap
import bankingstrings


def calculate_checksum(number):
    string_number = str(number)
    digit_sum = 0
    double = True
    for c in string_number:
        digit = int(c)
        if double:
            digit = digit * 2
        double = not double
        if digit > 9:
            digit -= 9
        digit_sum += digit
    checksum = 10 - digit_sum % 10
    if checksum == 10:
        checksum = 0
    string_number += str(checksum)
    return int(string_number)


def get_pin(card_number):
    cur.execute('''
    SELECT pin FROM card where number = {}'''.format(card_number))
    return cur.fetchone()[0]


def insert_card(connection, cursor, card_number, pin):
    cursor.execute('''
        INSERT INTO card (number, pin) VALUES ({}, {})'''.format(str(card_number), str(pin)))
    connection.commit()


def check_card_and_pin(cursor, card_number, pin):
    cursor.execute('''
    SELECT * FROM card where number = {} AND pin = {}'''.format(card_number, pin))
    check_result = cursor.fetchone()
    if debug:
        print(check_result)
    if check_result:
        return True
    else:
        return False

def check_card(cursor, card_number):
    cursor.execute('''
        SELECT * FROM card where number = {}'''.format(card_number))
    check_result = cursor.fetchone()
    if debug:
        print(check_result)
    if check_result:
        return True
    else:
        return False


def get_balance(card_number):
    cur.execute('''
    SELECT balance FROM card where number = {}'''.format(card_number))
    return int(cur.fetchone()[0])


def add_money(connection, cursor, card_number, amount):
    sql_command = "UPDATE card SET balance = balance + {} WHERE number = {}".format(amount, card_number)
    cursor.execute(sql_command)
    connection.commit()
    print("Income was added!\n")


def transfer(connection, cursor, source, target, amount):
    sql_command1 = "UPDATE card SET balance = balance - {} WHERE number = {}".format(amount, source)
    cursor.execute(sql_command1)
    sql_command2 = "UPDATE card SET balance = balance + {} WHERE number = {}".format(amount, target)
    cursor.execute(sql_command2)
    connection.commit()
    print("Success!")


debug = True
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()

current_number = 400000000000001

cur.execute(
        '''CREATE TABLE IF NOT EXISTS card (
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0);
        '''
    )
conn.commit()
if debug:
    cur.execute("SELECT * FROM card")
    result = cur.fetchall()
    print(result)
cur.execute('''
SELECT MAX(number) FROM card''')

current_max = str(cur.fetchone()[0])[:-1]
if debug:
    print("Max is: " + current_max)
if current_max is not None and current_max != "Non":
    # print(cur.fetchone())
    current_number = int(current_max) + 1
    if debug:
        print("Current Number is:" + str(current_number))

print(bankingstrings.main_menu_string)

user_choice = int(input())
while user_choice != 0:
    if user_choice == 1:
        user_number = calculate_checksum(current_number)
        current_number += 1
        user_pin = random.randint(1111, 9999)
        print("""Your card has been created
Your card number:
{}
Your card PIN:
{}""".format(user_number, user_pin))
        insert_card(conn, cur, user_number, user_pin)  # card_safe[user_number] = user_pin
    elif user_choice == 2:
        card_input = int(input("Enter your card number:"))
        pin_input = int(input("Enter your PIN:"))
        if check_card_and_pin(cur, card_input, pin_input):
            print("You have successfully logged in")
            account_choice = int(input(bankingstrings.account_string))
            while True:
                if account_choice == 0:
                    break
                elif account_choice == 1:
                    print("Balance: {}".format(get_balance(card_input)))
                    account_choice = int(input(bankingstrings.account_string))
                elif account_choice == 2:
                    income_input = int(input("Enter income:\n"))
                    add_money(conn, cur, card_input, income_input)
                elif account_choice == 3:
                    print("Transfer")
                    target_card = int(input("Enter card number:\n"))
                    if calculate_checksum(target_card[:-1]) != target_card[-1]:
                        print("Probably you made a mistake in the card number. Please try again!")
                    elif not check_card(cur, target_card):
                        print("Such a card does not exist.")
                    else:
                        transfer_amount = int(input("Enter how much money you want to transfer:\n"))
                        if get_balance(card_input) < transfer_amount:
                            print("Not enough money!")
                        else:
                            transfer(conn, cur, card_input, target_card, transfer_amount)
                account_choice = int(input(bankingstrings.account_string))
        else:
            print("Wrong card number or PIN!")
    user_choice = int(input(bankingstrings.main_menu_string))

conn.close()
