from rest_framework.throttling import SimpleRateThrottle

class RegisterThrottle(SimpleRateThrottle):

    scope = 'register'

    def get_cache_key(self, request, view):
        return self.get_ident(request)

class ForgotPasswordThrottle(SimpleRateThrottle):

    scope = 'forgot_password'

    def get_cache_key(self, request, view):
        email = request.user.email
        identity =  self.get_ident(request)

        return f"{email}:{identity}"