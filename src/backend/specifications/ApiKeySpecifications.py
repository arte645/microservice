from ..interfaces.ISpecification import *

class ApiKeySpecification:
    @staticmethod
    def api_is(description: str) -> ISpecification:
        return DirectSpecification(lambda ApiKey: ApiKey.description == description)
    
    @staticmethod
    def key_is(key: str) -> ISpecification:
        return DirectSpecification(lambda ApiKey: ApiKey.key == key)