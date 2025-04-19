class InvalidTransitionError(Exception):
    """Raised when an invalid state transition occurs."""

    pass


class UnexpectedSlashError(Exception):
    """Raised when an unexpected '/' character is encountered."""

    pass


class UnexpectedNumericError(Exception):
    """Raised when a numeric character is encountered in an invalid state."""

    pass


class QuoteFollowedByNonWhitespaceError(Exception):
    """Raised when a quote is followed by a non-whitespace character."""

    pass


class SemanticError(Exception):
    """Raised when there has been identified error in the semantic meaning of XML elements"""

    pass
