# Классы для ошибок

class ParsingError(Exception):
    def __init__(self, key_error):
        self.key_error = key_error
        super().__init__()
