from wonderwords import RandomWord

r = RandomWord()

cur_word = r.word(word_min_length=3, word_max_length=5)
true_guess = "-" * len(cur_word)
# print(cur_word)
print(true_guess)
health = 6

while health > 0:
    user_input = input("Enter a character: ").lower()
    if len(user_input) != 1:
        print("Please enter a single character")
        continue
    if user_input not in cur_word:
        print("your guess is not in the word")
        health -= 1
        print(true_guess)
        continue

    indices = [i for i, char in enumerate(cur_word) if char == user_input]
    for induce in indices:
        true_guess = true_guess[:induce] + user_input + true_guess[induce + 1 :]

    if true_guess == cur_word:
        print("You won!")
        print(true_guess)
        break

    print("Correct!")
    print(true_guess)
