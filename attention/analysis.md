# Analysis

## Layer 3, Head 11

This head appears to connect a verb to its direct object: the verb token puts
most of its attention on the noun that is being acted upon, and comparatively
little on nouns that are merely nearby. In "she wrote a letter to her sister",
`wrote` attends almost entirely to `letter` and essentially ignores `sister`,
even though `sister` is also a noun in the same clause. What convinced me this
is grammatical rather than positional is that the head has no positional
preference at all — averaged over many tokens it gives roughly the same weight
to the token before it, the token after it, and tokens three positions away —
and yet the verb-to-object link survives when I pad the object's noun phrase
with adjectives, so that the object sits two, three, or four tokens away. The
same head stays quiet when the source token is a determiner or a preposition,
which suggests it is specifically about verbs and what they act on. It is noisy:
when the object itself is the masked token the attention smears across the whole
object slot, and in "kicked the ball in the yard" the competing noun `yard`
comes close, so the pattern is a tendency rather than a rule.

Example Sentences:
- she wrote a letter to her sister and then [MASK] .
- they ate the cake with a spoon and [MASK] happily .
- the boy kicked the big red ball and [MASK] away .

## Layer 4, Head 10

This head looks like a noun-phrase head finder: a determiner or a preposition
attends to the head noun of the noun phrase it introduces, skipping over any
adjectives in between. In "he walked into the room", `into` lands on `room`, and
in "the tall man", `the` reaches past `tall` to `man`. The clearest evidence
that it is tracking grammatical structure and not just position is what happens
when the head noun is *not* the last word of the phrase. In "a bowl of soup",
`a` attends to `bowl` and almost not at all to `soup`; in "the man in the hat",
`the` attends to `man` rather than `hat`. A head that simply looked ahead a
fixed number of tokens, or looked to the end of the phrase, would get both of
those backwards. It does carry a mild forward bias — nearer nouns get somewhat
more weight than distant ones — so the link weakens as the noun phrase grows
longer, but the strongest cell in the row is still the correct head noun.

Example Sentences:
- a bowl of soup sat on the [MASK] .
- the man in the hat left and [MASK] quickly .
- he walked into the room with a smile and [MASK] .
