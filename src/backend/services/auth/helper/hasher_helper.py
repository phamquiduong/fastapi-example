from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher():
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> str:
        """
        The function verifies if a plain password matches a hashed password using a password context.

        Args:
          plain_password (str): A string representing the plain text password that needs to be verified.
          hashed_password (str): The hashed password from database, using Bcrypt Encoding.

        Returns:
          (bool): True if the password matches
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        The function takes a password string as input and returns its hashed value using a password
        context object.

        Args:
          password (str): A string representing the password that needs to be hashed.

        Returns:
          (str) The returned value is a string representing the Bcrypt hashed password.
        """
        return pwd_context.hash(password)
