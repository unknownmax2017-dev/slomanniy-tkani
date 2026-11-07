import random
import re
import string


def flip_text(text: str) -> str:
    table = str.maketrans(
        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "ɐqɔpǝɟƃɥıɾʞlɯuodbɹsʇnʌʍxʎz∀qƆpƎℲפHIſʞ˥WNOԀQɹS┴∩ΛMX⅄Z0ƖᄅƐㄣϛ9ㄥ860",
    )
    return text.translate(table)[::-1]


def morse_encode(text: str) -> str:
    code = {
        "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
        "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
        "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
        "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
        "Y": "-.--", "Z": "--..", "0": "-----", "1": ".----", "2": "..---",
        "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
        "8": "---..", "9": "----.",
    }
    return " ".join(code.get(c.upper(), c) for c in text)


def zalgo(text: str, intensity: int = 2) -> str:
    marks = [
        "\u0300", "\u0301", "\u0302", "\u0303", "\u0304", "\u0305", "\u0306",
        "\u0307", "\u0308", "\u0309", "\u030a", "\u030b", "\u030c", "\u030d",
        "\u030e", "\u030f", "\u0310", "\u0311", "\u0312", "\u0313", "\u0314",
        "\u0315", "\u0316", "\u0317", "\u0318", "\u0319", "\u031a", "\u031b",
        "\u031c", "\u031d", "\u031e", "\u031f",
    ]
    return "".join(c + "".join(random.choice(marks) for _ in range(intensity)) for c in text)


def leet(text: str, mode: int = 1337) -> str:
    if mode == 1337:
        repl = {"a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7", "l": "1"}
    else:
        repl = {"4": "a", "3": "e", "1": "i", "0": "o", "5": "s", "7": "t"}
    return "".join(repl.get(c, c) for c in text)


def words_one_by_one(text: str) -> str:
    return text.replace(" ", "\u200b") if text else text


def calc(expr: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/().%\s]*", expr):
        return "Недопустимые символы в выражении."
    expr = expr.replace("^", "**").replace(",", ".")
    try:
        result = eval(expr)  # noqa: S307 - числа и операторы уже отфильтрованы
        return f"{expr} = {result}"
    except Exception:
        return "Не удалось вычислить выражение."


def qr_make(data: str) -> bytes:
    pass


def pick(pool: list) -> str:
    return random.choice(pool)


DICES = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12, "d20": 20}