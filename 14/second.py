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


def add_piecewise(need, more, multiple=1):
    out = defaultdict(int, need)
    for chemical, qty in more.items():
        out[chemical] += qty * multiple

    return out


def produce(recipes, chemical, spare=None, initial_guess=1):
    if spare is None:
        spare = {}
    spare = defaultdict(int, spare)

    while initial_guess > 0:
        success, spare = try_generate(recipes, chemical, initial_guess, spare)
        if not success:
            initial_guess //= 2

    return spare


def try_generate(recipes, chemical, qty, spare):
    success = True
    need = defaultdict(int)
    for chem in topo_list(recipes, chemical):
        if chem == chemical:
            # force the production of chemical, even if not needed (so not consumed like needed things are)
            needed = recipes[chem]['yields']
            # First time, just make a lot
            if qty > needed:
                needed = qty
                qty = 0
        else:
            needed = need[chem] - spare[chem]
        if needed <= 0:
            # no need to produce this chemical
            print("Have enough", chem, (need[chem], spare[chem]))
            continue
        elif chem == "ORE":
            success = False
            return success, spare
        yields = recipes[chem]['yields']
        multiplier = ceil(needed / yields)

        more = dict(recipes[chem]['requires'])
        # print(needed, chem, "needs", more, "to be produced")
        more[chem] = -yields  # Now more is balanced per input and output
        need = add_piecewise(need, more, multiplier)
    # If can't fill need, return what we have left over
    for chem in need:
        if need[chem] > spare[chem]:
            success = False

    if success:
        spare = add_piecewise(spare, need, -1)  # subtract
        log_consumed(need, spare)
    return success, spare


def log_consumed(need, spare):
    if True:
        # Include abs on consumed for better formatting
        consumed = {chem: abs(need[chem]) for chem in need if need[chem] > 0}
        produced = {chem: abs(need[chem]) for chem in need if need[chem] < 0}
        print("produced", produced)
        print("consumed", consumed)
        print("have", spare)

    print(spare["ORE"], "Ore left")


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
    ORE_QTY = 1_000_000_000_000
    pprint(produce(recipes, "FUEL", spare={"ORE": ORE_QTY}, initial_guess=ORE_QTY // 143173))


if __name__ == "__main__":
    main()
