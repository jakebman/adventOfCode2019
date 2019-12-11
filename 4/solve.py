#

def succeeds(i):
    s = str(i)
    if s != ''.join(sorted(s)):
        return False
    if len(set(s)) == 6:
        return False
    return True


def main():
    # Your puzzle input is 372037-905157.

    count = 0
    for i in range(372037, 905157 + 1):
        if succeeds(i):
            count += 1
    print(count)


if __name__ == "__main__":
    main()
