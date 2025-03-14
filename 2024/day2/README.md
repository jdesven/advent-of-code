[Link to puzzle](https://adventofcode.com/2024/day/2)
## Pre-processing

The data is imported from the input file and formatted into a list of list, where every inner list represents one report.

```python
with open('2024/input/day2_input.txt', 'r') as file:
    nums = [list(map(int,(line))) for line in[row.split(' ') for row in file.read().splitlines()]]
```

## Solution

A report is safe, unless we determine that it is not. 

First we determine if the levels in the report are ascending or descending, by looking at the first two numbers in the report. Then, three checks are done for every level in the report. If any of these conditions hold true, then the whole report is considered unsafe.

1. If the report has ascending levels but it contains a level where the level is higher or equal than the level that follows it, then the report is unsafe.
1. If the report has descending levels but it contains a level where the level is lower or equal than the level that follows it, then the report is unsafe.
3. If the report contains a level where the level differs more than three from the next level, then the report is unsafe.

If none of these conditions apply for any of the levels in the report, then the report is safe.

The answer to the first question is equal to the amount of reports where no unsafe level is found.

```python
def test_if_safe(row):
    asc_desc_factor = 'asc' if row[0] < row[1] else 'desc'
    for j in range(len(row) - 1):
        if (asc_desc_factor == 'asc' and row[j] >= row[j + 1]) \
                or (asc_desc_factor == 'desc' and row[j] <= row[j + 1]) \
                or (abs(row[j] - row[j + 1]) > 3):
            return False
    return True

print(len([row for row in nums if test_if_safe(row) == True]))
```

The answer to the second question uses the test function from question 1. Instead of evaluating the full report itself, we consider all possible reports that would follow from the original report if we remove one level from the report. If any of these altered reports is safe, then the removal of one unsafe level is enough to make the report safe.

When a report is already safe without alterations, then the removal of either the first or last level in the report will never cause the altered report to become unsafe. Hence, we do not need to take already-safe reports into account.

```python
print(len([row for row in nums if len([j for j in range(len(row)) if test_if_safe(row[:j] + row[j+1:]) == True]) > 0]))
```