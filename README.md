# ChatsFlowBot-like Telegram Bot

Аналог бота ChatsFlowBot на обычном Bot API (Python + aiogram 3), без юзербота на личном аккаунте.

## Что внутри

Бесплатные функции:
- Игры: `.quote`, `.coin`, `.ball`, `.rsp`, `.ruletka`
- Текст: `.flip`, `.morse`, `.zalgo`, `.leet`, `.words`, `.b`, `.sp`
- Утилиты: `.calc`, `.remind`, `.qr`
- Кубики: `.d4`–`.d20`

Премиум (Ch...atsFlow+):
- Функции помечаются `@require_premium`: `.stt`, `.save`, `.voice`, `.tr`, `.sum`, `.hint`, `.blur`, `.wtm`
- Выдача премиума: `/premium`, активация вручную командой `/activate <код>` (код по умолчанию `CHATSFLOWFREE`).

## Запуск локально

```bash
pip install -r requirements.txt
copy .env.example .env   # впишите BOT_TOKEN из @BotFather
python main.py           # без DOMAIN запустит polling
```

## Развёртывание на Render

1. Загрузите папку `bot/` в Git-репозиторий (GitHub).
2. В Render: New → Web Service → выберите репозиторий.
3. Runtime: Python. Build: `pip install -r requirements.txt`. Start: `python main.py`.
4. В Environment добавьте:
   - `BOT_TOKEN` — токен из @BotFather
   - `DOMAIN` — адрес сервиса без протокола, например `chatsflow-bot.onrender.com`
5. Render сам выставит `PORT`; `main.py` повесит вебхук и поднимет aiohttp-сервер.
6. Если используете `render.yaml` из репозитория → Blueprint.

## Ограничения (честно)

Функции, требующие **личного аккаунта** (юзербот): анти-удаление, `.online`, клонирование профиля, часы в фамилии, золотая рамка, автоответчик, логи чатов — обычный Bot API их **не поддерживает**. Их можно добавить только Telethon/Pyrogram на отдельном аккаунте (нарушает ToS Telegram, риск бана — на свой страх).

Функции Telegram Premium (скриншоты без уведомления, Premium-стикеры) закрыты на уровне платформы — их невозможно отдать через публичного бота.