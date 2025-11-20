
from pathlib import Path
import json
import random
import string
import streamlit as st


class Bank:
    database = 'database.json'  # main data
    data = []  # temporary data

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            # initialize empty database file
            with open(database, 'w') as fs:
                json.dump([], fs)
            data = []
    except Exception as err:
        print(f"an error occurred: {err}")

    @classmethod
    def __update(cls):
        with open(cls.database, 'w') as fs:
            json.dump(cls.data, fs, indent=2)

    @staticmethod
    def __generateaccountNo():
        alpha = random.choices(string.ascii_letters, k=4)
        digit = random.choices(string.digits, k=5)
        id = alpha + digit
        random.shuffle(id)
        return "".join(id)


    def createaccount(self):
        name = input("Tell your Name : - ")

        while True:
            age = input("Tell your Age : - ")
            if age.isdigit() and int(age) >= 18:
                age = int(age)
                break
            else:
                print("you are not eligible for create account (18 or above).")

        while True:
            phoneNo = input("Enter your phone number only 10 digit  : -")
            if phoneNo.isdigit() and len(phoneNo) == 10:
                phoneNo = int(phoneNo)
                break
            else:
                print(" Please enter a valid 10-digit phone number.")

        while True:
            email = input("enter your email and email letter above 6 ")
            if "@" in email and "." in email and len(email) > 6:
                break
            else:
                print(" Please enter a valid email address (example: abc@gmail.com).")

        while True:
            pin = input("Enter your 4-digit PIN: -")
            if pin.isdigit() and len(pin) == 4:
                pin = int(pin)
                break
            else:
                print("PIN must be exactly 4 digits.")

        info = {
            "name": name,
            "age": age,
            "phoneNo": phoneNo,
            "email": email,
            "pin": pin,
            "accountNo": Bank.__generateaccountNo(),
            "balance": 0
        }

        Bank.data.append(info)
        Bank.__update()

        print("\n Account Created Successfully!")

        for k in info:
            print(f"{k} : {info[k]}")
        print("note down your account number")


    def depositmoney(self):
        accnumber = input("enter your account number : - ")
        try:
            pin = int(input("please tell your pin aswell : - "))
        except ValueError:
            print("Invalid PIN format.")
            return

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such of data found")
        else:
            try:
                amount = int(input("how much you Want to deposit : -"))
            except ValueError:
                print("Invalid amount.")
                return

            if amount > 10000 or amount <= 0:
                print("sorry the amount is too much or invalid; deposit must be between 1 and 10000")
            else:
                userdata[0]['balance'] += amount
                Bank.__update()
                print("your amount is successfully deposited")

    def withdrawmoney(self):
        accnumber = input("enter your account number : - ")
        try:
            pin = int(input("please tell your pin aswell : -"))
        except ValueError:
            print("Invalid PIN format.")
            return

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such of data found")
        else:
            try:
                amount = int(input("How much you want to withdrawmoney : -"))
            except ValueError:
                print("Invalid amount.")
                return

            if userdata[0]['balance'] < amount:
                print("in your account not required balance for withdrawl")
            else:
                userdata[0]['balance'] -= amount
                Bank.__update()
                print("your amount is withdrawl successfully")


    def showdetails(self):
        accnumber = input("enter your account number : - ")
        try:
            pin = int(input("please tell your pin aswell : -"))
        except ValueError:
            print("Invalid PIN format.")
            return

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such of data Found")

        else:
            print("your information is .... ")
            for i in userdata[0]:
                print(f"{i} : {userdata[0][i]}")


    def updatadetails(self):
        accnumber = input("enter your account number : - ")
        try:
            pin = int(input("please tell your pin aswell : -"))
        except ValueError:
            print("Invalid PIN format.")
            return

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such of data Found")
        else:
            print("you can't change account No , age , and balance")

            print("Fill the details for change or leave it empty if no change")

            newinfo = {
                "name": input("enter your newName  for change or press enter for skip : - "),
                "email": input("enter your New  email for change press enter for skip : -"),
                "phoneNo": input("enter New phone number for change press enter for skip : -"),
                "pin": input("enter your New pin for change press enter for skip")
            }

            if newinfo["name"] == "":
                newinfo["name"] = userdata[0]['name']

            if newinfo['email'] == "":
                newinfo['email'] = userdata[0]['email']

            if newinfo['phoneNo'] == "":
                newinfo['phoneNo'] = userdata[0]['phoneNo']

            if newinfo["pin"] == "":
                newinfo["pin"] = userdata[0]['pin']

            newinfo['age'] = userdata[0]['age']
            newinfo['accountNo'] = userdata[0]['accountNo']
            newinfo['balance'] = userdata[0]['balance']

            if isinstance(newinfo['pin'], str):
                if newinfo['pin'].isdigit():
                    newinfo['pin'] = int(newinfo['pin'])
                else:
                    print("Invalid PIN provided. Keeping old PIN.")
                    newinfo['pin'] = userdata[0]['pin']

            if isinstance(newinfo['phoneNo'], str):
                if newinfo['phoneNo'].isdigit():
                    newinfo['phoneNo'] = int(newinfo['phoneNo'])
                else:
                    print("Invalid phone number. Keeping old phone number.")
                    newinfo['phoneNo'] = userdata[0]['phoneNo']

            # Apply changes
            for key in ['name', 'email', 'phoneNo', 'pin']:
                userdata[0][key] = newinfo[key]

            Bank.__update()

            print("your account details update successfully")

    def deleteaccount(self):

        accnumber = input("enter your account number : - ")
        try:
            pin = int(input("enter your pin number : - "))
        except ValueError:
            print("Invalid PIN format.")
            return

        userdata = [i for i in Bank.data if i['accountNo'] == accnumber and i['pin'] == pin]

        if not userdata:
            print("No such data Found")
        else:
            try:
                cheak = input("Press 'y' if you actually want to delete the account or press 'n' to skip: ").strip().lower()

                if cheak not in ["y", "n"]:
                    raise ValueError("Invalid input! Please enter only 'y' or 'n'.")

                if cheak == "n":
                    print(" Account deletion cancelled (bypassed).")

                else:
                    # Try finding the user index safely
                    try:
                        index = Bank.data.index(userdata[0])
                    except ValueError:
                        print(" Sorry! Account data not found in records.")
                        return

                    # Try deleting the account
                    try:
                        Bank.data.pop(index)
                        Bank.__update()
                        print(" Account deleted successfully!")
                    except Exception as e:
                        print(f" Error while deleting account: {e}")
            except ValueError as ve:
                print(f" {ve}")
            except Exception as err:
                print(f" Unexpected error occurred: {err}")

