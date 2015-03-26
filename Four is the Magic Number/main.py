from sys import argv
import inflect

eng = inflect.engine()
current_word = eng.number_to_words(argv[1])
n = 0
temp = 0
while temp != 4:
    temp = len(current_word)
    print("We are at depth {0}\n{1} is the current word with a length of {2}".format(n, current_word, temp))
    current_word = eng.number_to_words(temp)
    n += 1
print("We have reached four at a depth of {0}".format(n))
exit(0)
