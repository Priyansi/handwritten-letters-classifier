def test():
    return "'"+"','". join(chr(i) for i in range(97, 123))+"'"


print(test())
