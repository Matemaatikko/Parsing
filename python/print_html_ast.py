
from html_parser import *


def print_html(html: Html):
    return "".join(print_elem(element) for element in html.elements)

def print_elem(element: Element):
    if isinstance(element, Tag) and element.content is None:
        return f"<{element.name}{print_attributes(element.attributes)}>"
    elif isinstance(element, Tag):
        return f"<{element.name}{print_attributes(element.attributes)}>{print_html(element.content)}</{element.name}>"
    elif isinstance(element, Text):
        return element.value
    elif isinstance(element, Comment):
        return "<!--" + element.value + "-->"

def print_attributes(attributes: List[Attribute]):
    result = " ".join(print_attribute(attribute) for attribute in attributes)
    if(len(result) > 0): result = " " + result
    return result 

def print_attribute(attribute: Attribute):
    if attribute.content is None:
        return attribute.name
    else:
        return f'{attribute.name}="{attribute.content}"'
        