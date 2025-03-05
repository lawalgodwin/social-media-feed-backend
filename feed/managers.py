from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """ Custom user manager """

    def _create_user(
            self, email,
            password,
            first_name,
            last_name,
            **extra_fields):
        """ Create a user """
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email,
            password,
            first_name, last_name,
            **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email, password,
            first_name, last_name,
            **extra_fields)

    def create_superuser(
            self, email,
            password, first_name,
            last_name,
            **extra_fields):
        """ Create a super user """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(
            email, password,
            first_name, last_name,
            **extra_fields)
