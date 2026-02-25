# Security Policy

## Supported Versions

We currently support and provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Agent-Adversary, please **do not open a public issue**. Instead, follow the process below:

1. **Email us**: Send a detailed report to `security@agent-adversary.com`.
2. **Details**: Include a proof-of-concept, the impact of the vulnerability, and the affected versions.
3. **Response**: We will acknowledge your report within 48 hours and provide a timeline for a fix.

We follow a coordinated disclosure policy. We ask you to keep the vulnerability private until we have released a fix.

## Enterprise Hardening

Agent-Adversary includes built-in security features for enterprise deployments:
- **HMAC Payload Signing**: Prevents tampering with tasks sent to worker nodes.
- **Audit Logs**: Maintains an immutable trail of all actions.
- **RBAC**: API key-based access control for administrative endpoints.
