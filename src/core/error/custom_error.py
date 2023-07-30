from core.error.error_list import ErrorCode


class FastAPIException(Exception):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        self.error_code = error_code
        self.detail = detail
