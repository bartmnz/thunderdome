#!/usr/bin/env python3

import psycopg2
import sys
import getpass
from make_dudes import eprint

def eprint(*args, **kwargs):
	print(*args, file=sys.stderr, **kwargs)

def main():
	if not (len(sys.argv) == 2):
		eprint("ERROR: usage reset <database_name>")
		sys.exit()
	
	try:
		u_name = getpass.getuser()
		connect_line = "dbname=" + str(sys.argv[1]) + " user=" + u_name
		con = psycopg2.connect(connect_line)
		cursor = con.cursor()
	except:
		eprint("ERROR: could not connect to database " + str(sys.argv[1]))
	cursor.execute('DELETE from fight')
	con.commit()
	con.close()
	


if __name__ == "__main__":
	main()
