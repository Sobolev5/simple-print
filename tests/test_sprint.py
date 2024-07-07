from simple_print import sprint


def test_sprint():
    """Test sprint.

    Run:
        pytest tests/test_sprint.py -s
    """

    # common
    types = (
        1,
        "yoda",
        (1,),
        [1],
        {1: 1},
        {1},
        True,
        None,
        lambda x: x,
        (x for x in range(2)),
        type,
    )
    print(*types)

    for i, case in enumerate(types):
        print("\n")
        print("*" * 30, type(case), "*" * 30)
        if i < 1:
            case_1 = "multi arg example"
            sprint(case, case_1)
        sprint(case)
        sprint(case, c="green", i=i)
        sprint(case, c="blue", b="on_white")
        sprint(case, c="blue", b="on_white", a="underline")
        sprint(case, c="blue", b="on_white", a="bold", p=True)
        my_string = sprint(case, s=True)
        print(my_string)
        my_string = sprint(case, s=True, p=True)
        print(my_string)

    # f string
    some_var = "some_value"
    sprint(f"some_var={some_var}")

    # format
    some_var = "some_value"
    sprint("some_var={}".format(some_var))

    # %
    some_var = "some_value"
    sprint("some_var=%s" % some_var)

    # README.md case
    print("\n\n")
    master = "yoda"
    sprint(master)
    sprint(
        master, c="magenta"
    )  # colors: grey, red, green, yellow, blue, magenta, cyan, white.
    sprint(
        master, c="white", b="on_blue"
    )  # backgrounds: on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan
    sprint(
        master, c="white", b="on_green", a="underline"
    )  # attributes: bold, dark, underline, blink, reverse, concealed
    sprint(master, c="blue", b="on_white", a="bold", p=True)  #
    my_string = sprint(master, s=True)  # return as string
    my_string = sprint(master, s=True, p=True)  # return as string with path to file

    # stderr
    print("\n\n")
    sprint("print to stderr", stream="stderr")

    # indent
    print("\n\n")
    fruits = ["lemon", "orange", "banana"]
    sprint(fruits, c="green")

    for fruit in fruits:
        sprint(fruit, c="yellow", i=4, p=1)
