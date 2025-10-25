"""
Factory for User model test data generation.
"""

from django.contrib.auth.models import User

import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """
    Factory for creating User instances with fake data.

    Attributes:
        username: Unique username generated from faker.
        email: Unique email generated from faker.
        password: Default test password (hashed).
        first_name: First name generated from faker.
        last_name: Last name generated from faker.
        is_active: Active status (default True).
        is_staff: Staff status (default False).
        is_superuser: Superuser status (default False).

    Examples:
        >>> user = UserFactory()
        >>> user.username
        'john_doe_42'
        >>> user.email
        'john.doe@example.com'

        >>> admin = UserFactory(is_staff=True, is_superuser=True)
        >>> admin.is_staff
        True

        >>> users = UserFactory.create_batch(5)
        >>> len(users)
        5
    """

    class Meta:
        """Factory configuration."""

        model = User
        django_get_or_create = ("username",)

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def password(
        self, create: bool, extracted: str | None, **kwargs: dict[str, str]
    ) -> None:
        """
        Set password after instance generation.

        Args:
            create: Whether the instance was created or just built.
            extracted: Password value passed to the factory.
            **kwargs: Additional keyword arguments.
        """
        if not create:
            return

        if extracted:
            self.set_password(extracted)
        else:
            self.set_password("testpass123")  # nosec B106
