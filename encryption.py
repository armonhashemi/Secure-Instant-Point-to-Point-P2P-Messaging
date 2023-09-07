from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_message(message, shared_key):
    iv = get_random_bytes(Blowfish.block_size)
    cipher = Blowfish.new(shared_key, Blowfish.MODE_CBC, iv)
    encrypted_message = iv + cipher.encrypt(pad(message.encode("utf-8"), Blowfish.block_size))
    return encrypted_message


def decrypt_message(encrypted_message, shared_key):
    iv = encrypted_message[:Blowfish.block_size]
    encrypted_message = encrypted_message[Blowfish.block_size:]
    cipher = Blowfish.new(shared_key, Blowfish.MODE_CBC, iv)
    try:
        decrypted_message = unpad(cipher.decrypt(encrypted_message), Blowfish.block_size).decode("utf-8")
    except ValueError:
        return ""
    return decrypted_message

