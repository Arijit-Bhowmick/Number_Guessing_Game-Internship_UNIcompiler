#!/bin/bash

from os import system
import sys
import random

class NumberGuessing:
    
    def __init__(self, min_random_initial=1, max_random_final=10):
        '''
        Defines Predefined Data to be assigned
        on each run
        '''

        # Score cannot be negative
        # score frequency increases with each level
        # Example: On Completing Level 1 | Score Provided = 1
        #          On Completing Level 2 | Score Provided += 2
        # But On revealing hints, Score is reduced by 1

        self.score = 0
        self.total_hint_used = 0
        self.min_random_initial = min_random_initial
        self.max_random_final = max_random_final
        self.current_level = 1
        self.platform = sys.platform
        
    def clearScreen(self):
        '''
        Clear Screen for next input
        '''

        if self.platform=='linux':
            system('clear')
        elif self.platform.startswith('win'):
            system('cls')

    def currentScore(self):
        '''
        Get the Current Score of the user
        '''
    def randomNumber(self, initial=1, final=10):
        '''
        Random Number to use during each stage
        of the game
        '''
        return random.randint(initial, final)

    def levelSetup(self):
        '''
        Setup Level for the game
        '''

        self.hint_used_per_level = 0
        self.guessed_numbers = []

        random_initial = random.randint(self.min_random_initial, self.max_random_final)
        random_final = random.randint(random_initial, self.max_random_final)

        # random_number => to be used for number guessing
        self.random_number = self.randomNumber(random_initial, random_final)
        print(self.random_number)
        # Hints Setup
        self.all_hints = ''

        self.total_hint_types = 7
        self.hint_types = [i for i in range(self.total_hint_types)]
        self.get_hint = GenerateHint(self.random_number)

        self.clearScreen()



    def guess(self):
        '''
        Function For Guess algorithm
        '''

        # self.guessed_number = int(input("Guess the Number\n==> "))
        self.guessed_number = int(input(f'''
{"-"*50}\nLevel {self.current_level}\n{"-"*50}

Hint Count : {self.hint_used_per_level}
Total Hint Count : {self.total_hint_used}
Score : {self.score}

{"-"*50}
--- REVEALED HINTS ---

{self.all_hints}
{"-"*50}
Checked Numbers : {str(self.guessed_numbers)[1:-1]}
{"-"*50}

Guess the Number\n==> '''))

        self.clearScreen()

        if self.guessed_number not in self.guessed_numbers:
            self.guessed_numbers.append(self.guessed_number)


        # Checks For guesses

        if self.guessed_number==self.random_number:
            self.score+=self.current_level
            self.current_level+=1

            input(f"""
{"-"*50}\n!!! Congratulations, You Got it !!!\n{"-"*50}

{"-"*50}
Score : {self.score}
You have used {self.hint_used_per_level} Hints in this Level
Total Hints used : {self.total_hint_used}
Checked Numbers : {str(self.guessed_numbers)[1:-1]}
{"-"*50}

Moving to Level {self.current_level} ... :)

--- PRESS ENTER TO CONTINUE ---
!!! PRESS CTRL^C TO EXIT !!!
""")
            self.levelSetup()

        else:
            print("): INCORRECT GUESS :(")
            if self.score==0:
                pass
            else:
                self.score-=1
            self.hint()

    def hint(self):
        '''
        Generate Hint Data to be used
        when the user makes a wrong guess
        '''

        if self.hint_types==[]:
            if self.guessed_number>self.random_number:
                hint_desc =  f"The Random Number is an Less than {self.guessed_number}"
            elif self.guessed_number<self.random_number:
                hint_desc =  f"The Random Number is an Greater than {self.guessed_number}"
        else:
            current_hint_type_num = random.choice(self.hint_types)
            
            if current_hint_type_num == 0:
                hint_desc = self.get_hint.evenOddCheck()
            elif current_hint_type_num == 1:
                hint_desc = self.get_hint.primeCheck()
            elif current_hint_type_num == 2:
                hint_desc = self.get_hint.nearestGreaterThanValue()
            elif current_hint_type_num == 3:
                hint_desc = self.get_hint.nearestLowerThanValue()
            elif current_hint_type_num == 4:
                if 1 in self.hint_types:
                    current_hint_type_num = 1
                hint_desc = self.get_hint.multipleValue()
            elif current_hint_type_num == 5:
                if 1 in self.hint_types:
                    current_hint_type_num = 1
                hint_desc = self.get_hint.divisibleValue()
            elif current_hint_type_num == 6:
                hint_desc = self.get_hint.numberLength()
            
            self.hint_types.remove(current_hint_type_num)
        # print(self.hint_types)

        self.hint_used_per_level+=1
        self.all_hints+=f'[{self.hint_used_per_level}] {hint_desc}\n'


            
        self.total_hint_used+=1
        return self.all_hints

class GenerateHint:
    '''
    Functions available to be used during
    Hint Generation
    '''
    def __init__(self, number):
        '''
        Defines Predefined Data to be assigned
        on each run
        '''
        self.number = number
        self.is_prime=None
        self.multiple_of = 1

    def evenOddCheck(self):
        '''
        Check if the number is Even or Odd
        '''
        if self.number%2==0:
            return "The Random Number is an Even Number"
        else:
            return "The Random Number is an Odd Number"

    def primeCheck(self):
        '''
        Check if the number is a Prime Number
        '''
        if self.number == 1:
            self.is_prime = False
            return "The Random Number is not a Prime Number"
        
        i = 2
        while i*i <= self.number:
            if self.number % i == 0:
                self.is_prime = False
                self.multiple_of = i
                return "The Random Number is not a Prime Number"
            i += 1
        self.is_prime = True
        return "The Random Number is a Prime Number"

    def nearestGreaterThanValue(self):
        '''
        Shows Nearest lower value of the Random Number
        '''
        return f"Random Number is Smaller than {random.randint(self.number+1, self.number+100)}"

    def nearestLowerThanValue(self):
        '''
        Shows Nearest Higher value of the Random Number
        '''
        return f"Random Number is Greater than {random.randint(1, self.number-1)}"

    def multipleValue(self):
        '''
        Shows Multiple of the Number
        '''
        if self.is_prime==None:
            return self.primeCheck()
        else:
            return f"The Random Number is a multiple of {self.multiple_of}"

    def divisibleValue(self):
        '''
        Shows Divisible of the Number
        '''
        if self.is_prime==None:
            return self.primeCheck()
        else:
            return f"The Random Number is divisible by {self.multiple_of}"

    def numberLength(self):
        '''
        Returns The Length of the Number
        '''

        return f"The Random Number has {len(str(self.number))} Digits"
        
            



game = NumberGuessing(1, 1000) # Change Random Number Range for Difficulty Level

# Generate First Level
game.levelSetup()

while True:
    try:
        game.guess()
    except KeyboardInterrupt:
        print("\nThankYou For Using :)")
        sys.exit()