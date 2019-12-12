from collections import defaultdict

SAN = "SAN"

YOU = "YOU"


def main():
    parents = {}
    children = defaultdict(list)
    values = {"COM": 0}  # initial condition

    def updateChildren(parent):
        if parent in values:
            for child in children[parent]:
                if child not in values:
                    values[child] = values[parent] + 1
                    print(child, "orbits", parent, "with total length", values[child])
                    updateChildren(child)

    for line in open("input.txt").readlines():
        parent, child = line.strip().split(")")
        children[parent].append(child)
        parents[child] = parent
        updateChildren(parent)

    def ancestors(child):
        while child in parents:
            child = parents[child]
            yield child

    def commonParent(a, b):
        commons = set(ancestors(a)).intersection(set(ancestors(b)))
        common = max(commons, key=values.get)
        return common

    common =commonParent(YOU, SAN)
    me = (values[YOU] - values[common] - 1)
    santa = (values[SAN] - values[common] - 1)
    distance = me + santa
    print("I need", me, "transfers to orbit", common, "and Santa needs", santa, "transfers")
    print(distance, "total transfers")


if __name__ == "__main__":
    main()
