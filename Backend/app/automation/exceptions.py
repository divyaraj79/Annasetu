class AutomationValidationError(Exception):
    """
    Raised when an email is processed
    successfully but contains invalid or
    incomplete business data.

    These emails should NOT be retried.
    Instead, the sender should be informed
    to correct and resend the email.
    """

    def __init__(
        self,
        message: str,
    ):

        super().__init__(message)

        self.message = message


class AutomationProcessingError(Exception):
    """
    Raised for unexpected infrastructure
    or processing failures.

    These emails SHOULD remain unread so
    they can be retried during the next
    scheduler cycle.
    """

    pass