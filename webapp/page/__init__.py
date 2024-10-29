from webapp.page import _enums as enums
from webapp.page.api import bp as api
from webapp.page.normal import bp as normal
from webapp.page.root import bp as root

__all__: list[str] = ["api", "root", "normal", "enums"]
