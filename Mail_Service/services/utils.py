from cryptography.fernet import Fernet, InvalidToken
import base64
import os
from django.conf import settings
from django.http import JsonResponse

fernet = Fernet(settings.FERNET_KEY)


def encrypt_pk(pk):
    """
    Шифрует первичный ключ.
    """
    pk_str = str(pk).encode()
    encrypted_pk = fernet.encrypt(pk_str)
    return base64.urlsafe_b64encode(encrypted_pk).decode()


def decrypt_pk(encrypted_pk):
    """
    Дешифрует первичный ключ.
    """

    if isinstance(encrypted_pk, int):
        raise TypeError("Argument should be a base64-encoded string")

    try:
        encrypted_pk_bytes = base64.urlsafe_b64decode(encrypted_pk)
        decrypted_pk = fernet.decrypt(encrypted_pk_bytes)
        return int(decrypted_pk.decode())
    except (base64.binascii.Error, ValueError) as e:
        # Ошибка при декодировании из base64
        raise ValueError("Invalid base64-encoded string") from e
    except InvalidToken as e:
        # Ошибка при дешифровании с использованием Fernet
        raise ValueError("Invalid encryption token") from e