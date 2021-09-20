from configuration.common import Configuration
from rodi import Container

from blacksheep.server import Application
from core.events import ServicesRegistrationContext
from core.db import register_tortoise
from core.auth import ExampleAuthHandler

from . import controllers  # NoQA
from .auth import configure_authentication
from .errors import configure_error_handlers
from .templating import configure_templating
from .docs import docs


async def before_start(application: Application) -> None:
    application.services.add_instance(application)
    application.services.add_alias("app", Application)


def configure_application(
    services: Container,
    context: ServicesRegistrationContext,
    configuration: Configuration,
) -> Application:
    app = Application(
        services=services,
        show_error_details=configuration.show_error_details,
        debug=configuration.debug,
    )

    app.on_start += before_start

    app.on_start += context.initialize
    app.on_stop += context.dispose

    configure_error_handlers(app)
    configure_authentication(app)
    configure_templating(app, configuration)
    register_tortoise(app, db_url=configuration.storage_connection_string, generate_schemas=True, modules={"models": ["app.models"]})

    app.use_authentication().add(ExampleAuthHandler())

    from blacksheep.server.authorization import Policy, auth
    from guardpost.common import AuthenticatedRequirement
    Authenticated = "authenticated"
    app.use_authorization().add(Policy(Authenticated, AuthenticatedRequirement()))
    app.serve_files("app/static")

    docs.bind_app(app)

    ######
    from blacksheep.server.responses import json
    from guardpost.authentication import User
    from typing import Optional
    from blacksheep import Request
    from guardpost.authentication import Identity
    from blacksheep.server.responses import ok
    get = app.router.get

    @get("/")
    async def for_anybody(user: Optional[User]):
        if user is None:
            return json({"anonymous": True})

        return json(user.claims)

    @auth(Authenticated)
    @get("/account")
    async def only_for_authenticated_users():
        return ok("example")

    return app
