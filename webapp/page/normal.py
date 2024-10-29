from dataclasses import dataclass
from enum import StrEnum, unique
from functools import cache
from random import choice
from typing import Self

from flask import current_app as app
from flask import render_template, request
from flask.blueprints import Blueprint
from flask.typing import ResponseReturnValue

from webapp.config.manager import FlaskManager
from webapp.handler.wordle import word_checker, wordle

# No page should be rendered from this route
bp = Blueprint("normal", __name__, url_prefix="/normal")


@cache  # global
@dataclass
class Status:
    attempts: int

    def __post_init__(self: Self) -> None:
        self.reset()

    def reset(self: Self) -> None:
        with FlaskManager() as manager:
            self.target = choice(manager.gvar.words)  # noqa: S311
        self.guess = ["0" * 5] * self.attempts
        self.result = ["~" * 5] * self.attempts


@unique
class Message(StrEnum):
    win = "Congratulations! The word was"
    loss = "Sorry, you've used all rounds. The word was"

    def message(self: Self, word: str) -> tuple[str, str]:
        return self.name, f"{self.value} - {word}."


# Convert form data with name: key0, key1,..., key5 to list
def get_list(data: dict[str, str], keys: str, length: int) -> list[str]:
    return [data[key] for i in range(length) if (key := f"{keys}{i}") in data]


# Route for the normal mode
@bp.route("/", methods=["GET"])
def home() -> ResponseReturnValue:
    return render_template(
        "normal/normal.html",
    )


# Route for receiving player input and update the game status
@bp.route("/form", methods=["POST"])
def form() -> ResponseReturnValue:
    status = Status(app.config.get("ROUNDS", 6))
    keyArr = "".join(get_list(request.form, "key", 5))

    attempt = request.form.get("attempt")
    message = None

    # If the attempt is valid and not exceeding the number of attempts
    if attempt and (attempt := int(attempt)) < status.attempts:
        # If the input word is valid
        if value := word_checker(keyArr):
            result = wordle(value, status.target)
            status.guess[attempt] = value
            status.result[attempt] = result
            attempt += 1

        # If player wins the game
        if value == status.target:
            message = Message.win.message(status.target)
            status.reset()
            attempt = None

        # If player loses the game
        elif attempt >= status.attempts:
            message = Message.loss.message(status.target)
            status.reset()
            attempt = None

    else:
        status.reset()
        attempt = None

    # Logging the correct answer and guess history to the logger
    app.logger.info(f"Current target: {status.target}")
    app.logger.info(f"Guess history: {status.guess}")

    return render_template(
        "normal/form.html",
        guess=status.guess,
        result=status.result,
        attempt=attempt,
        message=message,
    )
