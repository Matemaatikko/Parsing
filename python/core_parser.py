class Parser:
    def __init__(self, stream):
        self.stream = iter(stream)
        self.stream_ended = '¶'
        self.loaded_characters = []

    ##########################################

    def append(self):
        try:
            next_char = next(self.stream)
            self.loaded_characters.append(next_char)
        except StopIteration:
            self.loaded_characters.append(self.stream_ended)

    def skip_single(self, value, error=""):
        if self.peek() != value:
            raise Exception(error + self.peek(70))
        self.consume()

    def consume(self):
        last = self.peek()
        self.loaded_characters = self.loaded_characters[1:]
        return last

    ##########################################

    def peek(self, n = 1):
        while len(self.loaded_characters) < n:
            self.append()
        return ''.join(self.loaded_characters[:n])

    def check(self, string):
        return self.peek(len(string)) == string
    

    ##########################################

    def skip_times(self, times):
        for _ in range(times):
            self.consume()

    def skip_until(self, condition, error=""):
        if not condition():
            self.consume()
            self.skip_until(condition, error)

    def skip(self, value, error=""):
        for c in value:
            self.skip_single(c, error)

    def skip_white_spaces(self):
        while self.peek().isspace():
            self.consume()

    def skip_white_spaces_unless_line_break(self):
        while self.peek().isspace() and self.peek() != '\n':
            self.consume()

    ##########################################

    def collect_until(self, condition):
        result = ""
        while not condition() and self.peek() != self.stream_ended:
            result += self.consume()
        return result

    def do_until(self, fun, condition):
        result = []
        while not condition() and self.peek() != self.stream_ended:
            result.append(fun())
        return result

    def has_ended(self):
        return self.peek() == self.stream_ended