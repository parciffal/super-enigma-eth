from aiogram import Router


def ads_router():
    from . import show_ads, add_ads, edit_ads

    router = Router()
    router.include_router(add_ads.router)
    router.include_router(show_ads.router)
    router.include_router(edit_ads.router)

    return router
