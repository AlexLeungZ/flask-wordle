from enum import StrEnum, unique
from functools import cache
from pathlib import Path


@unique
class Result(StrEnum):
    HIT = "O"  # Correct letter in the correct spot (green)
    PRES = "?"  # Correct letter but wrong spot (yellow)
    MISS = "_"  # Letter not in the word (grey)
    NULL = "~"  # Initial state (white)


def word_checker(word: str, length: int = 5) -> str | None:
    if len(word := word.strip().lower()) == length and word.isalpha():
        return word


def words_loader(filename: Path) -> list[str]:
    with filename.open() as file:
        return [word for line in file if (word := word_checker(line))]


def wordle(guess: str, target: str) -> str:
    return "".join(
        Result.HIT if gChar == tChar else Result.PRES if gChar in target else Result.MISS
        for gChar, tChar in zip(guess, target, strict=False)
    )


@cache
def _res2color() -> dict[Result | str, str]:
    return {
        Result.HIT: "bg-green-500",
        Result.PRES: "bg-yellow-400",
        Result.MISS: "bg-gray-600",
    }


@cache
def res2color(result: Result | str) -> str:
    return _res2color().get(result, "bg-white")
