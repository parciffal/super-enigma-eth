from aiogram import Router


def admin_router() -> Router:
    from . import menu

    router = Router()
    router.include_router(menu.get_admin_menu_router())
    return router
