## CTok (C Tokenizer)

This is a simple demonstration script that will (sub)tokenize C code. 

### Dependencies

```
pycparser==2.20
spiral @ git+https://github.com/casics/
```

### Subtokenization

It is known that, to measure semantic similarities between code, it is better to subtokenize code tokens. This means that we will break down camelCases, or snake_cases, to smaller tokens. [Spriral](https://github.com/casics/spiral) is the most widely known subtokenizer, and you can find relevant literature from its webpage.

### Example

The example source code is hard-coded into `ctok.py`:

```C
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
```

After calling the lexer from `pycparser`, we get the following tokens:

```
['static', 'void', 'error', '(', 'mesg', ',', 'errnum', ')', 'const', 'char', '*', 'mesg', ';', 'int', 'errnum', ';', '{', 'if', '(', 'errnum', ')', 'fprintf', '(', 'stderr', ',', '"%s: %s: %s\\n"', ',', 'prog', ',', 'mesg', ',', 'strerror', '(', 'errnum', ')', ')', ';', 'else', 'fprintf', '(', 'stderr', ',', '"%s: %s\\n"', ',', 'prog', ',', 'mesg', ')', ';', 'errseen', '=', '1', ';', '}']
```

In Information Retrieval, it is also known that some keywords that occur too frequently will not contain much information. We filter them using a predefined set of [stopwords](https://stackabuse.com/removing-stop-words-from-strings-in-python/): you can change its contents to filter more or fewer tokens. After filtering, we get:

```
['static', 'error', 'mesg', 'errnum', 'const', 'mesg', 'errnum', 'errnum', 'fprintf', 'stderr', '"%s: %s: %s\\n"', 'prog', 'mesg', 'strerror', 'errnum', 'fprintf', 'stderr', '"%s: %s\\n"', 'prog', 'mesg', 'errseen']
```

If we want, we can go further by applying the subtokenization. A popular choice is Ronin from Spiral, after which we get:

```
['static', 'error', 'mesg', 'err', 'num', 'const', 'mesg', 'err', 'num', 'err', 'num', 'fpr', 'intf', 'stderr', '"%s', '%s', '%s\\n"', 'prog', 'mesg', 'str', 'error', 'err', 'num', 'fpr', 'intf', 'stderr', '"%s', '%s\\n"', 'prog', 'mesg', 'err', 'seen']
```

Note that we have separated `err` from `seen`, which seems good. However, it also incorrect split `fprintf` into `frp` and `intf`. It is likely that `fprintf` should be a stopword.