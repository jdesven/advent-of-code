[Link to puzzle](https://adventofcode.com/2025/day/1)
## Pre-processing

We start off by importing the input as a list, and then we calculate the value of the dial after every instruction. We pretend that this dial has infinitely many numbers in both the positive and negative direction - i.e. we do not flip back the dial position to the number 0 after passing the number 99. This will help us later when we need to calculate how many times we pass the number 0.

```python
input = [50] + open("2025\input\day1_input.txt").read().split('\n')

for i in range(1, len(input)):
    input[i] = input[i - 1] + (int(input[i][1:]) * (1 if input[i][0] == 'R' else -1))
```

## Solution

The answer to the first question is found by counting the amount of numbers in our list that can be divided by 100. In a circular dial with numbers going from 0 to 99, these numbers will end up at the position of the number 0, which is the answer to our question.

```python
print([num % 100 for num in input].count(0))
```

The answer to the second question is a bit more complicated. In essence, the amount of times that 0 is passed in one step is equal to the difference between the original and next value divided by 100, floored to the integer `abs(b // 100 - a // 100)`. For example, going from the number 99 to 250 would pass 0 twice, as the number 99 is floored to 0 and the number 250 is floored to 2. However, this leaves two edge cases;

1. If the original position is 0 then no 0 is passed with a small right-sided turn, yet the usual formula `abs(b // 100 - a // 100)` would result in 1 (f.e. going from 100 to 110 would not pass 0 but the formula would calculate to 1). We account for this using `(abs(b - a) // 100)`.
2. If the new position is 0 then one 0 is being passed, but the usual formula does not account for this if we are coming from the right (f.e. going from 5 to 0  should count as 1 even though the formula calculates to 0). We account for this using `sum((1 + abs(b - a) // 100)`.

With these rules, we can calculate how many times we pass - or land on - the number 0.

```python
print(sum((1 + abs(b - a) // 100) if b % 100 == 0
    else (abs(b - a) // 100) if a % 100 == 0
    else abs(b // 100 - a // 100)
    for a, b in zip(input, input[1:])
))
```