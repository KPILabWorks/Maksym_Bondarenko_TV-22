def custom_zip(*iterables, strict=False):
    iterators = [iter(it) for it in iterables]

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
list3 = [True, False, None, True]

print(list(custom_zip(list1,list2,list3, strict=True)))
