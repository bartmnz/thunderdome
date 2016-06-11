from __future__ import print_function
import psycopg2
import sys
import random
import getpass #for getting username
import datetime

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

class Attack:
    def __init__(self, *args):
        if not len(*args) == 5:
            raise AttributeError
        self.name = args[0][0]
        self.atk_type = args[0][1]
        try:
            self.min_dmg = int(args[0][2])
            self.max_dmg = int(args[0][3])
            self.speed = args[0][4]
            self.speed = self.speed.total_seconds()
        except:
            raise ValueError
        


class Dude:
    def __init__(self, *args):

        if not len(*args) == 6:
            raise AttributeError
        self.attack_list = [] 
        self.my_id = args[0][0]
        self.name = args[0][1]
        self.atk_timer = 0
        self.sp_type = ''
        self.atk_index = 0
        self.bonus = 0
        self.wins = 0
        self.loss = 0
        self.ties = 0
        self.fight_time = 0
        try:
            self.species_id = int(args[0][2])
            self.plus_atk = int(args[0][3])
            self.plus_dfn = int(args[0][4])
            self.plus_hp = int(args[0][5])
        except:
            raise ValueError
        
    

    def set_attacks(self, *args):
        #append each attack to array
        for atk in args:
            try:
                new_atk = Attack(atk)
                self.attack_list.append(new_atk)
            except Exception as e :
                eprint("ERROR: could not make attack" + str(type(e)))
                continue

    def set_species_data(self, *args):
        if not len(*args) == 4:
            raise AttributeError
        try:
            self.sp_type = args[0][0]
            self.plus_atk += int(args[0][1])
            self.plus_dfn += int(args[0][2])
            self.plus_hp += int(args[0][3])
        except:
            raise ValueError
        
    def fight(self, second):
        if not second:
            eprint("ERROR: fighter is None type")
            raise ValueError
        first_hp = self.plus_hp
        self.bonus = self.get_bonus(self.sp_type, second.sp_type)
        second.bonus = self.get_bonus(second.sp_type, self.sp_type)
        
        second_hp = second.plus_hp
        timer = 0
        self.next_attack(timer)
        second.next_attack(timer)
        while(first_hp > 0 and second_hp > 0):
            #Liam's function its' ugly -- not my fault and it's backwards 
            
            if ( self.atk_timer == timer):
                check = second.plus_dfn - self.plus_atk
                if (check < 0 ):
                    check = 0
                first_half = self.bonus*random.randint(0, check)
                bonus = self.get_bonus(self.attack_list[self.atk_index].atk_type, second.sp_type)
                second_half = bonus*random.randint(self.attack_list[self.atk_index].min_dmg, self.attack_list[self.atk_index].max_dmg)
                second_hp -= first_half + second_half
                self.next_attack(timer)
                
            if ( second.atk_timer == timer):
                check = self.plus_dfn-second.plus_atk
                if (check < 0):
                    check = 0
                first_half = second.bonus*random.randint(0, check) 
                bonus = second.get_bonus(second.attack_list[second.atk_index].atk_type, self.sp_type)            
                second_half = bonus*random.randint(second.attack_list[second.atk_index].min_dmg, second.attack_list[second.atk_index].max_dmg)
                first_hp -= first_half + second_half
                second.next_attack(timer)
            timer += 1 
    
        
        if first_hp > 0:
            return ('One', timer)
        elif second_hp > 0:
            return ('Two', timer)
        else:
            return ('Tie', timer)

    def next_attack(self, timer):
        value = random.randint(0, len(self.attack_list)-1)
        self.atk_index = value
        self.atk_timer = timer + self.attack_list[value].speed
        #print(str(value) + ' ' + str(dude.attack_list[value]))
    
    def get_bonus(self, first, second):
        if first =='Physical':
            if second == 'Biological':
                return 2
            elif second == 'Chemical':
                return .5
        elif first == 'Biological':
            if second == 'Radioactive' or second == 'Technological':
                return 2
        elif first == 'Radioactive':
            if second == 'Physical' or second == 'Mystical' :
                return 2
            elif second == 'Chemical' or second == 'Technological':
                return .5
        elif first == 'Chemical':
            if second == 'Biological':
                return 2
            elif second == 'Radioactive' or second == 'Chemical' or second =='Technological':
                return .5
        elif first == 'Technological':
            if second == 'Radioactive':
                return .5
            elif second == 'Chemical':
                return 2
        elif first == 'Mystical':
            if second == 'Biological' or second == 'Radioactive':
                return 2
            elif second == 'Mineral':
                return 1
            else:
                return .5
        elif first == 'Mineral' and second == 'Mineral':
            return 0
    
        return 1
            
            
