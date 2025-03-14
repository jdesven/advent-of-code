[Link to puzzle](https://adventofcode.com/2024/day/13)
## Pre-processing

We import the `.txt` file as a string and isolate the numerical information using [regular expressions](https://en.wikipedia.org/wiki/Regular_expression). We then store the information in lists for the A buttons, the B buttons and the prize locations, by using the fact that this information is present on every first, second and third row out of every four rows, respectively.

```python
import re

with open('2024/input/day13_input.txt', 'r') as file:
    txt = file.read().splitlines()
button_a = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[0::4]]]
button_b = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[1::4]]]
prizes = [[int(row.split(',')[0]), int(row.split(',')[1])] for row in [re.sub(r'[^0-9,]','',row) for row in txt[2::4]]]
```

## Solution

For every claw machine, the A button moves the claw by $(a_X,a_Y)$, while the B button moves the claw by $(b_X,b_Y)$. The prize is located at $(p_X,p_Y)$. The parameters $a_X$, $a_Y$, $b_X$, $b_Y$, $p_X$, and $p_Y$ are known parameters from the input file. If we represent the number of times we press the A button and B button as $T_A$ and $T_B$, respectively, the problem becomes [a system of linear equations](https://en.wikipedia.org/wiki/System_of_linear_equations) with two unknowns.

$$
\begin{aligned}
a_XT_A+b_XT_B=p_X \\
a_YT_A+b_YT_B=p_Y
\end{aligned}
$$

The solution to either linear equation can be rewritten as $T_A=-bT_B/a+p/a$, which forms a linear line in $(T_A,T_B)$ space. The solution(s) to the full system of equations thus equal the point(s) where these lines intersect. Since both lines are linear, [there can only be 0, 1, or infinitely many intersection points](https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection). However, since all constants and unknowns in the system are in $\mathbb{R}_{>0}$ (positive, non-zero integers), $T_A$ cannot surpass $p_X/a_X$, or the claw will overshoot $p_X$. Since there is a finite amount of integers between 1 and $p_X/a_X$, an infinite amount of solutions can never occur. This ensures that any claw machine with a solution, has one and only one solution. As a result, we will not have to test which solution has the lowest token cost (even though the puzzle text implies otherwise).

The system of linear equations can be written in matrix multiplication form $A\bf{T}=\bf{p}$, where $A$ is the matrix representation of $a_i$ and $b_i$, $\bf{T}$ the column vector representation of $T_i$, and $\bf{p}$ the column vector representation of $p_i$. If $A_i$ is the matrix formed by replacing the $i$-th column of $A$ by the column vector $\bf{p}$, then [Cramer's theorem](https://en.wikipedia.org/wiki/Cramer%27s_rule) states that the solutions to the system of linear equations can be calculated from the [determinants](https://en.wikipedia.org/wiki/Determinant) of the matrices $A$ and $A_i$.

$$T_i = \frac{\det(A_i)}{\det(A)}$$

The solution to $T_i$ must be a positive integer, so the solution is only valid when the [modulo](https://en.wikipedia.org/wiki/Modulo) of $det(A_i)$ to $det(A)$ equals 0 (i.e. the integer division $det(A_i)/det(A)$ does not leave a remainder). If this condition holds true, we have the one and only solution to the system of linear equations.

Implementing this in Python, we obtain the following.

```python
def calc_tokens(button_a, button_b, prizes):
    tokens = 0
    for i in range(len(prizes)):
        det_A = button_a[i][0] * button_b[i][1] - button_b[i][0] * button_a[i][1]
        det_A1 = prizes[i][0] * button_b[i][1] - button_b[i][0] * prizes[i][1]
        det_A2 = button_a[i][0] * prizes[i][1] - prizes[i][0] * button_a[i][1]
        if det_A1 % det_A == 0 and det_A2 % det_A == 0:
            tokens += 3 * int(det_A1 / det_A) + int(det_A2 / det_A)
    return tokens
print(calc_tokens(button_a, button_b, prizes))
```

The second part of the problem is calculated using the same method. The only adjustment here is a $10^{13}$ x $10^{13}$ translation of the prize locations.

```python
prizes_translated = [[num + 1e13 for num in prize] for prize in prizes]
print(calc_tokens(button_a, button_b, prizes_translated))
```