import string
import unittest


class EncryptedField:
    def __init__(self, encryption_type='caesar', key=None):
        self.encryption_type = encryption_type
        self.key = key
        self.storage_name = None

    def __set_name__(self, owner, name):
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None: return self
        value = getattr(obj, self.storage_name, None)
        if value is None: return None
        return self._decrypt(value, obj)

    def __set__(self, obj, value):
        if value is None:
            setattr(obj, self.storage_name, None)
            return
        encrypted_value = self._encrypt(str(value), obj)
        setattr(obj, self.storage_name, encrypted_value)

    def _encrypt(self, text, obj):
        if self.encryption_type == 'caesar':
            return CaesarCipher.encrypt(text, self._get_key(obj))
        return AtbashCipher.encrypt(text)

    def _decrypt(self, encrypted_text, obj):
        if self.encryption_type == 'caesar':
            return CaesarCipher.decrypt(encrypted_text, self._get_key(obj))
        return AtbashCipher.decrypt(encrypted_text)

    def _get_key(self, obj):
        return self.key or getattr(obj, 'cipher_key', 3)


class CaesarCipher:
    def encrypt(text, shift=3):
        result = []
        for char in text:
            if char.isupper():
                result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
            elif char.islower():
                result.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
            elif char.isdigit():
                result.append(chr((ord(char) - ord('0') + shift) % 10 + ord('0')))
            else:
                result.append(char)
        return ''.join(result)

    def decrypt(encrypted_text, shift=3):
        return CaesarCipher.encrypt(encrypted_text, -shift)

    def brute_force(encrypted_text):
        return {shift: CaesarCipher.decrypt(encrypted_text, shift) for shift in range(26)}


class AtbashCipher:
    RU_UPPER = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    RU_LOWER = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    EN_UPPER = string.ascii_uppercase
    EN_LOWER = string.ascii_lowercase
    DIGITS = string.digits

    ATBASH_MAP = {}

    def init_mapping():
        if AtbashCipher.ATBASH_MAP: return
        for alphabet in [AtbashCipher.EN_UPPER, AtbashCipher.EN_LOWER, AtbashCipher.RU_UPPER, AtbashCipher.RU_LOWER,
                         AtbashCipher.DIGITS]:
            for i in range(len(alphabet)):
                AtbashCipher.ATBASH_MAP[alphabet[i]] = alphabet[-i - 1]

    def encrypt(text):
        AtbashCipher.init_mapping()
        return ''.join(AtbashCipher.ATBASH_MAP.get(char, char) for char in text)

    def decrypt(encrypted_text):
        return AtbashCipher.encrypt(encrypted_text)


class SecretMessage:
    caesar_message = EncryptedField('caesar', key=3)
    caesar_custom = EncryptedField('caesar', key=7)
    atbash_message = EncryptedField('atbash')

    def __init__(self, cipher_key=3):
        self.cipher_key = cipher_key


class TestCiphers(unittest.TestCase):
    def setUp(self):
        self.secret = SecretMessage(5)

    def test_caesar(self):
        self.secret.caesar_message = "Hello123"
        self.assertEqual("Hello123", self.secret.caesar_message)

    def test_atbash(self):
        self.secret.atbash_message = "ABC"
        self.assertEqual("ABC", self.secret.atbash_message)

    def test_russian(self):
        self.assertEqual("ПриветМир", AtbashCipher.decrypt(AtbashCipher.encrypt("ПриветМир")))


if __name__ == "__main__":
    unittest.main(argv=[''], exit=False, verbosity=2)
