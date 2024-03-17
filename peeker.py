import sqlite3
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from hashlib import pbkdf2_hmac
import time
import getpass
import pyperclip
import sys

def greet_user():
    print("""
  _____            _             
 |  __ \          | |            
 | |__) |__   ___ | | _____ _ __ 
 |  ___/ _ \ / _ \| |/ / _ \ '__|
 | |  |  __/|  __/|   <  __/ |   
 |_|   \___| \___||_|\_\___|_|   
                                 
    """)

    print("\033[1;34;40mWelcome to PassKeep by EmToEn!\033[0m")
    print("\033[1;32;40mYour ultimate password manager.\033[0m\n")

# Call the function
greet_user()



master_password =  "Your Master Password"
salt = b"Your Password Salt"
key = pbkdf2_hmac('sha256', master_password.encode(), salt, 100000)

def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_ECB)
    enc_pwd = cipher.encrypt(password.rjust(32))
    return b64encode(enc_pwd).decode('utf-8') 

def decrypt_password(encoded_password, key):
    cipher = AES.new(key, AES.MODE_ECB)
    dec_pwd = cipher.decrypt(b64decode(encoded_password)).strip()
    return dec_pwd.decode('utf-8')

def createTable():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        encrypted_password BLOB NOT NULL
    )
    ''')
    time.sleep(1)
    print("\033[32m(+) New Table Created.\033[0m")
    conn.commit()
    conn.close()


def add_account(website, username, password,):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    enc_pass = encrypt_password(password, key)

    cursor.execute("INSERT INTO accounts (website, username, encrypted_password) VALUES (?, ?, ?)", 
                   (website, username, enc_pass))
    print("\033[32m(+) User Details Added.\033[0m")
    conn.commit()
    conn.close()


def retrieveData(website):
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password FROM accounts WHERE website=?", (website,))
    results = cursor.fetchall()
    print("\033[33mRetreivig Data..\033[0m")
    time.sleep(2)
    if results:
        for idx, result in enumerate(results, 1):
            dec_password = result[0]
            data = decrypt_password(dec_password,key)
            pyperclip.copy(data)
            print(f"\033[34mPassword {idx} for {website} is: ********** \033[0m")
            print("\033[1;32;40mCopied to Clipboard!\033[0m\n")
    else:
        print(f"\033[34mNo passwords found for {website}\033[0m")
    conn.close()


def deleteTable():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM accounts")
    print("\033[31m(x) Deleting Data..\033[0m")
    time.sleep(2)
    conn.commit()
    conn.close()

def viewDatabase():
    conn = sqlite3.connect('password_manager.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    rows = cursor.fetchall()
    # Fetch the column names (assuming the table isn't empty)
    columns = [desc[0] for desc in cursor.description]

    # Display the column names
    for col in columns:
        print(f'{col:<15}', end=' ')  # Assuming max column name length is 15
    print("\n" + "-"*len(columns)*16)  # Print a separator
    for row in rows:
        for field in row:
            print(f'{field:<15}', end=' ')  # Adjust 15 according to your needs
        print()
    conn.close()

def main():
    while True:
        # Greet the user and display options
        time.sleep(2)
        print("\n\033[1m\033[31mChoose an option:\033[0m")
        print("\033[1m1. Create a Table/Database")
        print("\033[1m2. Make a new entry into table\033[0m")
        print("\033[1m3. Retrieve password from table\033[0m")
        print("\033[1m4. To view entire database\033[0m")
        print("\033[1m5. Delete the database\033[0m")
        print("\033[1m6. Exit\033[0m")
        
        # Get user choice
        choice = input("\033[1mEnter your choice (1/2/3/4/5/6): \033[0m")
        
        if choice == "1":
            createTable()
        elif choice == "2":
            website = input("\033[1mEnter the website url: \033[0m")
            time.sleep(1)
            username = input("\033[1mEnter your username: \033[0m")
            time.sleep(1)
            password = getpass.getpass("\033[1mEnter your password: \033[0m")
            time.sleep(1)
            add_account(website, username, password)
        elif choice == "3":
            website = input("\033[1mEnter the website name: \033[0m")
            time.sleep(1)
            while True:
                ms = getpass.getpass("\033[1mEnter master password: \033[0m")
                if ms== master_password:
                    retrieveData(website)
                    break
                else:
                    print("\033[1m\033[31mIncorrect password. Please try again.\033[0m")
                    
        elif choice == "4":
            while True:
                ms = getpass.getpass("\033[1mEnter master password: \033[0m")
                if ms== master_password:
                    time.sleep(1)
                    viewDatabase()
                    break
                else:
                    print("\033[1m\033[31mIncorrect password. Please try again.\033[0m")
        elif choice == "5":
            while True:
                ms = getpass.getpass("\033[1mEnter master password: \033[0m")
                if ms== master_password:
                    deleteTable()
                    break
                else:
                    print("\033[1m\033[31mIncorrect password. Please try again.\033[0m")

        elif choice == "6":
            print("\033[1m\033[31mGoodbye!\033[0m")
            break
        else:
            print("\033[1m\033[31mInvalid choice. Please choose between 1 and 5 or select 6 to exit.\033[0m")

if __name__ == "__main__":
    main()

