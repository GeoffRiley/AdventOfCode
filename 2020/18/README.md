# Advent of Code

## Day 18: Operation Order

I started spinning my own parser, [see day18.py](day18.py), which worked fine for part 1. However, when presented with
part 2 it was difficult to modify in order to operate with the extra criteria.

I have previously used Lex and Yacc (or Flex and Bison for GNU versions) on a C language target to develop much more
complex parsers… so I hunted around for something similar working with Python and
found [sly](https://github.com/dabeaz/sly) —SLY Lex Yacc written 100% in Python.

As I had already submitted part one, and knew it was correct, I thought I could go more experimental for the second
part. So I started a second source file, [see day18a.py](day18a.py), and fiddled about with one of the example pieces of
code provided with `sly`.

The only difference between parts one and two is the precedence, so my idea was to replace the precedence declaration
within the parser and use the same parser class for both parts. However, I was unable to find a way to reset the parser
after replacing the precedence and so ended up including two copies of the parser class. It just feels wrong.