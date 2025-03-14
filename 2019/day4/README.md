[Link to puzzle](https://adventofcode.com/2019/day/4)
## Import

```python
with open('2019/input/day4_input.txt', 'r') as file:
    range_min, range_max = [int(num) for num in file.read().split('-')]
```

## Solution

When constructing valid integers, the numbers 0-9 that fill the six positions of the integer are dependent on the numbers that came before. This means we have to compare numbers inside the integer, so it is convenient to save the integers as a list of six numbers 0-9. To construct all possible integers, we start with a list of numbers 1-9, and append all valid next-in-line numbers to these numbers, such that we eventually end up with a list `nums` containing all valid integers. 

>Note that the initial starting list starts with range 1-9, as a starting number of 0 would not create a six-number integer.

In general, for every partially constructed integer in `nums`, we append the numbers `j` in `range(num[-1],10)`, to create a new list of integers. The arguments from the `range` function must be such that the numbers inside the integer can never go down. Therefore, the list of possible numbers to add equals the range starting from the last number in the partially constructed integer, up to 9.

When the list reaches a length of 5, then there is an additional condition that we need to take into account. Since the integer must contain a sequence of at least two equal numbers in a row, we force the last number of the six-number integer to be equal to the fifth number, if this condition isn't already true by now. This ensures that there is always a sequence of at least two equal numbers in a row inside the integer. We do this by checking if `len(num) == len(set(num))`. If this condition is true, then all numbers are unique, since a set cannot contain duplicates. If this condition is false, then there is always a sequence of at least 2 equal numbers in a row, since the numbers are ordered from low to high.

```python
nums = [[num] for num in range(1, 10)]
for i in range(5):
    nums_next = []
    for num in nums:
        if len(num) == 5 and len(num) == len(set(num)):
            nums_next.append(num + [num[-1]])
        else:
            for j in range(num[-1],10):
                nums_next.append(num + [j])
    nums = nums_next
```

The only step remaining to find the answer to the first question, is to filter integers that are not within the range given in the input. Since we constructed the integers as a list of numbers, we must first cast the numbers to string type, concatenate these strings, and then cast the answer back to integer. The length of the list of valid integers is the answer to the first question.

```python
nums_joined = [int("".join(map(str, num))) for num in nums]
print(len([num for num in nums_joined if range_min <= num <= range_max]))
```

To find the answer to the second question, we add an additional filter. If we set the numbers of the integer to a dictionary where every number is a key with the amount of times this number is in the integer as value, then we only need to check if the number 2 is contained in the list of values. If this is the case, then the condition is satisfied and we obtain the answer to the second question.

```python
nums_joined = [int("".join(map(str, num))) for num in nums if 2 in {char:num.count(char) for char in num}.values()]
print(len([num for num in nums_joined if range_min <= num <= range_max]))
```