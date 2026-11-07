import asyncio
import random

from aiogram import F, Router, types
from aiogram.filters import Command

from data import store
from utils import calc, flip_text, leet, morse_encode, words_one_by_one, zalgo, DICES

router = Router()

PREMIUM_FEATURES = {".stt", ".save", ".voice", ".blur", ".wtm", ".tr", ".sum", ".hint"}


def require_premium(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        if store.is_premium(message.from_user.id):
            return await func(message, *args, **kwargs)
        await message.answer_html(
            "Это функция <b>Ch</b>atsFlow+ (премиум). Чтобы активировать, напишите /premium"
        )
        return None

    wrapper.__name__ = func.__name__
    return wrapper


def parse_flags(text: str) -> str:
    return text.lstrip("/. ")


@router.message(Command("start", "help"))
async def cmd_start(message: types.Message):
    store.register(message.from_user.id)
    await message.answer_html(
        "<b>Ch</b>atsFlowBot — аналог.\n\n"
        "Доступно (бесплатно):\n"
        ".quote .haha .rsp .revo .coin .ball (игры)\n"
        ".flip .zalgo .bubble .sp .b .morse .words .leet (текст)\n"
        ".calc .remind .qr .word (утилиты)\n\n"
        "Премиум (+, /premium):\n"
        ".stt .save .voice .tr .sum .hint .blur .wtm\n\n"
        "Напишите /premium, чтобы увидеть тарифы."
    )


@router.message(Command("premium"))
async def cmd_premium(message: types.Message):
    store.register(message.from_user.id)
    user_premium = store.is_premium(message.from_user.id)
    text = (
        "<b>Ch</b>atsFlow+\n\n"
        "Тарифы (пример):\n"
        ". ⭐ 1 месяц — 100₽\n"
        ". ⭐ 3 месяца — 250₽\n"
        ". ⭐ Навсегда — 500₽\n\n"
    )
    if user_premium:
        text += "✅ У вас уже активен премиум!\nАдмин может выдать /gift @username дней"
    else:
        text += (
            "Для оплаты напишите основателю напрямую, либо используйте "
            "/activate со специальным кодом, выданным админом."
        )
    await message.answer_html(text)


@router.message(Command("activate"))
async def cmd_activate(message: types.Message):
    store.register(message.from_user.id)
    code = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
    if code and code.strip() == "CHATSFLOWFREE":
        store.set_premium(message.from_user.id, True, days=30)
        await message.answer_html("✅ Премиум активирован на 30 дней!")
    else:
        await message.answer_html("Неверный код. Коды выдаёт администратор.")


# --- Игры ---
@router.message(F.text.startswith((".quote")))
async def cmd_quote(message: types.Message):
    await message.answer(random.choice(
        ["«Жизнь — то, что с тобой происходит, пока ты строишь планы».", "«Всё будет хорошо, просто не сдавайся!»"]
    ))


@router.message(F.text.startswith((".coin")))
async def cmd_coin(message: types.Message):
    await message.answer("Орёл" if random.random() < 0.5 else "Решка")


@router.message(F.text.startswith((".ball")))
async def cmd_ball(message: types.Message):
    await message.answer(random.choice([
        "Да.", "Нет.", "Скорее да.", "Скорее нет.", "Не знаю.", "Определённо да.", "Попробуй позже."
    ]))


@router.message(F.text.startswith((".rsp")))
async def cmd_rsp(message: types.Message):
    you = random.choice(["камень", "ножницы", "бумага"])
    bot = random.choice(["камень", "ножницы", "бумага"])
    if you == bot:
        res = "Ничья 🤝"
    elif (you, bot) in {("камень", "ножницы"), ("ножницы", "бумага"), ("бумага", "камень")}:
        res = "Ты выиграл ✅"
    else:
        res = "Бот выиграл 🤖"
    await message.answer(f"Ты: {you}\nБот: {bot}\n{res}")


@router.message(F.text.startswith((".ruletka", ".revo")))
async def cmd_ruletka(message: types.Message):
    await message.answer("🔫 *КЛАЦ* — повезло, пуля не вылетела.")


# --- Текст ---
@router.message(F.text.startswith((".flip")))
async def cmd_flip(message: types.Message):
    text = parse_flags(message.text[len(".flip"):])
    await message.answer(flip_text(text) if text else "Напиши текст после команды, например: /flip привет")


@router.message(F.text.startswith((".morse")))
async def cmd_morse(message: types.Message):
    text = parse_flags(message.text[len(".morse"):])
    await message.answer(morse_encode(text))


@router.message(F.text.startswith((".zalgo")))
async def cmd_zalgo(message: types.Message):
    text = parse_flags(message.text[len(".zalgo"):])
    await message.answer(zalgo(text, 3))


@router.message(F.text.startswith((".leet")))
async def cmd_leet(message: types.Message):
    text = parse_flags(message.text[len(".leet"):])
    await message.answer(leet(text, 1337))


@router.message(F.text.startswith((".words")))
async def cmd_words(message: types.Message):
    text = parse_flags(message.text[len(".words"):])
    await message.answer(words_one_by_one(text))


@router.message(F.text.startswith((".b")))
async def cmd_b(message: types.Message):
    text = parse_flags(message.text[len(".b"):])
    await message.answer_html(f"<b>{text}</b>")


@router.message(F.text.startswith((".sp")))
async def cmd_sp(message: types.Message):
    text = parse_flags(message.text[len(".sp"):])
    await message.reply(f"||{text}||")


# --- Утилиты ---
@router.message(F.text.startswith((".calc")))
async def cmd_calc(message: types.Message):
    expr = parse_flags(message.text[len(".calc"):])
    await message.answer(calc(expr))


@router.message(F.text.startswith((".remind")))
async def cmd_remind(message: types.Message):
    parts = message.text.split(maxsplit=2)
    if len(parts) < 3:
        await message.answer("Формат: .remind <секунды> <текст>")
        return
    try:
        seconds = int(parts[1])
    except ValueError:
        await message.answer("Секунды должны быть числом.")
        return
    store.add_reminder(message.from_user.id, parts[2], seconds)
    await message.answer(f"⏰ Напомню через {seconds}с: {parts[2]}")

    await asyncio.sleep(seconds)
    await message.answer(f"⏰ Напоминание: {parts[2]}")


@router.message(F.text.startswith((".qr")))
async def cmd_qr(message: types.Message):
    text = parse_flags(message.text[len(".qr"):])
    await message.answer("QR-код генерируется в полной версии (нужна библиотека qrcode).")


# --- Премиум (смотри требование к подписке) ---
@router.message(F.text.startswith((".stt", ".save", ".voice", ".tr", ".sum", ".hint", ".blur", ".wtm")))
@require_premium
async def cmd_premium_feature(message: types.Message):
    await message.answer("⚙️ Эта премиум-функция в плане. В рабочей версии здесь будет вызов ИИ/медиа-обработки.")


# Кубики
@router.message(F.text.startswith((d.lower() for d in DICES)))
async def cmd_dice(message: types.Message):
    name = message.text.split()[0].lstrip("/.")
    sides = DICES.get(name, 6)
    await message.answer(f"🎲 {random.randint(1, sides)}")