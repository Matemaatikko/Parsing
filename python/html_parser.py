from dataclasses import dataclass
from typing import List, Optional

from core_parser import Parser


@dataclass
class Html:
    elements: List['Element']

@dataclass
class Element:
    pass

@dataclass
class Tag(Element):
    name: str
    attributes: List['Attribute']
    content: Html | None

@dataclass
class Text(Element):
    value: str

@dataclass
class Comment(Element):
    value: str

@dataclass
class Attribute:
    name: str
    content: Optional[str]


class HtmlParser(Parser):
    ignore = ["br", "hr", "meta", "img", "input", "!doctype"]

    def parse(self):
        return Html(self.do_until(self.parse_element, self.has_ended))

    def parse_tag(self):
        self.skip("<")
        self.skip_white_spaces()

        if self.check("!--"): #Comment
            self.skip("!--")
            content = self.collect_until(lambda: self.check("-->"))
            self.skip("-->")
            return Comment(content)

        name = self.collect_until(lambda: self.peek() == ' ' or self.peek() == '>')
        self.skip_white_spaces()

        attributes = self.do_until(self.parse_attribute, lambda: self.peek() == '>')
        self.skip(">")
        closing = f"</{name}>"

        if name.lower().strip() == 'script' or name.lower().strip() == 'style':  #script/style content parsing skip
            content = self.collect_until(lambda: self.check(closing))
            self.skip(closing)
            return Tag(name, attributes, Html([Text(content)]))
        
        elif name.lower().strip() in self.ignore:
            return Tag(name, attributes, None)
        
        else:
            content = Html(self.do_until(self.parse_element, lambda: self.check(closing)))
            self.skip(closing)
            return Tag(name, attributes, content)

    def parse_attribute(self):
        name = self.collect_until(lambda: self.peek() == '=' or self.peek() == ' ' or self.peek() == '>')
        if self.peek() != '=':
            return Attribute(name, None)
        else:
            self.skip("=\"")
            value = self.collect_until(lambda: self.peek() == '\"')
            self.skip("\"")
            self.skip_white_spaces()
            return Attribute(name, value)

    def parse_element(self):
        if self.peek() == '<':
            return self.parse_tag()
        else:
            return Text(self.collect_until(lambda: self.peek() == '<'))
