from random import randint
import requests




class HangedMan():
    words = ['fiton', 'jackson','zurita','eeeee','one']
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"


    
    def __init__(self):        
        self.connectedUsernames = []   
        response = requests.get(self.word_site)
        self.WORDS = response.content.splitlines()
        self.__setup()
            
    
    def __setup(self):
        # self.hiddenWord = str(self.WORDS[randint(0,len(self.WORDS)-1)])[1:]
        self.hiddenWord = (self.WORDS[randint(0,len(self.WORDS)-1)]).decode('utf-8')
        while len(self.hiddenWord) > 7:
            self.hiddenWord = (self.WORDS[randint(0,len(self.WORDS)-1)]).decode('utf-8')
        self.currentWord = self.__get_format_hidden_word()
        self.currentUserIndex = 0
            
    def __get_format_hidden_word(self):
        res = ''
        for char in self.hiddenWord:
            if char != ' ':
                res += '-'
            else:
                res += ' '
        return res
    
    def addUsername(self, username):                    
        if username not in self.connectedUsernames:
            self.connectedUsernames.append(username)
        
    def removeUsername(self, username):
        self.connectedUsernames.remove(username)
        if len(self.connectedUsernames) == 0:
            self.__setup()
        else:
            self.__nextPlayer()
            
    
    # Debug
    def hword(self):
        return self.hiddenWord
    
    def cword(self):
        return self.currentWord
    
    def usernames(self):
        return self.connectedUsernames
    
    def canPlay(self, username):
        return self.connectedUsernames[self.currentUserIndex] == username
    
    def currentUser(self):
        return self.connectedUsernames[self.currentUserIndex]
    
    def guessLetter(self, letter):
        guessResult = False
        # Asegurar que sea solo uh caracter
        lstring = list(self.currentWord)
        if len(lstring) != 0 and letter in self.hiddenWord and letter not in self.currentWord:            
            letter = letter[0]
            # Revelar la letra en currentWord
            for i in range(len(self.hiddenWord)):
                if self.hiddenWord[i] == letter:
                    lstring[i] = letter
                    
            guessResult = True
            self.currentWord = ''.join(lstring)
        else:
            self.__nextPlayer()
        return guessResult
    
    def guessWord(self, word):
        guessResult = False
        if word == self.hiddenWord:                    
            guessResult = True
            self.currentWord = self.hiddenWord
        else:
            self.__nextPlayer()
        return guessResult
            
    def __nextPlayer(self):
        self.currentUserIndex = (self.currentUserIndex + 1) % len(self.connectedUsernames)
    
    def checkIfSolved(self):
        gameSolved = '-' not in self.currentWord
        
        if gameSolved:
            self.__setup()
        
        return gameSolved