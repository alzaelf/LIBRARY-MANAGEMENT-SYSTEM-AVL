import csv
import os
from user import User

FILENAME = "users.csv"

def load_users():
    users = []
    if not os.path.exists(FILENAME):
        return users
    with open(FILENAME, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            users.append(User(
                row["username"],
                row["password"],
                row["role"]
            ))
    return users

def save_users(users):
    with open(FILENAME, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["username", "password", "role"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for u in users:
            writer.writerow({
                "username": u.username,
                "password": u.password,
                "role": u.role
            })

def register_user(username, password, role="pengunjung"):
    users = load_users()
    if any(u.username == username for u in users):
        return False
    users.append(User(username, password, role))
    save_users(users)
    return True

def authenticate(username, password):
    users = load_users()
    for u in users:
        if u.username == username and u.password == password:
            return u
    return None
