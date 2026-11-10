from rest_framework.throttling import SimpleRateThrottle
from rest_framework.throttling import AnonRateThrottle

import hashlib


class RegisterThrottle(SimpleRateThrottle):
    scope = 'register'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


class ForgotPasswordEmailThrottle(SimpleRateThrottle):
    scope = "forgot_password_email"

    def get_cache_key(self, request, view):
        email = request.data.get("email", "").strip().lower()
        ident = hashlib.sha256(email.encode()).hexdigest()

        if not email:
            return None

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }


class ForgotPasswordIPThrottle(AnonRateThrottle):
    scope = "forgot_password_ip"
