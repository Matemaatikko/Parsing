import { Parser, ResolveParserRef } from "../core/parser"

type Html = {
    elements: HtmlElement[]
}

type HtmlElement = Tag | HtmlText

type Tag = {
    name: string
    attributes: Attribute[]
    content: Html
}

type HtmlText = {
    value: string
}

type Attribute = {
    name: string
    content?: string
}

export class PrintHtml {
    static apply(html: Html): string {
        return html.elements.map(element => PrintHtml.printElem(element)).join("")
    }

    static printElem(element: HtmlElement): string {
        if ("attributes" in element) {
            return `<${element.name} ${PrintHtml.printAttributes(element.attributes)}>${PrintHtml.apply(element.content)}</${element.name}>`
        } else if ("value" in element) {
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
    const ignore: string[] = ["br", "hr", "meta", "img", "input", "!doctype"]

    const parseAttribute = (): Attribute => {
        const name = parser.collectUntil(() => parser.peek() === '=' || parser.peek() === ' ' || parser.peek() === '>')
        if (parser.peek() !== '=') {
            return { name: name }
        } else {
            parser.skip("=\"")
            const value = parser.collectUntil(() => parser.peek() === '\"')
            parser.skip("\"")
            parser.skipWhiteSpaces()
            return { name: name, content: value }
        }
    }

    const parseElement = (): HtmlElement => {
        if (parser.peek() === '<') {
            return parseTag()
        } else {
            return { value: parser.collectUntil(() => parser.peek() === '<') }
        }
    }

    const parseTag = (): Tag => {
        parser.skip("<")
        parser.skipWhiteSpaces()
        // TODO Parse comment

        const name = parser.collectUntil(() => parser.peek() === ' ' || parser.peek() === '>')
        parser.skipWhiteSpaces()
        const attributes = parser.doUntil(parseAttribute, () => parser.peek() === '>')
        parser.skip(">")
        const closing = `</${name}>`
        // TODO Skip script/style
        if (ignore.includes(name.toLowerCase().trim())) {
            return { name: name, attributes: attributes, content: { elements: [] } }
        } else {
            const content = { elements: parser.doUntil(parseElement, () => parser.check(closing)) }
            parser.skip(closing)
            return { name: name, attributes: attributes, content: content }
        }
    }

    const parse = (): Html => {
        return { elements: parser.doUntil(parseElement, parser.hasEnded) }
    }

    return parse()
}

