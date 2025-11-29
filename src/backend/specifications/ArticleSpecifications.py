from ..interfaces.ISpecification import *

class ArticleSpecification:
    @staticmethod
    def created_by_user(user_id: str) -> ISpecification:
        return DirectSpecification(lambda Article: Article.user_id == user_id)

    @staticmethod
    def article_id_is(article_id: str) -> ISpecification:
        return DirectSpecification(lambda Article: Article.article_id == article_id)
    
    @staticmethod
    def not_deleted() -> ISpecification:
        return DirectSpecification(lambda Article: Article.is_deleted == False)
