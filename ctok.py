import sys
from pycparser import c_parser
from spiral import ronin

# Stopwords: any tokens that occur so frequently that need to be excluded
STOPWORDS = set([
    "{","}","(",")",";",",", "[", "]", "<", ">", "+","-","=","*","%","/","&","==","!=","&&","||",
    "for", "if", "else", "while", "int", "char", "void", "return", "1"
    ])

code = r"""
static void
error(mesg, errnum)
     const char *mesg;
     int errnum;
{
  if (errnum)
    fprintf(stderr, "%s: %s: %s\n", prog, mesg, strerror(errnum));
  else
    fprintf(stderr, "%s: %s\n", prog, mesg);
  errseen = 1;
}
"""

if __name__ == '__main__':
    # We invoke a C Parser from pycparser
    parser = c_parser.CParser()
    # But we will only borrow its lexer (=tokenizer)
    parser.clex.input(code)

    # Wr read ecah token from the lexer
    tokens = []
    while True:
        t = parser.clex.token()
        if t == None:
            break
        else:
            tokens.append(t.value)
    print(tokens)

    # filter the stopwords defined above
    filtered = [t for t in tokens if not t in STOPWORDS]

    print(filtered)

    # if we want subtokenization, we can apply ronin from Spiral
    subtokens = []
    for token in filtered:
        subtokens.extend(ronin.split(token))

    print(subtokens)