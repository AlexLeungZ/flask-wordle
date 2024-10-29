from enum import StrEnum, unique
from typing import Self


# Default message class for Wordle end game
@unique
class Message(StrEnum):
    win = "Congratulations! The word was"
    loss = "Sorry, you've used all rounds. The word was"

    def message(self: Self, word: str | set[str]) -> tuple[str, str]:
        return self.name, f"{self.value} - {word}."


# Convert form data with name: key0, key1,..., key5 to key
def list2key(data: dict[str, str], keys: str, length: int) -> str:
    return "".join(data[key] for i in range(length) if (key := f"{keys}{i}") in data)
