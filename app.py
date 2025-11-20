import streamlit as st
from bank import Bank

st.set_page_config(page_title="Simple Bank App", layout="centered")

st.title("🏦 Simple Bank Management")

bank = Bank()

menu = st.sidebar.selectbox("Choose an action", ["Create Account", "Deposit", "Withdraw", "Show Details", "Update Details", "Delete Account"]) 

if menu == "Create Account":
    st.header("Create Account")
    name = st.text_input("Full name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    phone = st.text_input("Phone (10 digits)")
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create"):
        # Basic validations similar to CLI
        if age < 18:
            st.error("You must be at least 18 years old.")
        elif not (phone.isdigit() and len(phone) == 10):
            st.error("Enter a valid 10-digit phone number.")
        elif not ("@" in email and "." in email and len(email) > 6):
            st.error("Enter a valid email address.")
        elif not (pin.isdigit() and len(pin) == 4):
            st.error("PIN must be exactly 4 digits.")
        else:
            # create account dict and append
            info = {
                "name": name,
                "age": int(age),
                "phoneNo": int(phone),
                "email": email,
                "pin": int(pin),
                "accountNo": Bank._Bank__generateaccountNo(),
                "balance": 0
            }
            Bank.data.append(info)
            Bank._Bank__update()
            st.success("Account created successfully!")
            st.write(info)

elif menu == "Deposit":
    st.header("Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        try:
            pin_int = int(pin)
        except:
            st.error("Invalid PIN format.")
        else:
            userdata = [i for i in Bank.data if i['accountNo'] == acc and i['pin'] == pin_int]
            if not userdata:
                st.error("Account not found or wrong PIN.")
            else:
                if amount > 10000:
                    st.error("Deposit limit is 10000")
                else:
                    userdata[0]['balance'] += amount
                    Bank._Bank__update()
                    st.success("Amount deposited successfully!")

elif menu == "Withdraw":
    st.header("Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        try:
            pin_int = int(pin)
        except:
            st.error("Invalid PIN format.")
        else:
            userdata = [i for i in Bank.data if i['accountNo'] == acc and i['pin'] == pin_int]
            if not userdata:
                st.error("Account not found or wrong PIN.")
            else:
                if userdata[0]['balance'] < amount:
                    st.error("Insufficient balance.")
                else:
                    userdata[0]['balance'] -= amount
                    Bank._Bank__update()
                    st.success("Withdrawal successful!")

elif menu == "Show Details":
    st.header("Show Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show"):
        try:
            pin_int = int(pin)
        except:
            st.error("Invalid PIN format.")
        else:
            userdata = [i for i in Bank.data if i['accountNo'] == acc and i['pin'] == pin_int]
            if not userdata:
                st.error("Account not found or wrong PIN.")
            else:
                st.json(userdata[0])

elif menu == "Update Details":
    st.header("Update Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Load"):
        try:
            pin_int = int(pin)
        except:
            st.error("Invalid PIN format.")
        else:
            userdata = [i for i in Bank.data if i['accountNo'] == acc and i['pin'] == pin_int]
            if not userdata:
                st.error("Account not found or wrong PIN.")
            else:
                user = userdata[0]
                new_name = st.text_input("Name", value=user['name'])
                new_email = st.text_input("Email", value=user['email'])
                new_phone = st.text_input("Phone", value=str(user['phoneNo']))
                new_pin = st.text_input("PIN", value=str(user['pin']), type="password")

                if st.button("Update"):
                    if not (new_pin.isdigit() and len(new_pin) == 4):
                        st.error("PIN must be 4 digits.")
                    elif not (new_phone.isdigit() and len(new_phone) == 10):
                        st.error("Phone must be 10 digits.")
                    else:
                        user['name'] = new_name
                        user['email'] = new_email
                        user['phoneNo'] = int(new_phone)
                        user['pin'] = int(new_pin)
                        Bank._Bank__update()
                        st.success("Details updated!")

elif menu == "Delete Account":
    st.header("Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        try:
            pin_int = int(pin)
        except:
            st.error("Invalid PIN format.")
        else:
            userdata = [i for i in Bank.data if i['accountNo'] == acc and i['pin'] == pin_int]
            if not userdata:
                st.error("Account not found or wrong PIN.")
            else:
                if st.confirm("Are you sure you want to delete this account?"):
                    try:
                        Bank.data.remove(userdata[0])
                        Bank._Bank__update()
                        st.success("Account deleted")
                    except Exception as e:
                        st.error(f"Error deleting account: {e}")
