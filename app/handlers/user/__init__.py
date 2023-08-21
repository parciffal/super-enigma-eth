from aiogram import Router


def get_user_router() -> Router:
    from . import rug_check_handler

    router = Router()
    router.include_router(rug_check_handler.router)
    return router
