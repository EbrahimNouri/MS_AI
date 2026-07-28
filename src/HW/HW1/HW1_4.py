from random import randint

NUMBER_RANGE: int = 20
COUNT_OF_GUES: int = 5


def gues_number(index: int, correct_num: int) -> bool:
    input_str = input(f"{index}- Guess a number between 1 and {NUMBER_RANGE}:\n")
    if not input_str.isdigit():
        print("Invalid input.")
        return gues_number(index, correct_num)

    choice_number = int(input_str)
    if 0 > choice_number > NUMBER_RANGE:
        print("Invalid range.")
        return gues_number(index, correct_num)

    if correct_num < choice_number:
        print("Your guess is too high.")
        return False

    elif correct_num > choice_number:
        print("Your guess is too low.")
        return False

    else:
        print("Correct!")
        return True


if __name__ == "__main__":

    correct_number = randint(1, NUMBER_RANGE)

    for i in range(1, COUNT_OF_GUES + 1):
        guess = gues_number(i, correct_number)

        if guess or i == COUNT_OF_GUES:
            print(f"Correct number is: {correct_number}")
            break
