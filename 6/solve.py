from collections import defaultdict


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
        updateChildren(parent)

    print(sum(values.values()))

if __name__ == "__main__":
    main()
