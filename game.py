import mysql.connector as sql
import random


def canvas1(word):
    wordLc = list(word)
    canvas = list('_' * len(word))
    noLetters = len(word) // 4
    for i in range(noLetters):
        char = random.choice(word)
        while wordLc.count(char) != 0:
            x = wordLc.index(char)
            canvas[x] = char
            wordLc[x] = ''
    return canvas


def guess(wordL, g):
    if g in wordL:
        return True
    else:
        return False




database = sql.connect(host = "localhost", user = "root", passwd = "", database = "Hangman")

if database.is_connected():
    print("Succesfully connected")

cursor = database.cursor()

Name = input("Enter your name")

print('\n\n', "HELLO", Name, "Do you think you can win me ? HAHAHA.... Try answering but don't expect to get them all !")

streak = True
score = 0
randint = 1
while streak == True:

    
    query = "SELECT Answer, Riddle FROM main WHERE ID = " + str(randint)

    cursor.execute(query)

    lol = cursor.fetchall()
    dataset = lol[0]

    word = dataset[0]
    hint = dataset[1]


    wordL = list(word)
    canvas = canvas1(wordL)
    print(*canvas)
    print("Hint :",hint)
    for i in range(4):
        g = input("What is your guess ? ")
        if guess(wordL, g):
            while wordL.count(g) != 0:
                x = wordL.index(g)
                canvas[x] = g
                wordL[x] = ''
            print(*canvas)
            print(3 - i, 'chances left')
        elif g == word:
            print("CORRECT\n\n")
            score+=1
            if randint == 10:
                print("YOU WON !!!")
                streak = False
            break
        else:
            print("INCORRECT")
            print(3 - i, 'chances left')
            print(*canvas)
        if canvas == list(word):
            print("Correct\n\n")
            score += 1
            if randint == 10:
                print("YOU WON !!!")
                streak = False
            break
    else:
        print("The word is:-- ", word)
        print("Your score is", score,"\n\n")
        streak = False
    randint += 1
   
    


query2 = "INSERT INTO leaderboard (Name, Score) values('"+ Name+"'," +str(score)+")"
cursor.execute(query2)
database.commit()

query3 = "select * from leaderboard order by Score DESC"
cursor.execute(query3)

lol = cursor.fetchall()

print("\t 𝙇𝙚𝙖𝙙𝙚𝙧𝙗𝙤𝙖𝙧𝙙")
rank = 1
for i in lol:
    print(rank,i[0],"\t", i[1])
    rank+=1

cursor.close()
