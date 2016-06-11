#!/usr/bin/env python3

import sys
import os
import make_dudes as md
import time




def main():
    if not(len(sys.argv) == 2):
        print(str(len(sys.argv)))
        eprint("ERROR: usage stats <database_name>")
        sys.exit()
    #connect to database
    try:
        con, cursor = md.connect(sys.argv[1])
    except:
        eprint("ERROR: could not connect to database "+ str(database))
        sys.exit()
    #populate list of players
    dude_list = md.DudeList(con, cursor)
    if dude_list == None:
        con.close()
        sys.exit()
    
    #just add it, if there is no data in table ... stats will all be zero
    dude_list.add_fight_data()
    #dude_list.print_list()
    while (True):
        os.system('clear')
        print("What statistic would you like? Enter number or 'q' for quit \n" \
              "1) Who fought the longest \n" \
              "2) Who fought the shortest \n"\
              "3) Who won the most fights \n"\
              "4) Who lost the most fights \n"\
              "5) Who has the most possible attacks \n"\
              "6) Table of win loss draw by species")
        choice = input()
        if choice == 'q':
            break
        elif choice == '1':
            result = dude_list.longest_total_time()
            for dude in result:
                output = str(dude.name) + " fought for " + str(dude.fight_time) + \
                     " {time}".format(time = 'second' if dude.fight_time == 1 else 'seconds')
                print(output)
        elif choice == '2':
            result = dude_list.shortest_total_time()
            for dude in result:
                output = str(dude.name) + " fought for " + str(dude.fight_time) + \
                     " {time}".format(time = 'second' if dude.fight_time == 1 else 'seconds')
                print(output)
        elif choice == '3':
            result = dude_list.most_wins()
            for dude in result:
                output = str(dude.name) + " won " + str(dude.wins) + \
                     " {num}".format(num = 'fight' if dude.wins == 1 else 'fights')
                print(output)
        elif choice == '4':
            result = dude_list.most_loss()
            for dude in result:
                output = str(dude.name) + " lost " + str(dude.loss) + \
                     " {num}".format(num = 'fight' if dude.loss == 1 else 'fights')
                print(output)
        elif choice == '5':
            result = dude_list.most_attacks()
            for dude in result:
                output = str(dude.name) + " has " + str(len(dude.attack_list)) + \
                     " {num}".format(num = 'attack' if len(dude.attack_list) == 1 else 'attacks')
                print(output)
        elif choice == '6':
            print (' species wins loss tie')
            result = dude_list.win_loss_tie_by_species()
            for thing in result:
                for index in thing:
                    print(str(index), end= ' ')
                print()
            
        print('Enter to continue')
        input()
    
    

if __name__ == "__main__":
    main()
