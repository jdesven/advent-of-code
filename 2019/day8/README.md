[Link to puzzle](https://adventofcode.com/2019/day/8)
## Import

```python
from pyhelper.pyimport import seperator_to_list
input = seperator_to_list('2019/input/day8_input.txt', cast = int)
```

## Solution

We seperate the layers into the nested list `nums_per_layer`, such that every element of `nums_per_layer` represents one layer. Then, for every layer we count the number of zeros and store this in `zeros_per_layer`. We then find the index of the layer with the least amount of zeros `layer_least_zeros` and multiplicate the amount of ones with the amount of twos in this layer. This equals the answer to the first question.

```python
img_size = [25, 6]
nums_per_layer = [input[i:i + (img_size[0] * img_size[1])] for i in range(0, len(input), (img_size[0] * img_size[1]))]
zeros_per_layer = [layer.count(0) for layer in nums_per_layer]
layer_least_zeros = zeros_per_layer.index(min(zeros_per_layer))
print(nums_per_layer[layer_least_zeros].count(1) * nums_per_layer[layer_least_zeros].count(2))
```

We start by filling the image `img` with transparent pixels (2). Then, for every layer `layer`, we check if there any pixels `num` that are non-transparent in `layer`, yet still transparent in `img`. If so, we overwrite this pixel in `img`. After checking every layer, we print this image to the console to find the answer to the second question.

```python
img = [2] * (img_size[0] * img_size[1])
for layer in range(len(nums_per_layer)):
    for i_num, num in enumerate(nums_per_layer[layer]):
        if num in (0, 1) and img[i_num] == 2:
            img[i_num] = '#' if num == 1 else ' '
for layer in [img[i:i + img_size[0]] for i in range(0, len(img), img_size[0])]:
    print(layer)
```