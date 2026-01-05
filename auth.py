import json
import os
import hashlib
import time
from typing import Optional

from user import User

class AuthSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user: Optional[User] = None

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        if username in users:
            return False

        user = User(username)
        user.password_hash = self.hash_password(password)

        users[username] = user.to_dict()

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

        self.current_user = user
        return True

    def login(self, username: str, password: str) -> bool:
        if not os.path.exists(self.users_file):
            return False

        with open(self.users_file, 'r') as f:
            users = json.load(f)

        if username not in users:
            return False

        if users[username]["password_hash"] != self.hash_password(password):
            return False

        self.current_user = User.from_dict(users[username])
        return True

    def save_user(self):
        if not self.current_user:
            return

        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                users = json.load(f)
        else:
            users = {}

        users[self.current_user.username] = self.current_user.to_dict()

        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)

    def save_game(self, save_name: str = "quicksave"):
        if not self.current_user:
            return False

        save_data = {
            "user": self.current_user.to_dict(),
            "timestamp": time.time()
        }

        save_dir = "saves"
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        save_file = os.path.join(save_dir, f"{save_name}.json")

        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)

        print(f"Игра сохранена: {save_name}")
        return True

    def load_game(self, save_name: str = "quicksave") -> bool:
        save_file = os.path.join("saves", f"{save_name}.json")

        if not os.path.exists(save_file):
            return False

        with open(save_file, 'r') as f:
            save_data = json.load(f)

        self.current_user = User.from_dict(save_data["user"])
        print(f"Загружено сохранение: {save_name}")
        return True