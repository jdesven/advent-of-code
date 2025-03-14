from pyhelper.pyimport import lines_to_list_of_list
from math import ceil
input = lines_to_list_of_list('2019/input/day14_input.txt', seperator = ' ', regex = '[0-9A-Z ]')
recipes = {recipe[-1]: [int(recipe[-2])] + [(int(recipe[i]), recipe[i + 1]) for i in range(0, len(recipe) - 2, 2)] for recipe in input}

def calc_requirements(end_product,amount_end_product):
    def calc_recipe(end_product = end_product,amount_end_product = amount_end_product):
        end_product_stashed = stash.get(end_product) if end_product in stash else 0
        ore_needed = 0
        times_recipe_needed = ceil(((amount_end_product - end_product_stashed)) / recipes[end_product][0])
        stash[end_product] = (recipes[end_product][0] * times_recipe_needed + end_product_stashed) - amount_end_product
        for (begin_product_amount, begin_product) in recipes[end_product][1:]:
            if begin_product == 'ORE':
                ore_needed += begin_product_amount * times_recipe_needed
            else:
                ore_needed += calc_recipe(begin_product, begin_product_amount * times_recipe_needed)
        return ore_needed
    stash = {}
    return calc_recipe(end_product, amount_end_product)

ore_for_one_fuel = calc_requirements('FUEL', 1)
print(ore_for_one_fuel)

max_fuel = int(1e12 / ore_for_one_fuel)
ore_needed = calc_requirements('FUEL', max_fuel)
while ore_needed <= 1e12:
    prev_max_fuel = max_fuel
    max_fuel = int(1e12 / ore_needed * max_fuel)
    if max_fuel <= prev_max_fuel:
        max_fuel = prev_max_fuel + 1
    ore_needed = calc_requirements('FUEL', max_fuel)
print(prev_max_fuel)