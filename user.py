from typing import Dict, List

class User:
    def __init__(self, username: str):
        self.username = username
        self.password_hash = ""
        self.artifacts: List[str] = []
        self.achievements: List[str] = []
        self.hp = 100
        self.max_hp = 100
        self.location = "start"
        self.story_progress = 0
        self.father_respect = 0
        self.drunk_level = 0
        self.quests_completed = {
            "parents": False,
            "friends": False,
            "father_jokes": False,
            "vitaly_battle": False,
            "rps_game": False,
            "baba_zina": False
        }

    def to_dict(self) -> Dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "artifacts": self.artifacts,
            "achievements": self.achievements,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "location": self.location,
            "story_progress": self.story_progress,
            "father_respect": self.father_respect,
            "drunk_level": self.drunk_level,
            "quests_completed": self.quests_completed
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        user = cls(data["username"])
        user.password_hash = data["password_hash"]
        user.artifacts = data["artifacts"]
        user.achievements = data["achievements"]
        user.hp = data["hp"]
        user.max_hp = data["max_hp"]
        user.location = data["location"]
        user.story_progress = data["story_progress"]
        user.father_respect = data["father_respect"]
        user.drunk_level = data["drunk_level"]
        user.quests_completed = data.get("quests_completed", {
            "parents": False, "friends": False, "father_jokes": False,
            "vitaly_battle": False, "rps_game": False, "baba_zina": False
        })
        return user

    def check_all_quests_completed(self) -> bool:
        return all(self.quests_completed.values())