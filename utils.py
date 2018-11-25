def int_input(prompt='Please enter a number: '):
    while True:
        n = input(prompt)
        try:
            n = int(n)
        except ValueError:
            print('You must enter an integer!')
        else:
            break

    return n