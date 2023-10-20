from aiogram import Router


def get_user_router() -> Router:
    from . import start_cmd

    router = Router()
    router.include_router(start_cmd.router)
    return router
