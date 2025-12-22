from yadura import CaesarCipher, AtbashCipher

# Цезарь
print(CaesarCipher.encrypt("Hello", 5))
print(CaesarCipher.decrypt("Mjqqt", 5))

# Атбаш
print(AtbashCipher.encrypt("ABC123"))
print(AtbashCipher.decrypt("ZYX876"))

# Подбор ключа Цезаря
print(CaesarCipher.brute_force("Khoor"))