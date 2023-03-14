from board import Board


def run_tests():
    test_checkwin()


def test_checkwin():
    arrays = [
        [1, 1, 1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [1, 2, 1, 0, 2, 2, 2, 0],
        [1, 2, 1, 2, 2, 2, 2, 0],
        [1, 2, 1, 0, 2, 2, 2, 2],
        [1, 2, 1, 0, 0, 2, 2, 2],
    ]
    win = [True, False, False, True, True, False]

    for i in range(len(arrays)):
        assert win[i] == Board._check_four_in_a_row(arrays[i]), "arrays[{}] is wrong".format(i)