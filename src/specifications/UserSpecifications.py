from src.interfaces.ISpecification import *

class UserSpecification:
    @staticmethod
    def existing_email(email: str) -> ISpecification:
        return DirectSpecification(lambda User: User.email == email)

    @staticmethod
    def existing_username(username: str) -> ISpecification:
        return DirectSpecification(lambda User: User.username == username)
    
    @staticmethod
    def existing_password(password: str) -> ISpecification:
        return DirectSpecification(lambda User: User.password == password)

    @staticmethod
    def is_deleted() -> ISpecification:
        return DirectSpecification(lambda User: User.is_deleted)
    
    @staticmethod
    def id_is(user_id: str) -> ISpecification:
        return DirectSpecification(lambda User: User.user_id == user_id)
