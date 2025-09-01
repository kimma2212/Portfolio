Readme.txt


By default, it will be the user vs cpu format
player 1 : user
player 2 : cpu (alphabeta cutoff)

+=========================================+
  Input format: coordinate

  alphabet number (without space)
  ex) a3     c5    h1
+=========================================+

If you want to change the player,
Go to main funtion that is placed at the bottom of this code.

Erase comment to choose different evaluation functions.
for example human vs ai:
erase # for player1 = human_player and player2 = ai_player  then comment out every other functions.

    '''
    Player 1
    '''
    #Choose player 1 method
    player1 = human_player                #Played by the user
    #player1 = ai_player                  #Played by the alpha-beta original
 


    '''
    Player 2
    '''
    #Choose player 2 method
    player2 = ai_player                   #Played by original alpha-beta by cpu
    #player2 = human_player               #Played by the user 
    #player2 = better_ai_player           #Played by the better alpha-beta by cpu. Increased depth to 8
    #player2 = weight_ai_player           #Played by the 2nd eval function (weight)
    #player2 = movement_ai_player         #Played by the 3rd eval function (number of possible movement)
    