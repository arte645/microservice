from ..interfaces.ISpecification import *

class SubscriptionSpecification:
    @staticmethod
    def subscriber_user_id_is(subscriber_user_id: str) -> ISpecification:
        return DirectSpecification(lambda Subscription: Subscription.subscriber_user_id == subscriber_user_id)
    
    @staticmethod
    def target_user_id_is(target_user_id: str) -> ISpecification:
        return DirectSpecification(lambda Subscription: Subscription.target_user_id== target_user_id)
