def int_input(prompt='Please enter a number: '):
    while True:
        n = input(prompt)
        try:
            n = int(n)
        except (ValueError, TypeError):
            print('You must enter an integer!')
        else:
            break

    return n

def is_valid_int(n):
    try:
        n = int(n)
    except (ValueError, TypeError):
        return False

    return True

def tell_everyone(players, string):
    for player in players:
        player.tell(string)