#!/usr/bin/env python3

import psycopg2
import sys
from make_dudes import eprint
import make_dudes as md





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
    
    #make sure fight data is empty ...annnnddd FIIIIIGGGHT
    dude_list.check_fight()
    dude_list.ultimate_showdown_of_ultimate_destiny()

	#cleanup
    con.commit()
    con.close()
    

if __name__ == "__main__":
    main()
