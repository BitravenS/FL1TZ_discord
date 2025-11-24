from string import ascii_lowercase, ascii_uppercase
from typing import Optional
from factordb.factordb import FactorDB
import hashlib
from discord import Interaction, app_commands


class ClassicCiphers:
    """Implementation of some basic classic ciphers."""

    @staticmethod
    def caesar(message: str, key: int) -> str:
        return "".join(
            (
                chr((ord(i) - (97, 65)[i.isupper()] + key) % 26 + (97, 65)[i.isupper()])
                if i.isalpha()
                else i
            )
            for i in message
        )

    @staticmethod
    def rot13(message: str) -> str:
        return ClassicCiphers.caesar(message, 13)

    @staticmethod
    def atbash(message: str) -> str:
        return message.translate(
            {
                **str.maketrans(ascii_lowercase, ascii_lowercase[::-1]),
                **str.maketrans(ascii_uppercase, ascii_uppercase[::-1]),
            }
        )
    
    @staticmethod
    def factor(number: int) -> str:
        """Factor a number using FactorDB.

        Args:
            number: The number to factor.

        Returns:
            A string representation of the factors.
        """
        f = FactorDB(number)
        f.connect()
        factors = f.get_factor_list()
        return " × ".join(str(factor) for factor in factors)


class Crypto(app_commands.Group):
    """Encryption/Decryption using classic ciphers."""
    hashing = app_commands.Group(name="hashing", description="Hash a message using various algorithms.")
    rsa = app_commands.Group(name="rsa", description="Tools for dealing with RSA cryptography.")


    @app_commands.command()
    async def caesar(
        self, interaction: Interaction, message: str, key: Optional[int]
    ) -> None:
        """Caesar cipher

        Args:
            interaction: The interaction that triggered this command.
            message: The message encrypt/decrypt.
            key: The key to be used for encryption/decryption (default: brute force).
        """
        if key is None:
            result = "\n".join(
                f"{key:>2} | {ClassicCiphers.caesar(message, key)}"
                for key in range(1, 26)
            )
        else:
            result = ClassicCiphers.caesar(message, int(key))

        await interaction.response.send_message(f"```\n{result}\n```")

    @app_commands.command()
    async def rot13(self, interaction: Interaction, message: str) -> None:
        """Rot13 cipher

        Args:
            interaction: The interaction that triggered this command.
            message: The message encrypt/decrypt.
        """
        await interaction.response.send_message(
            f"```\n{ClassicCiphers.rot13(message)}\n```"
        )

    @app_commands.command()
    async def atbash(self, interaction: Interaction, message: str) -> None:
        """Atbash cipher

        Args:
            interaction: The interaction that triggered this command.
            message: The message encrypt/decrypt.
        """
        await interaction.response.send_message(
            f"```\n{ClassicCiphers.atbash(message)}\n```"
        )

    @app_commands.command()
    async def factor(self, interaction: Interaction, number: int) -> None:
        """Factor a number using FactorDB.

        Args:
            interaction: The interaction that triggered this command.
            number: The number to factor.
        """
        factors = ClassicCiphers.factor(number)
        await interaction.response.send_message(f"```\n{number} = {factors}\n```")

    @hashing.command(name="sha256")
    async def sha256(self, interaction: Interaction, message: str) -> None:
        """Compute the SHA-256 hash of a message.

        Args:
            interaction: The interaction that triggered this command.
            message: The message to hash.
        """
        hash_object = hashlib.sha256(message.encode())
        hash_hex = hash_object.hexdigest()
        await interaction.response.send_message(f"```\nSHA-256: {hash_hex}\n```")
    
    @hashing.command(name="sha1")
    async def sha1(self, interaction: Interaction, message: str) -> None:
        """Compute the SHA-1 hash of a message.

        Args:
            interaction: The interaction that triggered this command.
            message: The message to hash.
        """
        hash_object = hashlib.sha1(message.encode())
        hash_hex = hash_object.hexdigest()
        await interaction.response.send_message(f"```\nSHA-1: {hash_hex}\n```")

    @hashing.command(name="md5")
    async def md5(self, interaction: Interaction, message: str) -> None:
        """Compute the MD5 hash of a message.

        Args:
            interaction: The interaction that triggered this command.
            message: The message to hash.
        """
        hash_object = hashlib.md5(message.encode())
        hash_hex = hash_object.hexdigest()
        await interaction.response.send_message(f"```\nMD5: {hash_hex}\n```")

    @rsa.command(name="decrypt")
    async def rsa_decrypt(
        self, interaction: Interaction, ciphertext: int, n: int, e: int, p: int, q: int
    ) -> None:
        """Decrypt an RSA ciphertext given the private key components.

        Args:
            interaction: The interaction that triggered this command.
            ciphertext: The RSA ciphertext to decrypt.
            n: The modulus.
            e: The public exponent.
            p: The first prime factor of n.
            q: The second prime factor of n.
        """
        try:
            phi = (p - 1) * (q - 1)
            d = pow(e, -1, phi)
            plaintext_int = pow(ciphertext, d, n)
            plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'big')
            plaintext = plaintext_bytes.decode()
        except UnicodeDecodeError:
            plaintext = str(plaintext_int)
        except Exception as ex:
            await interaction.response.send_message(f"Error during decryption: {ex}")
            return
        
        await interaction.response.send_message(f"```\nDecrypted message: {plaintext}\n```")