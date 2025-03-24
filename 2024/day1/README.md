[Link to puzzle](https://adventofcode.com/2024/day/1)
## Pre-processing

We start by importing the data from the source file and fitting this sequence of numbers into a list of rows. We then split this input into a left column and a right column, each creating a list of integers. These lists are then sorted.

```python
from pyhelper.pyimport import lines_to_list_of_list
nums = lines_to_list_of_list("2024\input\day1_input.txt", '   ', int)

nums_left = sorted([row[0] for row in nums])
nums_right = sorted([row[1] for row in nums])
```

## Solution

The answer to the first question is found by summing the differences between the sorted left and right columns.

The answer to the second question is found by summing the products of the left column numbers with the number of times this number appears in the right column, using the `list.count()` function.

```python
print(sum([abs(nums_left[i] - nums_right[i]) for i in range(len(nums))]))

print(sum([nums_left[i] * nums_right.count(nums_left[i]) for i in range(len(nums))]))
```