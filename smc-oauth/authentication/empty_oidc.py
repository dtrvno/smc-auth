from flask_oidc import OpenIDConnect
from functools import wraps
class EmptyOidc:
    def __init__(self):
        pass

    def accept_token(self,require_token=True, scopes_required='openid'):
        def wrapper(view_func):
            @wraps(view_func)
            def decorated(*args, **kwargs):
                return view_func(*args, **kwargs)

            return decorated
        return wrapper
