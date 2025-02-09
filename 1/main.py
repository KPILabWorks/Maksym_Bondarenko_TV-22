from itertools import tee

def custom_zip(*iterables):
    iterators = [iter(it) for it in iterables]

    while iterators:
        result = []
        for it in iterators:
            try:
                result.append(next(it))
            except StopIteration:
                return
        yield tuple(result)

list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c']
list3 = [True, False, None, True]

print(list(custom_zip(list1,list2,list3)))
