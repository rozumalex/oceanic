from tortoise import Tortoise


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url="postgres://alex:password@localhost:5432/oceanic",
        modules={'models': ['app.models']}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    init()

