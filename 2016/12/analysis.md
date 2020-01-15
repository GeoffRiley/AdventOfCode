# Leonardo's Monorail
[Advent of Code 2018 Day 12](https://adventofcode.com/2016/day/12)

The task for today was to create a computer simulator with a very simple instruction set.
Just four instructions are recognised:
- `cpy x,y` Copy value or register x into register y
- `inc x` Increment register x by 1
- `dec x` Decrement register x by 1
- `jnz x,y` Jump relative y instructions if value or register x is not zero

Here is the code:
```text
cpy 1 a
cpy 1 b
cpy 26 d
jnz c 2
jnz 1 5
cpy 7 c
inc d
dec c
jnz c -2
cpy a c
inc a
dec b
jnz b -2
cpy c b
dec d
jnz d -6
cpy 14 c
cpy 14 d
inc a
dec d
jnz d -2
dec c
jnz c -5
```

Turning this into pseudo-code makes it easier to understand:
- At the start, register c is pre-set: to 0 for Part 1 and to 1 for Part 2
```text
Initialise:
    LET a ← 1
        b ← 1
        d ← 26
    IF c != 0 GOTO (Part2Entry)
    GOTO (Part1Entry)
```
- This effectively adds 7 to register d
```text
Part2Entry:
    LET c ← 7
Part2Loop:
    LET d ← d + 1
        c ← c - 1
    IF c != 0 GOTO (Part2Loop)
```
- At this point the only difference between Part 1 and Part 2
 is that register d is set to 33 rather than 26
 All other registers: a = 1; b = 1; c = 0

- This pair of loops generate the Fibonacci sequence, starting from the second position:
  - Before the first time through a = 1; b = 1
  - After the fist time through a = 2 (ie: a+b); b = 1 (ie: the old value of a)
  - After the second time through a = 3; b = 2
  - After the third time through a = 5; b = 3 
```text
Part1Entry:
    LET c ← a
Part1Loop:
    LET a ← a + 1
        b ← b - 1
    IF b != 0 GOTO (Part1Loop)
    LET b ← c
        d ← d - 1
    IF d != 0 GOTO (Part1Entry)
```
- The loop continues for 'd' times, ie 26 times for Part 1 or 33 times for Part 2                                           

- Finally there is a fixed addition of 14 times 14 added to a through this last loop
```text
    LET c ← 14
ExitOuterLoop:
    LET d ← 14
ExitInnerLoop:
    LET a ← a + 1
        d ← d - 1
    IF d != 0 GOTO (ExitInnerLoop)
    LET c ← c - 1
    IF c != 0 GOTO (ExitOuterLoop)
```
As the calculation started at the second Fibonacci number the equivalent `fib()` calls would have two added to them.

The final value, therefore, is the 28<sup>th</sup> or 35<sup>th</sup> Fibonacci number plus 14<sup>2</sup>.
- fib(28) = 317,811; plus 14<sup>2</sup> → 318,007
- fib(35) = 9,227,465; plus 14<sup>2</sup> → 9,227,661
