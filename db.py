import sqlite3

import logging

class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    def reg_users(self, uid, name, lname, usname, lan_code):
        with self.connection:
            self.cursor.execute(f"INSERT INTO reg_users(user_id, name, surname, username, language_code) VALUES (?, ?, ?, ?, ?)", (uid, name, lname, usname, lan_code,))

    def add_reg(self, uid, regs):
        with self.connection:
            self.cursor.execute("UPDATE reg_users SET reg = ? WHERE user_id = ?", (uid, regs))
            return self.cursor.fetchone()



    def chek(self, uid):
        with self.connection:
            self.cursor.execute("SELECT name, surname, people, payment, day, time FROM reg_users, reg_volleyball WHERE (reg_users.user_id = reg_volleyball.user_id) and reg_users.user_id = ?", (uid,))
            return self.cursor.fetchone()

    def update_something(self, uid, table, column, value):
        with self.connection:
            self.cursor.execute(f"UPDATE {table} SET {column} = ? WHERE user_id = ? and stage = 'registration_in_progress'", (value, uid,))


    

    def sel_count_time(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_games WHERE data_id = ?", (data_id,))
            res = self.cursor.fetchone()
            return res

    
        
    def add_game(self, column, ww, stp, uid):
        with self.connection:
            self.cursor.execute(f"UPDATE reg_to_games SET {column} = ?, step = ? WHERE user_id = ?", (ww, stp, uid,))


    def select_entry(self, column, uid, game):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM com_reg_to_games WHERE user_id = ? and game = ?", (uid, game,))
            return self.cursor.fetchall()
    
    def del_entry(self, uid, game, day):
        with self.connection:
            self.cursor.execute("DELETE FROM _reg_to_games WHERE user_id = :uid AND game = :game AND day = :day", ({"uid": uid, "game": game, "day": day}))
    
    def del_data(self, day):
        with self.connection:
            self.cursor.execute("DELETE FROM reg_to_games WHERE day = :day", ({"day": day}))

    def change_step(self, step, uid):
        with self.connection:
            self.cursor.execute("UPDATE reg_to_games SET step = :step WHERE user_id = :uid", ({"step":step, "uid":uid,}))

    def select_info(self, uid, game, day):
        with self.connection:
            self.cursor.execute("SELECT name, game, people, day, time, payment FROM reg_users, reg_to_games WHERE reg_users.user_id = reg_to_games.user_id AND reg_users.user_id = :uid AND game = :game AND day = :day", (uid, game, day))
            res = self.cursor.fetchall()
            return res
    
    def all_days(self):
        with self.connection:
            self.cursor.execute("SELECT day FROM reg_to_games")
            res = self.cursor.fetchall()
            return res
        
    def hm_dataid(self, data):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule WHERE data = :data", ({"data": data}))
            return self.cursor.fetchone()
        
    def return_info(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT time, places FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def select_id_game_us(self, uid):
        with self.connection:
            self.cursor.execute("SELECT id_game_user FROM reg_to_games WHERE user_id = ?", (uid,))
            return self.cursor.fetchone()
        
    def select_all_time(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT time FROM schedule_games WHERE data_id = ?", (data_id,))
            return self.cursor.fetchall()
        

    

    
        
    def select_data_id(self, data):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE data = :data", ({"data": data}))
            return self.cursor.fetchone()

    def isert_game_id(self, user_id, game_id):
        with self.connection:
            self.cursor.execute("UPDATE inf SET game_id = :game_id WHERE user_id = :user_id", ({"game_id": game_id, "user_id": user_id}))

    def del_inf_game(self, user_id, game_id):
        with self.connection:
            self.cursor.execute("DELETE FROM com_reg_to_games WHERE user_id = :user_id and game_id = :game_id", ({"user_id": user_id, "game_id": game_id}))

    def s_game_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM inf WHERE user_id =:user_id", ({"user_id": user_id}))
            return self.cursor.fetchone()
        
    
        
    def sel_game(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        
    def update_step(self, step, user_id):
        with self.connection:
            self.cursor.execute("UPDATE prog_reg_to_games SET step = :step WHERE user_id = :user_id", ({"step": step, "user_id": user_id}))

    def update(self, column, step, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE prog_reg_to_games SET {column} = NULL, step = :step WHERE user_id = :user_id", ({"step": step, "user_id": user_id}))

    def update_step(self, step, user_id):
        with self.connection:
            self.cursor.execute("UPDATE prog_reg_to_games SET step = :step WHERE user_id = :user_id", ({"step": step, "user_id": user_id}))










    def add_new_user(self, uid, table):
        with self.connection:
            self.cursor.execute(f"INSERT INTO {table}(user_id) VALUES (?)", (uid,))

    def chek_reg(self, uid):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) as reg FROM reg_users WHERE user_id = ?", (uid,))
            return self.cursor.fetchone()[0]

    def new_us(self, user_id, name, surname, user_name, lang):
        with self.connection:
            self.cursor.execute("INSERT INTO reg_users(user_id, name, surname, username, language_code) VALUES (?, ?, ?, ?, ?)", (user_id, name, surname, user_name, lang,))


    def f_step(self, uid, lvl):
        with self.connection:
            self.cursor.execute("INSERT INTO prog_reg_to_games(user_id, lvl) VALUES (?, ?)", (uid, lvl,))

    def sel_user(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))
            res = self.cursor.fetchone()
            return res

    def del_prog_to_game(self, user_id):
        with self.connection:
            self.cursor.execute("DELETE FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))

    def update_prog_reg(self, column, value, lvl, user_id):
        with self.connection:
            self.cursor.execute(f"UPDATE prog_reg_to_games SET {column} = :value, lvl = :lvl WHERE user_id = :user_id", ({"value": value, "lvl": lvl, "user_id": user_id}))

    def select(self, column, uid):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM prog_reg_to_games WHERE user_id = ?", (uid,))
            return self.cursor.fetchone()
        
    def select_id_data(self):
        with self.connection:
            self.cursor.execute(f"SELECT COUNT(*) FROM schedule_data")
            return self.cursor.fetchone()
        
    def select_data(self, data_id, game):
        with self.connection:
            self.cursor.execute(f"SELECT data FROM schedule_data WHERE data_id = :data_id and game = :game", ({ "data_id": data_id, "game": game}))
            res = self.cursor.fetchone()
            return res

    def select_game_us(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game, day, time, people FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))
            res = self.cursor.fetchone()
            return res
        
    def select_id_wh_data(self, data, game):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE data = :data and game = :game", ({"data": data, "game": game}))
            return self.cursor.fetchone()
        
    def select_game_id(self, data_id, time):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM schedule_games WHERE data_id = :data_id and time = :time and step = 'complited'", ({"data_id": data_id, "time": time}))
            res = self.cursor.fetchone()
            return res
        
    def select_place(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT places FROM schedule_games WHERE game_id = :game_id", ({"game_id": game_id}))
            res = self.cursor.fetchone()
            return res
        
    def update_places(self, places, data_id, game_id):
        with self.connection:
            self.cursor.execute("UPDATE schedule_games SET places = :places WHERE data_id = :data_id and game_id = :game_id", ({"places": places, "data_id": data_id, "game_id": game_id}))

    def chek_condition(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT day, time FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))
            return self.cursor.fetchone()
        
    def complete_registration(self, uid):
        with self.connection:
            self.cursor.execute("DELETE FROM prog_reg_to_games WHERE user_id = ?", (uid,))

    def select_pep(self, uid):
        with self.connection:
            self.cursor.execute("SELECT people FROM prog_reg_to_games WHERE user_id = :uid", ({"uid": uid}))
            return self.cursor.fetchone()
        
    def com_reg_to_games(self, user_id, game_id, people, mes):
        with self.connection:
            self.cursor.execute("INSERT INTO com_reg_to_games(user_id, game_id, people, payment) VALUES (?, ?, ?, ?)", (user_id, game_id, people, mes,))
        
    def sel_pay(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT payment FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))
            return self.cursor.fetchone()
        
    def click_time(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT time FROM prog_reg_to_games WHERE user_id = :user_id", ({"user_id": user_id}))
            return self.cursor.fetchone()
        
    def sel_lvl(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT lvl FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            res = self.cursor.fetchone()
            return res
        
    def sel_data(self, game_id, game):
        with self.connection:
            self.cursor.execute("SELECT data_id, time FROM schedule_games WHERE game_id = ?", (game_id,))
            res = self.cursor.fetchone()
            return res
        
    def click_data(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT day FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        
    def click_people(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT people FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        
    def click_game(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
    
    def check_lvl(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT lvl FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        
    def update_lvl(self, lvl, user_id):
        with self.connection:
            self.cursor.execute("UPDATE prog_reg_to_games SET lvl = :lvl WHERE user_id = :user_id", ({"lvl": lvl, "user_id": user_id}))

    def count(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        
    def select_game(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        
    def countprog(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            res = self.cursor.fetchall()
            return res

    def start_inf(self, user_id):
        with self.connection:
            self.cursor.execute("INSERT INTO inf(user_id) VALUES (?)", (user_id,))

    def sel_us_game_id(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM com_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchall()
        
    def chek_game(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT game FROM schedule_data WHERE data_id = :data_id", ({"data_id": data_id}))
            res = self.cursor.fetchone()
            return res

    def del_all_inf(self, uid):
        with self.connection:
            self.cursor.execute("DELETE FROM reg_users WHERE user_id = ?", (uid,))
            self.cursor.execute("DELETE FROM com_reg_to_games WHERE user_id = ?", (uid,))
    
    def click_payment(self, user_id):
        with self.connection:
            self.cursor.execute("SELECT payment FROM prog_reg_to_games WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
