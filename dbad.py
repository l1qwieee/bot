import sqlite3

import logging


class DataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def chek_info(self, ds, idd):
        with self.connection:
            self.cursor.execute("SELECT user_id, name, surname, people, payment, day, time FROM users WHERE day = ? and id = ?", (ds, idd))
            return self.cursor.fetchone()
        
    def how_many_str(self, uid):
        with self.connection:
            self.cursor.execute("SELECT user_id, name, surname, people, payment, day, time FROM users WHERE user_id = ?", (uid,))
            rows = self.cursor.fetchall()
            quantity = (len(rows))
            return quantity
        
    def column_counter(self, table, column):
        with self.connection:
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns_info = self.cursor.fetchall()
            count = sum(1 for column in columns_info if column[1] == column)
            return count
        
    def add_data(self, table, data):
        with self.connection:
            self.cursor.execute(f"INSERT INTO {table}(day) VALUES (?)", (data,))
    
    def add_time(self, table, t1, data):
        with self.connection:
            self.cursor.execute(f"UPDATE {table} SET time = ? WHERE day = ?", (t1, data,))

    def chek_data(self, data, game):
        with self.connection:
            self.cursor.execute(f"SELECT data FROM schedule_data WHERE data = ? and game = ?", (data, game,))
            info = self.cursor.fetchall()
            return info
    
    def del_data(self, data, table):
        with self.connection:
            self.cursor.execute(f"DELETE FROM {table} WHERE data = ?", (data,))

    def change_data(self, data, table):
        with self.connection:
            self.cursor.execute(f"UPDATE {table} SET day = ?", (data,))

    def ff_step(self, table, lvl):
        with self.connection:
            self.cursor.execute(f"INSERT INTO {table}(lvl) VALUES (:lvl)", ({"lvl": lvl}))

    def f_step(self, table, game, nextlvl, lvl):
        with self.connection:
            self.cursor.execute(f"UPDATE {table} SET game = :game, lvl = :nextlvl WHERE lvl = :lvl", ({"game": game, "nextlvl": nextlvl, "lvl": lvl}))

    def add(self, column, c, nextlvl, lvl, game):
        with self.connection:
            #self.cursor.execute(f"UPDATE schedule SET {column} = ?, step = ? WHERE step = ? and game = ?", (c, stp1, stp2, game,))
            self.cursor.execute(f"UPDATE schedule_data SET {column} = :c, lvl = :nextlvl WHERE lvl = :lvl and game = :game", ({"c": c, "nextlvl": nextlvl, "lvl": lvl, "game": game}))

    def select(self, column, lvl):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM schedule_data WHERE lvl = ?", (lvl,))
            return self.cursor.fetchone()

    def select_data(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT data FROM schedule_data WHERE lvl = :lvl", ({"lvl": lvl}))
            return self.cursor.fetchone()
    
    def insert_another_data(self, game, data, step):
        with self.connection:
            self.cursor.execute("INSERT INTO schedule(game, data, step) VALUES (?, ?, ?)", (game, data, step,))

    def select_inf(self, data, game):
        with self.connection:
            self.cursor.execute("SELECT id, game, time FROM schedule WHERE data = :data and game = :game", ({"data": data, "game": game}))
            return self.cursor.fetchall()
        
    def add_place(self, place, game_id, data_id):
        with self.connection:
            self.cursor.execute("UPDATE schedule_games SET places = :place, lvl = 5 WHERE game_id = :game_id", ({"place": place, "game_id": game_id}))
            self.cursor.execute("UPDATE schedule_data SET lvl = 5 WHERE data_id = :data_id", ({"data_id": data_id}))


    def select_data_id(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE lvl = :lvl", ({"lvl": lvl}))
            return self.cursor.fetchone()

    def insert_time(self, data_id, time, lvl):
        with self.connection:
            self.cursor.execute("INSERT INTO schedule_games(data_id, time, lvl) VALUES (?, ?, ?)", (data_id, time, lvl,))

    def update_step(self, data_id, lvl):
        with self.connection:
            self.cursor.execute("UPDATE schedule_data SET lvl = :lvl WHERE data_id = :data_id", ({"lvl": lvl, "data_id": data_id}))

    def select_id(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def sel_all_data(self, game):
        with self.connection:
            self.cursor.execute("SELECT data FROM schedule_data WHERE game = :game", ({"game": game}))
            return self.cursor.fetchall()
        
    def sel_data_id(self, data):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE data = :data", ({"data": data}))
            return self.cursor.fetchone()
        
    def sel_time(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT time FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def update(self, column, value, nextlvl, lvl):
        with self.connection:
            self.cursor.execute(f"UPDATE prog_who_reg SET {column} = :value, lvl = :nextlvl WHERE lvl = :lvl", ({"value": value, "nextlvl": nextlvl, "lvl": lvl}))

    def chek_guys(self, game_id):
        with self.connection:
            self.cursor.execute("""
                SELECT name, people, payment
                FROM schedule_games
                JOIN tg_users ON schedule_games.game_id = tg_users.game_id
                JOIN reg_users ON tg_users.user_id = reg_users.user_id
                WHERE schedule_games.game_id = :game_id
                AND schedule_games.lvl = 10
            """, {"game_id": game_id})    
            return self.cursor.fetchall()
        
    def select_game_id(self, data_id, time):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM schedule_games WHERE data_id = :data_id and time = :time", ({"data_id": data_id, "time": time}))
            return self.cursor.fetchone()
        
    def select_data_id_chek(self, data):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE data = :data", ({"data": data}))
            res = self.cursor.fetchone()
            return res
        
    def sel_all_us(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT user_id FROM tg_users WHERE game_id = :game_id", ({"game_id": game_id}))
            res = self.cursor.fetchone()
            return res
        
    def sel_all_nickname(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT username FROM reg_users JOIN tg_users ON reg_users.user_id = tg_users.user_id WHERE game_id = :game_id", ({"game_id": game_id}))
            return self.cursor.fetchall()

    def delete(self):
        with self.connection:
            self.cursor.execute("DELETE FROM prog_who_reg")

    def w_is_inside(self, table):
        with self.connection:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            res = self.cursor.fetchone()[0]
            if res == 0:
                return False
            else:
                return True
            
        
    def ex_step(self, table, lvl):
        with self.connection:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE lvl = :lvl", ({"lvl": lvl}))
            res = self.cursor.fetchone()[0]
            if res == 0:
                return False
            else:
                return True


    def inf_game(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM prog_who_reg")
            return self.cursor.fetchall()


    def hm_games(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_games WHERE data_id = ?", (data_id,))
            return self.cursor.fetchone()
        
    def del_game(self, game_id):
        with self.connection:
            self.cursor.execute("DELETE FROM schedule_games WHERE game_id = ?", (game_id,))

    def delete_data(self):
        with self.connection:
            self.cursor.execute("DELETE FROM schedule_data WHERE lvl != 10")
            self.cursor.execute("DELETE FROM schedule_games WHERE lvl != 10")

    def c_n_d(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_games WHERE time = NULL")
            return self.cursor.fetchall()

#        SELECT nickname FROM reg_users JOIN com_reg_to_games ON reg_users.user_id = com_reg_to_games.user_id WHERE game_id = :game_id


    def count_games(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_games WHERE lvl = ?", (lvl,))
            return self.cursor.fetchone()
        
    def select_game(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT game FROM schedule_data WHERE lvl = ?", (lvl,))
            return self.cursor.fetchone()
        
    def name_table(self):
        with self.connection:
#            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN (SELECT name FROM schedule_data, schedule_games, prog_who_reg WHERE schedule_data.lvl, schedule_games.lvl, prog_who_reg.lvl != 10)")
            self.cursor.execute("""
                                SELECT 'schedule_data' AS table_name FROM schedule_data WHERE lvl != 10
                                UNION
                                SELECT 'schedule_games' AS table_name FROM schedule_games WHERE lvl != 10
                                UNION
                                SELECT 'prog_who_reg' AS table_name FROM prog_who_reg WHERE lvl != 10;
                                """)
#            table_names = [row[0] for row in self.cursor.fetchall()]
            return self.cursor.fetchone()

    def sel_lvl(self, table):
        with self.connection:
            self.cursor.execute(f"SELECT lvl FROM {table} WHERE lvl != 10")
            return self.cursor.fetchone()
        
    def select_game_whor(self):
        with self.connection:
            self.cursor.execute("SELECT game FROM prog_who_reg")
            return self.cursor.fetchone()
        
    def select_data_whor(self):
        with self.connection:
            self.cursor.execute("SELECT data FROM prog_who_reg")
            return self.cursor.fetchone()
        
    def update_lvl_whor(self, lvl):
        with self.connection:
            self.cursor.execute("UPDATE prog_who_reg SET lvl = :lvl", (lvl,))

    def update_lvl(self, lvl, table1, table2):
        with self.connection:
            self.cursor.execute(f"UPDATE {table1} SET lvl = :lvl WHERE lvl != 10", {"lvl": lvl})
            self.cursor.execute(f"UPDATE {table2} SET lvl = :lvl WHERE lvl != 10", {"lvl": lvl})

    def select_new_games(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_games WHERE lvl != 10")
            return self.cursor.fetchone()
        
    def select_times(self):
        with self.connection:
            self.cursor.execute("SELECT time FROM schedule_games WHERE lvl != 10")
            return self.cursor.fetchall()
        
    def end(self):
        with self.connection:
            self.cursor.execute("UPDATE schedule_games SET lvl = 10 WHERE lvl != 10")
            self.cursor.execute("UPDATE schedule_data SET lvl = 10 WHERE lvl != 10")

    def dele(self):
        with self.connection:
            self.cursor.execute("DELETE FROM schedule_data WHERE lvl != 10")
            self.cursor.execute("DELETE FROM schedule_games WHERE lvl != 10")

    def delete_new_times(self):
        with self.connection:
            self.cursor.execute("DELETE FROM schedule_games WHERE lvl != 10")

    def f_step_new_us(self, lvl):
        with self.connection:
            self.cursor.execute("INSERT INTO users_from_admin(lvl) VALUES (?)", (lvl))

    def delete_prog_reg(self):
        with self.connection:
            self.cursor.execute("DELETE FROM users_from_admin WHERE lvl != 10")

    def add_name(self, name, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET name = :name, lvl = :nextlvl WHERE lvl = :lvl", ({"name": name, "nextlvl": nextlvl, "lvl": lvl}))

    def select_game_admin(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT game FROM users_from_admin WHERE lvl = :lvl", ({"lvl": lvl}))
            return self.cursor.fetchone()

    def select_name(self):
        with self.connection:
            self.cursor.execute("SELECT name FROM users_from_admin")
            return self.cursor.fetchone()

    def add_date(self, date, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET date = :date, lvl = :nextlvl WHERE lvl = :lvl", ({"date": date, "nextlvl": nextlvl, "lvl": lvl}))

    def add_time_admin(self, time, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET time = :time, lvl = :nextlvl WHERE lvl = :lvl", ({"time": time, "nextlvl":nextlvl, "lvl": lvl}))

    def select_ad_data(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT date FROM users_from_admin WHERE lvl = :lvl", ({"lvl": lvl}))
            return self.cursor.fetchone()
        
    def add_seats(self, seats, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET seats = :seats, lvl = :nextlvl WHERE lvl = :lvl", ({"seats": seats, "nextlvl": nextlvl, "lvl": lvl}))

    def select_ad_us(self, lvl):
        with self.connection:
            self.cursor.execute(f"SELECT admin_id, game, date, name, time, seats, payment FROM users_from_admin WHERE lvl = ?", (lvl,))
            return self.cursor.fetchall()
        
    def add_payment(self, payment, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET payment = :payment, lvl = :nextlvl WHERE lvl = :lvl", ({"payment": payment, "nextlvl": nextlvl, "lvl": lvl}))

    def select_inf_ad(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT admin_id, game, date, name, time, seats, payment FROM users_from_admin WHERE lvl = ?", (lvl,))
            return self.cursor.fetchall()
        
    def add_new(self, admin_id, game_id, seats, payment):
        with self.connection:
            self.cursor.execute("INSERT INTO call_users(admin_id, game_id, seats, payment) VALUES (:admin_id, :game_id, :seats, :payment)", ({"admin_id": admin_id, "game_id": game_id, "seats": seats, "payment": payment}))

    def delete_us_admin(self, lvl):
        with self.connection:
            self.cursor.execute("DELETE FROM users_from_admin WHERE lvl = ?", (lvl,))

    def set(self):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM users_from_admin WHERE settings = 'start'")
            res = self.cursor.fetchone()[0]
            if res == 0:
                res = False
            return res
        
    def up_set(self, value):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET settings = :value", ({"value": value}))
    
    def sel_set(self, lvl):
        with self.connection:
            self.cursor.execute("SELECT settings FROM users_from_admin WHERE lvl = :lvl", ({"lvl": lvl}))
            return self.cursor.fetchone()

    def update_column(self, column, value):
        with self.connection:
            self.cursor.execute(f"UPDATE users_from_admin SET {column} = :value WHERE settings = 'start'", ({"value": value}))

    def sel_admin_us(self, column, lvl):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM users_from_admin WHERE lvl = :lvl", ({"lvl":lvl}))
            return self.cursor.fetchone()
        
    def update_lvl_admin(self, nextlvl, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET lvl = :nextlvl WHERE lvl = :lvl", ({"nextlvl": nextlvl, "lvl": lvl}))

    def update_lvl_set(self, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET lvl = :lvl, settings = 'start' WHERE lvl != 10", ({"lvl": lvl}))

    def sel_seats(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT places FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def select_seats(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT places FROM schedule_games WHERE game_id = :game_id", ({"game_id": game_id}))
            return self.cursor.fetchone()
        
    def update_seats(self, seats, game_id):
        with self.connection:
            self.cursor.execute("UPDATE schedule_games SET places = :seats WHERE game_id = :game_id", ({"seats": seats, "game_id": game_id}))

    def select_cho_to(self, column, column2, value):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM users_from_admin WHERE {column2} = :value", ({"value": value}))
            return self.cursor.fetchall()
        
    def select_count_games(self, game):
        with self.connection:
            self.cursor.execute("SELECT COUNT(*) FROM schedule_data WHERE game = :game", ({"game": game}))
            return self.cursor.fetchone()
    
    def update_num(self, num, lvl):
        with self.connection:
            self.cursor.execute("UPDATE users_from_admin SET phone_num = :num WHERE lvl = :lvl", ({"num": num, "lvl": lvl}))