from typing import Optional

from blacksheep.messages import Request
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity


class ExampleAuthHandler(AuthenticationHandler):
    def __init__(self):
        pass

    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b"Authorization")
        if header_value:
            # TODO: parse and validate the value of the authorization
            # header to get an actual user's identity
            context.identity = Identity({"name": "Jan Kowalski"}, "MOCK")
        else:
            context.identity = None
        return context.identity
