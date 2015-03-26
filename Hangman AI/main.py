from collections import Counter
import re
import sys


class hangman():
    def __init__(self, word, guesses):
        self.guesses = guesses
        self.word = word
        self.wordlen = len(word)
        self.guess_state = ['' for x in range(len(word))] # initialzed the current information about known letters and their locations

    def guess_word(self, word):
        return word == self.word

    def guess_letters(self, letter):
        self.guesses -= 1
        if letter not in self.word:
            return False
        for i in enumerate(self.word):
            if letter is i[1]:
                self.guess_state[i[0]] = letter
        return True



def dict_char_freq(dict):
    """
    :argument dictionary name
    :return list of character frequencies in des order
    """
    with open(dict, 'r') as f:
        raw_data = f.read()
        new_data = re.sub('\n|-', '', raw_data).lower()
        return [x[0] for x in Counter(new_data).most_common()]


def dict_words(dict):
    """
    :argument dictionary name
    :return list of words
    """
    with open(dict, 'r') as f:
        raw_data = f.read()
        new_data = [x.strip().lower() for x in raw_data.splitlines()]
        return new_data



def letter_check(w1, w2):
    """
    :argument w1 list of chars
    :argument w2 is a word i.e a list of chars, but one we are checking against
    :return bolean
    Basically, checks if a word has any words in a list of words. This is useful for pairing down the dictionary
    """
    for x in w2:
        if x in w1:
            return False
    return True


class hangman_ai():
    def __init__(self, game, dict):
        self.game = game
        self.guessed = []
        self.vowels = ['e','t','a','o','i','u']
        self.guessed_wrong = []
        self.diction = [x for x in dict_words(dict) if len(x) is self.game.wordlen] # initalize the AI's diction based on word length

    def calc_word_freq(self):
        """
        If a vowel has not been guessed, guess a vowel. If one has...
        Calculates the character frequencies based on the dictionary - the letters that have already been guessed
        """

        if self.guessed == self.guessed_wrong:
            return [x for x in self.vowels if x not in self.guessed]
        else:
            return [x[0] for x in Counter(((''.join(self.diction)).lower())).most_common() if x[0] not in self.guessed]
        #self.vowel_word_freq = []

    def diction_update(self):
        """Updates the dictionary to reflect all info about a word, the chars in it and their positions"""
        state = self.game.guess_state
        not_allowed = self.guessed_wrong
        res = []
        for x in state:
            if x is '':
                res.append('.')
            if x is not '':
                res.append(x)
        res1 = ''.join(res)
        self.diction = [x for x in self.diction if re.match(res1, x) is not None and letter_check(x, not_allowed) ]
    def guess(self, c):
        """Guesses a char and updates the relevant variables"""
        self.guessed.append(c)
        isin = self.game.guess_letters(c)
        if not isin:
            self.guessed_wrong.append(c)
    def play(self):
        """Continues to guess char/update the diction based on these guesses until it runs out of turns or wins """
        if len(self.diction) is 1:
            print("Possible victory")
            guess = self.diction[0]
            test = self.game.guess_word(guess)
            if test:
                print("VICTORY!!")
                return True

            print("Catastropic Failure 3")
            print("Trying something new")
            return False

        state = ''.join(self.game.guess_state)
        if len(state) is self.game.wordlen:
            print("Possible victory")
            test = self.game.guess_word(''.join(self.game.guess_state))
            if test:
                print("VICTORY!")
                return True
            print("Catastrophic Failure 1")
            return False
        print(self.game.guesses)
        if self.game.guesses == 0:
            print("Catastrophic Failure 2")
            return False
        self.diction_update()
        guess = self.calc_word_freq()
        try:
            c = guess[0]
        except IndexError:
            print("Catastrophic Failure 3")
            return False
        print(c)
        self.guess(c)
        return self.play()



def play_hangman(word, turns, dict):
    game = hangman(word, turns)
    ai = hangman_ai(game, dict)
    return ai.play()

def mass_test():
    """Runs the hangman game on everyword in the dictionary"""
    all_words = dict_words('dict.txt')
    results = []
    try:
        for x in all_words:
            print('Trying: ', x)
            results.append(play_hangman(x, 10, 'dict.txt'))
    except KeyboardInterrupt:
        print('Interrupted, calculating results')
        success_percent = 100 * len([x for x in results if x is True]) / len(results)
        failure_percent = 100 * len([x for x in results if x is False]) / len(results)
        print('The program succeeded {0}% of the time and failed {1}% of the time.'.format(success_percent, failure_percent))
        sys.exit(127)

    success_percent = 100 * len([x for x in results if x is True]) / len(results)
    failure_percent = 100 * len([x for x in results if x is False]) / len(results)
    print('The program succeeded {0}% of the time and failed {1}% of the time.'.format(success_percent, failure_percent))

mass_test()
#play_hangman('global', 10, 'dict.txt')