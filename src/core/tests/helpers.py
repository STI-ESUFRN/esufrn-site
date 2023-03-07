from typing import List

from django.contrib.auth.models import Group, User
from model_bakery import baker


def sample_user(**kwargs) -> User | List[User]:
    def configure_user(user: User, groups: list):
        user.set_password(user.password)
        if groups:
            for group in groups:
                user.groups.add(group)

        user.save()

    groups = kwargs.pop("groups", None)
    result = baker.make(User, **kwargs)
    if isinstance(result, list):
        for user in result:
            configure_user(user, groups)

    else:
        configure_user(result, groups)

    return result


def sample_group(**kwargs) -> Group | List[Group]:
    return baker.make(Group, **kwargs)
