import { Parser, ResolveParserRef } from "../core/parser"

class Html {
    elements: HtmlElement[]

    constructor(elements: HtmlElement[]) {
        this.elements = elements
    }
}

class HtmlElement { }

class Tag extends HtmlElement {
    name: string
    attributes: Attribute[]
    content: Html

    constructor(name: string, attributes: Attribute[], content: Html) {
        super()
        this.name = name
        this.attributes = attributes
        this.content = content
    }
}

class HtmlText extends HtmlElement {
    value: string

    constructor(value: string) {
        super()
        this.value = value
    }
}

class Attribute {
    name: string
    content: string | null

    constructor(name: string, content: string | null) {
        this.name = name
        this.content = content
    }
}

export class PrintHtml {
    static apply(html: Html): string {
        return html.elements.map(element => PrintHtml.printElem(element)).join("")
    }

    static printElem(element: HtmlElement): string {
        if (element instanceof Tag) {
            return `<${element.name} ${PrintHtml.printAttributes(element.attributes)}>${PrintHtml.apply(element.content)}</${element.name}>`
        } else if (element instanceof HtmlText) {
            return element.value
        } else {
            throw new Error("Unknown element type")
        }
    }

    static printAttributes(attributes: Attribute[]): string {
        return attributes.map(attribute => PrintHtml.printAttribute(attribute)).join(" ")
    }

    static printAttribute(attribute: Attribute): string {
        if (attribute.content !== null) {
            return `${attribute.name}="${attribute.content}"`
        } else {
            return attribute.name
        }
    }
}

export const HtmlParser = (str: string) => {

    const ref = ResolveParserRef(str)
    const parser = Parser(ref)
    const ignore: string[] = ["br", "meta", "img", "input"]

    const parseAttribute = (): Attribute => {
        const name = parser.collectUntil(() => parser.peek() === '=' || parser.peek() === ' ' || parser.peek() === '>')
        if (parser.peek() !== '=') {
            return new Attribute(name, null)
        } else {
            parser.skip("=\"")
            const value = parser.collectUntil(() => parser.peek() === '\"')
            parser.skip("\"")
            parser.skipWhiteSpaces()
            return new Attribute(name, value)
        }
    }

    const parseElement = (): HtmlElement => {
        if (parser.peek() === '<') {
            return parseTag()
        } else {
            return new HtmlText(parser.collectUntil(() => parser.peek() === '<'))
        }
    }

    const parseTag = (): Tag => {
        parser.skip("<")
        parser.skipWhiteSpaces()
        const name = parser.collectUntil(() => parser.peek() === ' ' || parser.peek() === '>')
        //console.log(name)
        parser.skipWhiteSpaces()
        const attributes = parser.doUntil(parseAttribute, () => parser.peek() === '>')
        parser.skip(">")
        const closing = `</${name}>`
        if (name.toLowerCase().trim() in ignore) {
            return new Tag(name, attributes, new Html([]))
        } else {
            const content = new Html(parser.doUntil(parseElement, () => parser.check(closing)))
            parser.skip(closing)
            return new Tag(name, attributes, content)
        }
    }

    const parse = (): Html => {
        return new Html(parser.doUntil(parseElement, parser.hasEnded))
    }

    return parse()
}

