from collections import defaultdict
from enum import StrEnum, unique
from functools import cache
from pathlib import Path


# Enum for Result values
@unique
class Result(StrEnum):
    HIT = "O"  # Correct letter in the correct spot (green)
    PRES = "?"  # Correct letter but wrong spot (yellow)
    MISS = "_"  # Letter not in the word (grey)
    NULL = "~"  # Initial state (white)


# Check if the word is valid and of the correct length
def word_checker(word: str, length: int = 5) -> str | None:
    if len(word := word.strip().lower()) == length and word.isalpha():
        return word


# Load words from a file and filter valid ones
def words_loader(filename: Path) -> list[str]:
    with filename.open() as file:
        return [word for line in file if (word := word_checker(line))]


# Main wordle logic that return the result pattern
def wordle(guess: str, target: str) -> str:
    return "".join(
        Result.HIT if gChar == tChar else Result.PRES if gChar in target else Result.MISS
        for gChar, tChar in zip(guess, target, strict=False)
    )


# Finalize the result pattern into hits and presses count
def pattern_finalizer(key: str) -> tuple[int, int]:
    return (key.count(Result.HIT), key.count(Result.PRES))


# Main absurdle logic that return the most optimal group of words and its result pattern
def absurdle(guess: str, words: set[str]) -> tuple[set[str], str]:
    # Group possible words by their result pattern
    patterns = defaultdict[str, set[str]](set[str])
    for word in words:
        pattern = wordle(guess, word)
        patterns[pattern].add(word)

    # Choose the optimal pattern with minimum hits and presses
    optimal = min(patterns, key=pattern_finalizer)
    return patterns[optimal], optimal


# Cached functions for color conversion
@cache
def _res2color() -> dict[Result | str, str]:
    return {
        Result.HIT: "bg-green-500",
        Result.PRES: "bg-yellow-400",
        Result.MISS: "bg-gray-600",
    }


# Function to convert Result to color
@cache
def res2color(result: Result | str) -> str:
    return _res2color().get(result, "bg-white")
