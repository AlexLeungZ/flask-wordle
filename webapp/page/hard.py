from dataclasses import dataclass
from functools import cache
from typing import Self

from flask import current_app as app
from flask import render_template, request
from flask.blueprints import Blueprint
from flask.typing import ResponseReturnValue

from webapp.config.manager import FlaskManager
from webapp.handler.wordle import absurdle, word_checker
from webapp.page._wordle import Message, list2key

# No page should be rendered from this route
bp = Blueprint("hard", __name__, url_prefix="/hard")


@cache  # global
@dataclass
class Status:
    attempts: int

    def __post_init__(self: Self) -> None:
        self.reset()

    def reset(self: Self) -> None:
        with FlaskManager() as manager:
            self.target = set(manager.gvar.words)
        self.guess = ["0" * 5] * self.attempts
        self.result = ["~" * 5] * self.attempts


# Route for the normal mode
@bp.route("/", methods=["GET"])
def home() -> ResponseReturnValue:
    return render_template("wordle/hard.html")


# Route for receiving player input and update the game status
@bp.route("/form", methods=["POST"])
def form() -> ResponseReturnValue:
    status = Status(app.config.get("ROUNDS", 6))
    keyArr = list2key(request.form, "key", 5)

    attempt = request.form.get("attempt")
    message = None

    # If the attempt is valid and not exceeding the number of attempts
    if attempt and (attempt := int(attempt)) < status.attempts:
        # If the input word is valid
        if value := word_checker(keyArr):
            status.target, optimal = absurdle(value, status.target)
            status.guess[attempt] = value
            status.result[attempt] = optimal
            attempt += 1

        # If player wins the game
        if len(status.target) == 1 and value in status.target:
            message = Message.win.message(status.target.pop())
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
    app.logger.info(f"Current target: {status.target}"[:150])
    app.logger.info(f"Guess history: {status.guess}")

    return render_template(
        "wordle/form.html",
        guess=status.guess,
        result=status.result,
        attempt=attempt,
        message=message,
    )
