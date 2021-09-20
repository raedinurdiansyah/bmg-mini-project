import re


def is_email(email: str) -> bool:
    try:
        regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        match = regex.match(email)

        if not match:
            return False

        return True
    except Exception:
        return False
