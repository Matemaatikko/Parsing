export type ParserRef = {
    stream: string
    pointer: number
    stream_ended: string
    loaded_characters: string[]
}

export const ResolveParserRef = (str: string): ParserRef => {
    return (
        { stream: str, pointer: 0, stream_ended: '¶', loaded_characters: [] }
    )
}


export const Parser = (ref: ParserRef) => {

    const next = () => {
        const value = ref.stream[ref.pointer]
        ref.pointer = ref.pointer + 1
        return value
    }

    const append = (): void => {
        try {
            const nextChar = next()
            if (nextChar === null || nextChar === undefined) {
                throw new Error("")
            }
            ref.loaded_characters.push(nextChar)
        } catch (error) {
            ref.loaded_characters.push(ref.stream_ended)
        }
    }

    const skipSingle = (value: string, error: string = ""): void => {
        if (peek() !== value) {
            throw new Error(error + peek().substring(0, 70))
        }
        consume()
    }

    const consume = (): string => {
        const last = peek()
        ref.loaded_characters = ref.loaded_characters.slice(1)
        return last
    }

    ///////////////////////////

    const peek = (n: number = 1): string => {
        while (ref.loaded_characters.length < n) {
            append()
        }
        return ref.loaded_characters.slice(0, n).join('')
    }

    const check = (str: string): boolean => {
        console.log("================")
        console.log(peek(str.length))
        console.log(str)
        console.log(peek(str.length) === str)

        return peek(str.length) === str
    }

    //////////////////////////////

    const skipTimes = (times: number): void => {
        for (let i = 0; i < times; i++) {
            consume()
        }
    }

    const skipUntil = (condition: () => boolean, error: string = ""): void => {
        if (!condition()) {
            consume()
            skipUntil(condition, error)
        }
    }


    const skip = (value: string, error: string = ""): void => {
        for (const c of value) {
            skipSingle(c, error)
        }
    }

    const skipWhiteSpaces = (): void => {
        while (peek().trim() === "") {
            consume()
        }
    }

    /////////////////////////////////

    const collectUntil = (condition: () => boolean): string => {
        let result = ""
        while (!condition() && peek() !== ref.stream_ended) {
            result += consume()
        }
        return result
    }

    const doUntil = <A>(fun: () => A, condition: () => boolean): A[] => {
        const result: A[] = []
        while (!condition() && peek() !== ref.stream_ended) {
            result.push(fun())
        }
        return result
    }

    const hasEnded = (): boolean => {
        return peek() === ref.stream_ended
    }

    return {
        peek: peek,
        check: check,
        skipTimes: skipTimes,
        skipUntil: skipUntil,
        skip: skip,
        skipWhiteSpaces: skipWhiteSpaces,
        collectUntil: collectUntil,
        doUntil: doUntil,
        hasEnded: hasEnded
    }
}
