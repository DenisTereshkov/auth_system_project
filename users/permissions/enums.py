from enum import Enum

class RoleType(str, Enum):
    ADMIN = "admin"
    USER = "user"
    
    @classmethod
    def choices(cls):
        return [(item.value, item.value) for item in cls]