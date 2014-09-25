class TwineException(Exception):
    """
    General twine exception.
    """
    pass

class TwineAssertionError(TwineException):
    """
    AssertionError to raise upon failure of some twine command.
    """
    pass

class TwineNameError(TwineException):
    """
    Error to raise when an unknown command is called.
    """
    pass
