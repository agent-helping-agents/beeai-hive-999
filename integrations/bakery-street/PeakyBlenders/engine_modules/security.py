import hashlib
import time
import json
from datetime import datetime

class SecurityManager:
    """
    Handles encryption, versioning, and audit trail security
    """
    def __init__(self):
        self.session_keys = {}
        self.audit_trail = []
        self.version_history = {}
        self.access_controls = {
            'read': ['analyst', 'auditor', 'admin'],
            'write': ['admin'],
            'audit': ['auditor', 'admin']
        }

    def generate_session_key(self, user_role):
        """Generate encrypted session key"""
        timestamp = str(time.time())
        raw_key = f"{user_role}_{timestamp}_{hash(user_role + timestamp)}"
        session_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16]

        self.session_keys[session_key] = {
            'role': user_role,
            'created': timestamp,
            'expires': str(time.time() + 3600),  # 1 hour expiration
            'active': True
        }

        return session_key

    def encrypt_output(self, data, session_key):
        """Encrypt output data (simplified encryption)"""
        if session_key not in self.session_keys:
            raise ValueError("Invalid session key")

        # Simple XOR encryption for demonstration
        data_str = json.dumps(data, default=str)
        key_bytes = session_key.encode()
        encrypted = []

        for i, char in enumerate(data_str):
            key_char = key_bytes[i % len(key_bytes)]
            encrypted_char = ord(char) ^ key_char
            encrypted.append(encrypted_char)

        encrypted_data = {
            'encrypted_payload': encrypted,
            'session_key': session_key,
            'timestamp': datetime.now().isoformat(),
            'version': self.get_version_id(data)
        }

        return encrypted_data

    def decrypt_output(self, encrypted_data):
        """Decrypt output data"""
        session_key = encrypted_data['session_key']

        if session_key not in self.session_keys:
            raise ValueError("Invalid session key")

        if not self.session_keys[session_key]['active']:
            raise ValueError("Session key expired")

        # Simple XOR decryption
        encrypted_payload = encrypted_data['encrypted_payload']
        key_bytes = session_key.encode()
        decrypted_chars = []

        for i, encrypted_char in enumerate(encrypted_payload):
            key_char = key_bytes[i % len(key_bytes)]
            decrypted_char = encrypted_char ^ key_char
            decrypted_chars.append(chr(decrypted_char))

        decrypted_str = ''.join(decrypted_chars)
        return json.loads(decrypted_str)

    def log_audit_event(self, event_type, user_role, data_accessed, session_key):
        """Log audit event"""
        audit_event = {
            'event_id': len(self.audit_trail),
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'user_role': user_role,
            'session_key': session_key,
            'data_hash': hashlib.md5(str(data_accessed).encode()).hexdigest(),
            'access_granted': self.check_access_permission(user_role, event_type)
        }

        self.audit_trail.append(audit_event)
        return audit_event

    def check_access_permission(self, user_role, operation):
        """Check if user role has permission for operation"""
        return user_role in self.access_controls.get(operation, [])

    def get_version_id(self, data):
        """Generate version ID for data"""
        data_hash = hashlib.md5(str(data).encode()).hexdigest()
        version_id = f"v{len(self.version_history)}_{data_hash[:8]}"

        self.version_history[version_id] = {
            'timestamp': datetime.now().isoformat(),
            'data_hash': data_hash,
            'size': len(str(data))
        }

        return version_id