import csv
import bcrypt
import re

CSV_FILE = 'regno.csv'

# Function to validate password strength
def validate_password(password):
    if (len(password) < 8 or
        not re.search(r"[A-Z]", password) or
        not re.search(r"[a-z]", password) or
        not re.search(r"\d", password) or
        not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
        return False
    return True

# Function to register a new user
def register():
    email = input("Enter your email: ")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print("Invalid email format.")
        return
    
    password = input("Enter your password: ")
    
    if not validate_password(password):
        print("Password must be at least 8 characters long, contain an uppercase letter, lowercase letter, a digit, and a special character.")
        return

    security_question = input("Enter a security question (e.g., Your pet's name): ")
    security_answer = input("Answer to the security question: ")

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, hashed_password, security_question, security_answer])

    print("Registration successful!")

# Function to log in a user
def login():
    attempts = 0
    while attempts < 5:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        with open(CSV_FILE, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                stored_email, stored_hashed_password, _, _ = row
                if email == stored_email and bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
                    print("Login successful!")
                    return True
        
        attempts += 1
        print(f"Invalid credentials. {5 - attempts} attempts remaining.")

    print("Too many failed attempts. Try again later.")
    return False

# Function to handle forgotten passwords
def forgot_password():
    email = input("Enter your registered email: ")

    with open(CSV_FILE, mode='r') as file:
        rows = list(csv.reader(file))
        for row in rows:
            stored_email, _, security_question, security_answer = row
            if email == stored_email:
                print(f"Security Question: {security_question}")
                answer = input("Your answer: ")
                if answer == security_answer:
                    new_password = input("Enter a new password: ")
                    if not validate_password(new_password):
                        print("Password does not meet security requirements.")
                        return

                    new_hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
                    row[1] = new_hashed_password

                    with open(CSV_FILE, mode='w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(rows)

                    print("Password reset successful!")
                    return
                else:
                    print("Incorrect security answer.")
                    return
    print("Email not found.")
