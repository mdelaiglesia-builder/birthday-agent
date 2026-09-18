import threading

my_dict: dict[int,int] = {}

lock: threading.Lock = threading.Lock()

def add(number: int):
    global my_dict
    with lock:
        if my_dict.get(number) is None:
            my_dict[number] = 1
        else:
            my_dict[number] = my_dict[number] + 1

def test_add_4_two_times():
    global my_dict
    add(4)
    add(4)
    assert 4 in my_dict
    assert my_dict[4] == 2
    assert 5 not in my_dict
    
def check(number: int) -> bool:
    global my_dict
    with lock:
        for a in my_dict:
            b = number - a
            if (my_dict.get(b) is not None):
                print(f"{a}: {b}")              
                if (b != a):
                    print(f"{a} distinct from {b}")  
                    return True
                elif (my_dict.get(b) > 1):
                    print(f"{b} > 1")
                    return True
        return False

def test_check_8():
    global my_dict
    my_dict = {2: 2, 3: 1, 5: 1, 8: 1, 13: 1, 21: 1}
    print(my_dict)
    assert check(8)

def test_check_4():
    global my_dict
    my_dict = {2: 2, 3: 1, 5: 1, 8: 1, 13: 1, 21: 1}
    print(my_dict)
    assert check(4)

def test_check_6_false():
    global my_dict
    my_dict = {2: 2, 3: 1, 5: 1, 8: 1, 13: 1, 21: 1}
    print(my_dict)
    assert check(6) is False

def test_check_6_extra():
    global my_dict
    my_dict = {3: 1, 1: 1, 5: 1}
    print(my_dict)
    assert check(6)