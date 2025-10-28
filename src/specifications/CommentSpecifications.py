from src.interfaces.ISpecification import *

class CommentSpecification:
    @staticmethod
    def user_is_author(user_id: str) -> ISpecification:
        return DirectSpecification(lambda Comment: Comment.user_id == user_id)
    
    def comment_is_deleted() ->  ISpecification:
        return DirectSpecification(lambda Comment: Comment.is_deleted)
    
    def comment_id_is(comment_id) -> ISpecification:
        return DirectSpecification(lambda Comment: Comment.comment_id == comment_id)
