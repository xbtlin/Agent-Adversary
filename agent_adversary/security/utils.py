import secrets
import string
import hmac
import hashlib
from typing import Tuple

class SecurityUtils:
    """
    Advanced security utilities for the Agent-Adversary framework.
    """
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """Generates a cryptographically secure random token."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    def verify_signature(payload: str, signature: str, secret: str) -> bool:
        """Verifies a HMAC-SHA256 signature for secure API communication."""
        expected = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(expected, signature)

    @staticmethod
    def sign_payload(payload: str, secret: str) -> str:
        """Signs a payload using HMAC-SHA256."""
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
