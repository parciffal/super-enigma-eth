from aiogram import Router


def get_user_router() -> Router:
    from . import rug_check_handler, start_cmd

    router = Router()
    router.include_router(start_cmd.router)
    router.include_router(rug_check_handler.router)
    return router
