def separation(list_, low, high, pivot):
    i = low
    j = low
    pivot_moved_to_end = False
    while j < high:
        if list_[j] < pivot:
            list_[i], list_[j] = list_[j], list_[i]
            i += 1
        elif list_[j] == pivot and pivot_moved_to_end is False:
            list_[j], list_[high] = list_[high], list_[j]
            j -= 1
            pivot_moved_to_end = True
        j += 1

    temp2 = list_[i]
    list_[i] = list_[high]
    list_[high] = temp2
    return i


def pair_up(nuts, bolts, low, high):
    if low < high:
        pivot = separation(nuts, low, high, bolts[high])
        separation(bolts, low, high, nuts[pivot])

        pair_up(nuts, bolts, low, pivot-1)
        pair_up(nuts, bolts, pivot+1, high)


nuts = [1, 3, 4, 5, 2, 6]
bolts = [5, 1, 6, 2, 3, 4]

pair_up(nuts, bolts, 0, 5)

print(nuts)
print(bolts)