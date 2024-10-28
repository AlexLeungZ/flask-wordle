from enum import StrEnum
from pathlib import Path
from random import choice


class Result(StrEnum):
    HIT = "O"  # Correct letter in the correct spot
    PRES = "?"  # Correct letter but wrong spot
    MISS = "_"  # Letter not in the word


def word_checker(word: str, length: int = 5) -> str | None:
    if len(word := word.strip().lower()) == length and word.isalpha():
        return word


# Function to read words from the file
def words_loader(filename: Path) -> list[str]:
    with filename.open() as file:
        return [word for line in file if (word := word_checker(line))]


# Function to check if the user input is exactly 5 characters
def input_getter() -> str:
    msgEnter = "Enter a 5-letter word: "
    msgFailed = "Input must be exactly 5 letters. Try again."

    guess = None
    while not guess:
        if guess := word_checker(input(msgEnter)):
            return guess
        print(msgFailed)

    raise Exception("never")


# Function to compare the guess with the target word
def wordle_checker(guess: str, target: str) -> str:
    return "".join(
        Result.HIT if gChar == tChar else Result.PRES if gChar in target else Result.MISS
        for gChar, tChar in zip(guess, target, strict=False)
    )


def wordle(target: str, max_rounds: int = 6) -> None:
    print(f"(For testing purposes, the target word is: {target})")

    for _ in range(max_rounds):
        guess = input_getter()
        result = wordle_checker(guess, target)
        print(f"Result: {result}")

        if guess == target:
            print("Congratulations, you guessed the word!")
            return

    print(f"Sorry, you've used all {max_rounds} rounds. The word was '{target}'.")


# Main entry point
if __name__ == "__main__":
    file = Path("./words/default.txt")
    if words := words_loader(file):
        word = choice(words)  # noqa: S311
        wordle(word)