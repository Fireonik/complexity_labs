def is_cyclic_displacement(tested_string, seeked_pattern):
    if len(tested_string) != len(seeked_pattern):
        return False

    test_string = tested_string * 2
    for i in range(len(tested_string)):  # direct comparison operation executes <= n times
        if test_string[i:i+len(seeked_pattern)] == seeked_pattern:
            return True

    return False


T_star = 'abc'
T = 'cab'
print(is_cyclic_displacement(T, T_star))
