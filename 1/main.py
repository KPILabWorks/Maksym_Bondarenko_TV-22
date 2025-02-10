def custom_zip(*iterables, strict=False):
    iterators = [iter(it.items() if isinstance(it, dict) else it) for it in iterables]

    while iterators:
        result = []
        for it in iterators:
            try:
                result.append(next(it))
            except StopIteration:
                if strict:
                    raise ValueError("Found iterables of different sizes")
                return
        yield tuple(result)

list1 = [1, 2, 3, 4, 5]
list2 = ['a', 'b', 'c']
tuple1 = (True, False)
map1 = {'a':1,'b':2}

print(list(custom_zip(list1,list2,tuple1,map1)))
