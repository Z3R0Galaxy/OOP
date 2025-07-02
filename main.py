from random import randint
import csv

# Function to simulate clearing the screen
def clear_screen():
    print("\n" * 100)

# User login and account creation
def log_in():
    clear_screen()
    has_account = input("Do you have an account Y/N: ")  # Prompt the user to check if they have an account

    if has_account.lower().strip() == "y":
        while True:
            clear_screen()
            username = input("Enter username: ").lower().strip()
            bankNum = input("Enter bank number: ")

            with open("bank.csv", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['Username'] == username and row['Bank Number'] == bankNum:
                        print("Valid user")
                        input("Press enter to continue...")
                        clear_screen()
                        return username
            print("Username or Bank Number is incorrect. Please try again")
            input("Press enter to try again...")

    elif has_account.lower().strip() == "n":
        clear_screen()
        print("Entering new sign-up protocol")

        def user():
            global nuser
            nuser = input("Please enter your username: ").lower().strip()
            conf = input(f"Your name is '{nuser}', is this correct Y/N: ")
            if conf.lower().strip() != "y":
                user()
            else:
                print("Name saved")

        def bankNum():
            global nbankNum
            nbankNum = randint(0, 99999999)
            print(f"Your auto generated bank number is {nbankNum}")

        def balacnce():
            global nbalance
            nbalance = input("Please enter your balance: $")
            conf = input(f"Your balance is ${nbalance}, is this correct Y/N: ")
            if conf.lower().strip() != "y":
                balacnce()
            else:
                print("Balance saved")

        def save():
            fieldnames = ['Username', 'Bank Number', 'Balance']
            with open('bank.csv', mode='a', newline='') as f:
                write_header = f.tell() == 0
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if write_header:
                    writer.writeheader()
                writer.writerow({'Username': nuser, 'Bank Number': nbankNum, 'Balance': nbalance})
            print("New user registered")
            return nuser

        user()
        bankNum()
        balacnce()
        new_user = save()
        print("The program will now restart. Please log in with your new account.")
        input("Press enter to continue...")
        clear_screen()
        log_in()
        return new_user

    else:
        print("You need an account to use the program. Restarting...")
        input("Press enter to continue...")
        clear_screen()
        return log_in()

# Menu selection
def selection():
    try:
        choice = int(input(
            "\nSelect a number:\n"
            "1. View account details\n"
            "2. Withdraw funds\n"
            "3. Deposit funds\n"
            "4. Exit program\n"
            "Enter choice: "
        ))
        if choice not in (1, 2, 3, 4):
            print("Invalid selection. Please try again.")
            return selection()
        else:
            clear_screen()
            return choice
    except ValueError:
        print("Please enter a valid number.")
        return selection()

# View user account
def view(user):
    clear_screen()
    with open("bank.csv", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == user:
                print("\n=== Account Details ===")
                print(f"Username: {row['Username']}")
                print(f"Bank Number: {row['Bank Number']}")
                print(f"Balance: ${row['Balance']}")
                input("Press enter to return to main menu")
                clear_screen()
                return
    print("User not found.")
    input("Press enter to return to main menu")
    clear_screen()

# Withdraw funds
def withdraw(user):
    clear_screen()
    print("\n=== Withdraw funds ===")
    rows = []
    with open("bank.csv", mode="r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == user:
                print(f"Current balance: ${row['Balance']}")
                Balance = float(row['Balance'])
                amount = float(input("Enter amount to withdraw: $"))
                if amount > Balance:
                    print("You don't have enough funds.")
                    input("Press enter to try again...")
                    return withdraw(user)
                row['Balance'] = round((Balance - amount), 3)
                print(f"Your balance is now ${row['Balance']}")
            rows.append(row)

    with open("bank.csv", mode="w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Username', 'Bank Number', 'Balance'])
        writer.writeheader()
        writer.writerows(rows)
    input("Press enter to return to main menu")
    clear_screen()

# Deposit funds
def deposit(user):
    clear_screen()
    print("\n=== Deposit funds ===")
    rows = []
    with open("bank.csv", mode="r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Username'] == user:
                print(f"Current balance: ${row['Balance']}")
                Balance = float(row['Balance'])
                amount = float(input("Enter amount to deposit: $"))
                row['Balance'] = round((Balance + amount), 3)
                print(f"Your balance is now ${row['Balance']}")
            rows.append(row)

    with open("bank.csv", mode="w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Username', 'Bank Number', 'Balance'])
        writer.writeheader()
        writer.writerows(rows)
    input("Press enter to return to main menu")
    clear_screen()

# Main program loop
def main():
    user = log_in()
    while True:
        choice = selection()
        if choice == 1:
            view(user)
        elif choice == 2:
            withdraw(user)
        elif choice == 3:
            deposit(user)
        elif choice == 4:
            print("Exiting program. Goodbye!")
            break

if __name__ == '__main__':
    main()