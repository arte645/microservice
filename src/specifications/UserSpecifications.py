from src.interfaces.ISpecification import *

class UserSpecification:
    @staticmethod
    def existing_email(email: str) -> ISpecification[dict]:
        return DirectSpecification(lambda User: User.email == email)

    @staticmethod
    def existing_username(username: str) -> ISpecification[dict]:
        return DirectSpecification(lambda User: User.username == username)