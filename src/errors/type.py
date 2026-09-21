from enum import StrEnum


class ErrorType(StrEnum):
    NOT_MATCH_REGEX = "not_match_regex"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
