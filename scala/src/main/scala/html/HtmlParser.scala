package html

import core.Parser

case class Html(elements: Seq[Element])

trait Element
case class Tag(name: String, attributes: Seq[Attribute], content: Html) extends Element
case class Text(value: String) extends Element
case class Attribute(name: String, content: Option[String])

case object PrintHtml {
  def apply(html: Html): String = html.elements.map(printElem).mkString("")

  def printElem(element: Element): String =
    element match {
      case Tag(name, attributes, content) => s"<$name ${printAttributes(attributes)}>${apply(content)}</$name>"
      case Text(value) => value
    }

  def printAttributes(attributes: Seq[Attribute]): String = attributes.map(printAttribute).mkString(" ")

  def printAttribute(attribute: Attribute): String =
    attribute.content match {
      case Some(content) => s"${attribute.name}=\"$content\""
      case None => attribute.name
    }
}


class HtmlParser(stream: Iterator[Char]) extends Parser(stream){

  val ignore = Seq("br", "hr", "meta", "img", "input", "!doctype")

  def parse(): Html =
    Html(doUntil(parseElement(), hasEnded))

  def parseTag(): Tag =
    skip("<")
    skipWhiteSpaces
    val name = collectUntil(peek == ' ' || peek == '>')
    // TODO Parse comment
    skipWhiteSpaces
    val attributes = doUntil(parseAttribute, peek == '>')
    skip(">")
    val closing = s"</${name}>"

    // TODO Skip script/style
    if ignore.contains(name.trim().toLowerCase()) then
      Tag(name, attributes, Html(Nil))
    else
      val content = Html(doUntil(parseElement(), check(closing)))
      skip(closing)
      Tag(name, attributes, content)

  def parseAttribute: Attribute =
    val name = collectUntil(peek == '=' || peek == ' ' || peek == '>')
    if peek != '=' then
      Attribute(name, None)
    else
      skip("=\"")
      val value = collectUntil(peek == '\"')
      skip("\"")
      skipWhiteSpaces
      Attribute(name, Some(value))

  def parseElement(): Element  =
    if peek == '<'
      then parseTag()
    else
      Text(collectUntil(peek == '<'))
}
