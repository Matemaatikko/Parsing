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
    content: Html

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


class PrintHtml:
    @staticmethod
    def apply(html):
        return "".join(PrintHtml.print_elem(element) for element in html.elements)

    @staticmethod
    def print_elem(element):
        if isinstance(element, Tag):
            return f"<{element.name} {PrintHtml.print_attributes(element.attributes)}>{PrintHtml.apply(element.content)}</{element.name}>"
        elif isinstance(element, Text):
            return element.value

    @staticmethod
    def print_attributes(attributes):
        return " ".join(PrintHtml.print_attribute(attribute) for attribute in attributes)

    @staticmethod
    def print_attribute(attribute):
        if attribute.content:
            return f'{attribute.name}="{attribute.content}"'
        else:
            return attribute.name


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
            return Tag(name, attributes, Html([]))
        
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
