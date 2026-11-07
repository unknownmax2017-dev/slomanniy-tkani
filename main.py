import logging

from aiogram import types
from aiogram.types import Update
from aiohttp import web

import config
from handlers import router

logging.getLogger("aiogram").setLevel(logging.WARNING)

config.dp.include_router(router)


async def on_startup(_: web.Application) -> None:
    if config.DOMAIN:
        wh = f"https://{config.DOMAIN}{config.WEBHOOK_PATH}"
        await config.bot.set_webhook(wh)
    else:
        raise RuntimeError("DOMAIN не задан в переменных окружения Render")


async def handle_webhook(request: web.Request) -> web.Response:
    update = types.Update.model_validate(await request.json())
    await config.bot.process_update(update)
    return web.Response(status=200)


def build_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.router.add_post(config.WEBHOOK_PATH, handle_webhook)
    return app


if __name__ == "__main__":
    web.run_app(build_app(), host=config.WEBAPP_HOST, port=config.WEBAPP_PORT)