class DudeList():
    def __init__(self, con, cursor):
        self.con = con
        self.cursor = cursor
        
        
        self.cursor.execute('SELECT id, name, species_id, plus_atk, plus_dfn, plus_hp from combatant')
        data = self.cursor.fetchall()
        self.dude_list = []
        for stats in data:
            #print(stats)
            try:
                new_dude = Dude(stats)
                self.dude_list.append(new_dude)
                #lookup species base data and add 
                #set species name field
                sqlString = 'SELECT type, base_atk, base_dfn, base_hp from species WHERE id = ' + str(new_dude.species_id)
                self.cursor.execute(sqlString)
                results = self.cursor.fetchall()
                #print(str(results))
                new_dude.set_species_data(*results) 
            except Exception as e :
                eprint("ERROR: could not create dude" + str(type(e)))
                continue
    
        for guy in self.dude_list:
            try:
                sqlString = 'SELECT name, type, min_dmg, max_dmg, speed from attack' +\
                        ' WHERE id in (SELECT attack_id from species_attack' +\
                            ' WHERE species_id = '+ str( guy.species_id) +')'
                self.cursor.execute(sqlString)
                attack_string = self.cursor.fetchall()
                for atk in attack_string:
                    guy.set_attacks(atk)
            except Exception as e:
                eprint("ERROR: could not add attack" + str(type(e)))
                continue
    
    
    def longest_fight(self):
        subString = '(SELECT *, finish - start as diff from fight) AS new_table'
        maxQuerry = '(SELECT MAX(diff) from ' + subString +')'
        sqlString = 'SELECT combatant_one, combatant_two, diff from (SELECT *, finish - start as diff from fight) as tale where diff in ' + maxQuerry
        self.cursor.execute(sqlString)
        result = self.cursor.fetchall()
        return result

    
    def shortest_fight(self):
        subString = '(SELECT *, finish - start as diff from fight) AS new_table'
        maxQuerry = '(SELECT MIN(diff) from ' + subString +')'
        sqlString = 'SELECT combatant_one, combatant_two, diff from (SELECT *, finish - start as diff from fight) as tale where diff in ' + maxQuerry
        self.cursor.execute(sqlString)
        result =self.cursor.fetchall()
        return (result)
    
    def add_fight_data(self):
        self.cursor.execute('SELECT *, finish - start as diff from fight')
        result = self.cursor.fetchall()
        for fight in result:
            if (fight[2] == 'One'):
                self.add_win(fight[0], fight[5])
                self.add_los(fight[1], fight[5])
            elif(fight[2] == 'Two'):
                self.add_win(fight[1], fight[5])
                self.add_los(fight[0], fight[5])
            else:
                self.add_tie(fight[0], fight[5])
                self.add_tie(fight[1], fight[5])
            
    def longest_total_time(self):
        max = 0
        results = []
        for dude in self.dude_list:
            if dude.fight_time > max:
                results = []
                max = dude.fight_time
            if dude.fight_time == max:
                results.append(dude)
        return results
       
    def shortest_total_time(self):
        min = sys.maxsize
        results = []
        for dude in self.dude_list:
            if dude.fight_time < min:
                results = []
                min = dude.fight_time
            if dude.fight_time == min:
                results.append(dude)
        return results
    
    def most_wins(self):
        max = 0
        results = []
        for dude in self.dude_list:
            if dude.wins > max:
                results = []
                max = dude.wins
            if dude.wins == max:
                results.append(dude)
        return results
    
    def most_loss(self):
        max = 0
        results = []
        for dude in self.dude_list:
            if dude.loss > max:
                results = []
                max = dude.loss
            if dude.loss == max:
                results.append(dude)
        return results
    
    def most_attacks(self):
        max = 0
        results = []
        for dude in self.dude_list:
            if len(dude.attack_list) > max:
                results = []
                max = len(dude.attack_list)
            if len(dude.attack_list) == max:
                results.append(dude)
        return results
    
    def most_attacks(self):
        max = 0
        results = []
        for dude in self.dude_list:
            if len(dude.attack_list) > max:
                results = []
                max = len(dude.attack_list)
            if len(dude.attack_list) == max:
                results.append(dude)
        return results
    
    def win_loss_tie(self, species):
        win = 0
        loss = 0
        tie = 0
        for dude in self.dude_list:
            if dude.species_id == species:
                win += dude.wins
                loss += dude.loss
                tie += dude.ties        
    
        return win, loss, tie
    
    def win_loss_tie_by_species(self):
        self.cursor.execute('SELECT id, name from species')
        species_list = self.cursor.fetchall()
        results = []
        for species in species_list:
            wlt = self.win_loss_tie(species[0])
            results.append((species[1], wlt[0], wlt[1], wlt[2]))
        return results
    
    
    
    
    def print_list(self):
        for dude in self.dude_list:
            print(str(dude.sp_type))
    
    def add_win(self, dude, time):
        time = time.total_seconds()
        for guy in self.dude_list:
            if guy.my_id == dude:
                guy.wins += 1
                guy.fight_time +=  time
                return
    
    def add_los(self, dude, time):
        time = time.total_seconds()
        for guy in self.dude_list:
            if guy.my_id == dude:
                guy.loss += 1
                guy.fight_time +=  time
                return
            
    def add_tie(self, dude, time):
        time = time.total_seconds()
        for guy in self.dude_list:
            if guy.my_id == dude:
                guy.ties += 1
                guy.fight_time +=  time
                return


    #check usage

   
    def check_fight(self): 
        self.cursor.execute('SELECT * from fight')
        fights = self.cursor.fetchall()
        if len(fights) > 0:    
            eprint("ERROR: tournament has already completed")
            self.con.commit()
            self.cursor.close()
            sys.exit()
    
    def ultimate_showdown_of_ultimate_destiny(self):
        if len(self.dude_list) < 2:
            eprint("ERROR: not enough fighters for battle")
            return
        #here is the loop-d-loop // make every fighter fight every fighter.
    
        for x in range(0,len(self.dude_list)-1):
            first = self.dude_list[x]
            for y in range(x+1, len(self.dude_list)):
                second = self.dude_list[y]
                #start = get time
                try:
                    winner = first.fight(second)
                    print(str(winner))
                except ValueError:
                    eprint("ERROR: fight failure")
                    continue
                time = str(datetime.timedelta(seconds=winner[1]))
                values = str(first.my_id) + ', ' + str(second.my_id) + ', ' + "'" + winner[0]+ "'" +', TIMESTAMP '+"' 2016-06-10 00:00:00', TIMESTAMP '2016-06-10 " + time+ "'"
                sqlString = 'insert into fight (combatant_one, combatant_two, winner, start, finish) values ('+values+');'
                self.cursor.execute(sqlString)

 
def connect(database):
    u_name = getpass.getuser()
    connect_line = "dbname="+str(database)+" user=" + u_name
    #print(connect_line)
    con = psycopg2.connect(connect_line)
    cursor = con.cursor()
    
    return con, cursor
    
    
