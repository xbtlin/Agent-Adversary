import pytest
from agent_adversary.security.utils import SecurityUtils

def test_secure_token_generation():
    token1 = SecurityUtils.generate_secure_token(32)
    token2 = SecurityUtils.generate_secure_token(32)
    
    assert len(token1) == 32
    assert token1 != token2
    # Check alphabet (approximate)
    assert any(c.isdigit() for c in token1)
    assert any(c.isalpha() for c in token1)

def test_payload_signing_and_verification():
    secret = "super-secret-key"
    payload = "important-data-payload"
    
    signature = SecurityUtils.sign_payload(payload, secret)
    assert SecurityUtils.verify_signature(payload, signature, secret) is True
    assert SecurityUtils.verify_signature(payload, "wrong-signature", secret) is False
    assert SecurityUtils.verify_signature("tampered-data", signature, secret) is False
