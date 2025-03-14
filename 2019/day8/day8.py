from pyhelper.pyimport import seperator_to_list
input = seperator_to_list('2019/input/day8_input.txt', cast = int)

img_size = [25, 6]
nums_per_layer = [input[i:i + (img_size[0] * img_size[1])] for i in range(0, len(input), (img_size[0] * img_size[1]))]
zeros_per_layer = [layer.count(0) for layer in nums_per_layer]
layer_least_zeros = zeros_per_layer.index(min(zeros_per_layer))
print(nums_per_layer[layer_least_zeros].count(1) * nums_per_layer[layer_least_zeros].count(2))

img = [2] * (img_size[0] * img_size[1])
for layer in range(len(nums_per_layer)):
    for i_num, num in enumerate(nums_per_layer[layer]):
        if num in (0, 1) and img[i_num] == 2:
            img[i_num] = '#' if num == 1 else ' '
for layer in [img[i:i + img_size[0]] for i in range(0, len(img), img_size[0])]:
    print(layer)