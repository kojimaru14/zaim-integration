from django.http import HttpResponse

import base64


def _http401():
    response = HttpResponse("Unauthorized", status=401)
    response['WWW-Authenticate'] = 'Basic realm="basic auth username/password inalid"'
    return response


def _basic_auth(request):
    if 'HTTP_AUTHORIZATION' not in request.META:
        return False, None
    (auth_scheme, base64_username_pass) = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
    if auth_scheme.lower() != 'basic':
        return False, None
    username_pass = base64.decodebytes(base64_username_pass.strip().encode('ascii')).decode('ascii')
    (username, password) = username_pass.split(':', 1)
    return True, (username, password)


def basic_auth(func):
    def wrapper(request, *args, **kwargs):
        success, tuple = _basic_auth(request)
        if not success:
            return _http401()
        else:
            username, password = tuple
            return func(request, username, password, *args, **kwargs)

    return wrapper