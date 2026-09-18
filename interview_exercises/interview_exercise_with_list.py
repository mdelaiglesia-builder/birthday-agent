my_list: list[int] = []

def add(number: int):
    my_list.append(number)

def test_add():
    original_len = len(my_list)
    add(4)
    new_len = len(my_list)
    assert 4 in my_list
    assert 5 not in my_list
    assert new_len == original_len + 1

def check(number: int) -> bool:
    print(my_list)
    for a in my_list:
        my_second_list: list[int] = my_list.copy()
        my_second_list.remove(a)
        print(my_second_list)
        for b in my_second_list:
            if a + b == number:
                return True
    return False

def test_check_8():
    global my_list
    my_list = [2,3,5,8,13,21]

    assert check(8) == True

def test_check_9():
    global my_list
    my_list = [2,3,5,8,13,21]
    
    assert check(9) == False

def test_check_4():
    global my_list
    my_list = [2]
    
    assert check(4) == False