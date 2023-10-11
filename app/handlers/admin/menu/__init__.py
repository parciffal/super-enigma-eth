from aiogram import Router


def get_admin_menu_router() -> Router:
    from . import menu, admins, ads, links

    router = Router()
    router.include_router(links.router)
    router.include_router(ads.ads_router())
    router.include_router(menu.router)
    # router.include_router(groups.router)
    router.include_router(admins.router)
    return router
