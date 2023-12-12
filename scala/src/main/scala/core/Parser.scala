package core

import scala.annotation.tailrec

class Parser(stream: Iterator[Char]) {

  val streamEnded = '¶'
  var loadedCharacters = List[Char]()

  private def append =
    if(stream.hasNext) loadedCharacters :+= stream.next()
    else loadedCharacters :+= streamEnded

  private def skipSingle(value: Char, error: String = ""): Unit =
    if peek != value then throw new Exception(error + peek(70))
    consume

  private def consume: Char =
    val last = peek
    loadedCharacters = loadedCharacters.drop(1)
    last

  ///////////

  def peek: Char =
    if(loadedCharacters.isEmpty) append
    loadedCharacters.head

  def peek(n: Int): String =
    while(loadedCharacters.length < n) append
    loadedCharacters.take(n).mkString

  def check(str: String): Boolean =
    peek(str.length) == str

  //////////////////

  def skipTimes(times: Int) =
    (0 until times).foreach(_ => consume)

  def skipUntil(condition: => Boolean, error: String = ""): Unit =
    if !condition then
      consume
      skipUntil(condition, error)

  def skip(value: String, error: String = ""): Unit =
    value.foreach(c => skipSingle(c, error))

  def skipWhiteSpaces =
    while (peek.isWhitespace) consume

  def skipWhiteSpacesUnlessLineBreak =
    while (peek.isWhitespace && peek != '\n')  consume

  //////////////////

  def collectUntil(condition: => Boolean): String =
    @tailrec
    def iter(result: String): String =
      if(!condition && peek != streamEnded) iter(result + consume)
      else result
    iter("")

  def doUntil[A](fun: => A, condition: => Boolean): Seq[A] =
    @tailrec
    def iter(result: Seq[A]): Seq[A] =
      if(!condition && peek != streamEnded) iter(result :+ fun)
      else result
    iter(Nil)

  def hasEnded: Boolean = peek == streamEnded
}