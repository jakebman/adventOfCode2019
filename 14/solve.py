from collections import defaultdict
from math import ceil
from pprint import pprint
from re import compile
from functools import reduce, partial, cmp_to_key


def parseLine(line, regex=compile("(\\d+) (\\w+)")):
    ingredients = regex.findall(line)
    return ingredients


def transitive_reqs(recipes, item_or_key):
    if type(item_or_key) is str:
        item = recipes[item_or_key]
    else:
        item = item_or_key
    if "transitive" not in item:
        item['direct'] = set(item['requires'].keys())
        item["transitive"] = reduce(set.union,
                                    (item['direct'], *map(lambda x: transitive_reqs(recipes, x), item['direct']),),
                                    set())

    print("Transitive dependencies of", item_or_key, "are", item['transitive'])
    return item["transitive"]


def produce_with_given(recipes, chemical, qty, given=None):
    if given is None:
        given = defaultdict(int)
    if chemical is "ORE":
        given["ORE"] += qty
        return
    needed = recipes[chemical]
    if given[chemical] >= qty:
        given[chemical] -= qty
        return


def topo_list_(recipes, chemical):
    yield chemical
    recipe = recipes[chemical]


def topo_cmp(recipes, a, b):
    # TODO: transitive now includes direct. The check for direct is now likely redundant
    if a in recipes[b]['direct'] or a in recipes[b]['transitive']:
        return -1
    elif b in recipes[a]['direct'] or b in recipes[a]['transitive']:
        return 1
    return len(recipes[a]['transitive']) - len(recipes[b]['transitive'])


def topo_list(recipes, chemical):
    # TODO: transitive now includes direct. The addition of direct is now likely redundant
    needed = {chemical, *recipes[chemical]['direct'], *recipes[chemical]['transitive']}
    l = list(needed)
    l.sort(key=cmp_to_key(partial(topo_cmp, recipes)))
    return l[::-1]


def add_need(need, more, multiple=1):
    for chemical, qty in more.items():
        need[chemical] += qty * multiple


def produce(recipes, chemical, qty):
    need = defaultdict(int, {chemical: qty})
    filled = defaultdict(int)
    process_order = topo_list(recipes, chemical)
    for chemical in process_order:
        if chemical not in need:
            print("Broken at", chemical, "-", "don't need it, for some reason")
            # exit(-1)
        needed = need[chemical]
        yields = recipes[chemical]['yields']
        multiplier = ceil(needed / yields)
        if not multiplier:
            print("Broken at", chemical, "-", "needed", needed, "yield", yields)
            exit(-1)
        more = recipes[chemical]['requires']

        print(chemical, "needs", more, "to be produced")
        add_need(need, more, multiplier)
        filled[chemical] = yields * multiplier
    return need, filled


def main():
    recipes = {"ORE": {"transitive": set(), "direct": set(), "yields": 1, "requires": dict()}}
    for equation in map(parseLine, map(str.strip, list(open("input.txt").readlines()))):
        product = equation[-1]
        requires = {}
        for ingredient in equation[:-1]:
            requires[ingredient[1]] = int(ingredient[0])
        recipes[product[1]] = {'yields': int(product[0]),
                               'requires': requires}
    print(len(recipes), "recipes")

    # don't need the value, just pre-calculating
    transitive_reqs(recipes, "FUEL")
    for key, value in recipes.items():
        if 'transitive' not in value:
            print("Didn't need", key, "for FUEL")
            transitive_reqs(recipes, value)

    print(recipes["FUEL"])
    print(topo_list(recipes, "ORE"))
    print(topo_list(recipes, "FUEL"))
    need, filled = produce(recipes, "FUEL", 1)
    pprint((need, filled))
    print("Used", filled['ORE'], "ORE to create", 1, "FUEL")


if __name__ == "__main__":
    main()
