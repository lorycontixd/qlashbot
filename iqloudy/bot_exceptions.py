import brawlstats

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

#*************************************************************************

class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class TagError(InputError):
    """Exception raised for errors in the input - brawl stars tags.

    Attributes:

    """

    def __init__(self, expression, message):
        super().__init__(expression,message)

#*************************************************************************

class NotFound(Error):
    """Exception raised when an object is not found.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self,message):
        self.message = message

class DiscordNotFound(NotFound):
    """Exception raised when an object is not found.

    Attributes:
        object -- Object that was not found (player,role,channel,etc)
        message -- explanation of the error
    """

    def __init__(self,object,message):
        self.object = object
        super().__init__(message)
