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
    win = "Congratulations, you guessed the word!"
    loss = "Sorry, you've used all rounds. The word was"


def get_list(data: dict[str, str], keys: str, length: int) -> list[str]:
    return [data[key] for i in range(length) if (key := f"{keys}{i}") in data]


# Redirect to main
@bp.route("/", methods=["GET"])
def home() -> ResponseReturnValue:
    return render_template(
        "normal/normal.html",
    )


@bp.route("/form", methods=["POST"])
def form() -> ResponseReturnValue:
    status = Status(app.config.get("ROUNDS", 6))
    keyArr = "".join(get_list(request.form, "key", 5))

    attempt = request.form.get("attempt")
    message = None

    if attempt and (attempt := int(attempt)) < status.attempts:
        if value := word_checker(keyArr):
            status.guess[attempt] = value
            status.result[attempt] = wordle(value, status.target)
            attempt += 1

        if value == status.target:
            message = (msg := Message.win).name, msg.value
        elif attempt >= status.attempts:
            message = (msg := Message.loss).name, f"{msg.value} - {status.target}"

    else:
        status.reset()
        attempt = None

    app.logger.info(f"Current target: {status.target}")
    app.logger.info(f"Guess history: {status.guess}")

    return render_template(
        "normal/form.html",
        guess=status.guess,
        result=status.result,
        attempt=attempt,
        message=message,
    )
