from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.exceptions import InvalidSignature


class Key:
    def __init__(self, public_key: str = None, private_key: str = None):
        """

        :param public_key: base64 encoded
        :param private_key: base64 encoded
        """
        self.__public_key = None
        self.__private_key = None

        if private_key is not None:
            self.__private_key = serialization.load_der_private_key(
                b64decode(private_key), None, default_backend()
            )
            self.__public_key = self.__private_key.public_key()

        if public_key is not None:
            self.__public_key = serialization.load_der_public_key(
                b64decode(public_key), default_backend()
            )

        if public_key is None and private_key is None:
            self.__private_key = ec.generate_private_key(
                ec.SECP256R1(), default_backend()
            )
            self.__public_key = self.__private_key.public_key()

    @property
    def can_sign(self) -> bool:
        return self.__private_key is not None

    @property
    def public_key(self) -> str:
        b = self.__public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return b64encode(b).decode('ascii')

    @property
    def private_key(self):
        if self.__private_key is not None:
            b = self.__private_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
            return b64encode(b).decode('ascii')
        return None

    def sign(self, data: bytes):
        if self.can_sign:
            signature = self.__private_key.sign(
                data,
                ec.ECDSA(SHA256())
            )
            return signature
        return None

    def verify(self, signature: str, data: bytes):
        try:
            self.__public_key.verify(
                b64decode(signature),
                data,
                ec.ECDSA(SHA256())
            )
            return True
        except InvalidSignature:
            return False
