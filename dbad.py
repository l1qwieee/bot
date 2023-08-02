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

    def ff_step(self, table, step):
        with self.connection:
            self.cursor.execute(f"INSERT INTO {table}(step) VALUES (:step)", ({"step": step}))

    def f_step(self, table, game, stp, step2):
        with self.connection:
            self.cursor.execute(f"UPDATE {table} SET game = :game, step = :stp WHERE step = :step2", ({"game": game, "stp": stp, "step2": step2}))

    def add(self, column, c, stp1, stp2, game):
        with self.connection:
            #self.cursor.execute(f"UPDATE schedule SET {column} = ?, step = ? WHERE step = ? and game = ?", (c, stp1, stp2, game,))
            self.cursor.execute(f"UPDATE schedule_data SET {column} = :c, step = :stp1 WHERE step = :stp2 and game = :game", ({"c": c, "stp1": stp1, "stp2": stp2, "game": game}))

    def select(self, column, stp):
        with self.connection:
            self.cursor.execute(f"SELECT {column} FROM schedule_data WHERE step = ?", (stp,))
            return self.cursor.fetchone()

    def select_data(self, step):
        with self.connection:
            self.cursor.execute("SELECT data FROM prog_who_reg WHERE step = :step", ({"step": step}))
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
            self.cursor.execute("UPDATE schedule_games SET places = :place, step = 'complited' WHERE game_id = :game_id", ({"place": place, "game_id": game_id}))
            self.cursor.execute("UPDATE schedule_data SET step = 'complited' WHERE data_id = :data_id", ({"data_id": data_id}))


    def select_data_id(self, step):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE step = :step", ({"step": step}))
            return self.cursor.fetchone()

    def insert_time(self, data_id, time, step):
        with self.connection:
            self.cursor.execute("INSERT INTO schedule_games(data_id, time, step) VALUES (?, ?, ?)", (data_id, time, step,))

    def update_step(self, data_id, step):
        with self.connection:
            self.cursor.execute("UPDATE schedule_data SET step = :step WHERE data_id = :data_id", ({"step": step, "data_id": data_id}))

    def select_id(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT game_id FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def sel_all_data(self):
        with self.connection:
            self.cursor.execute("SELECT data FROM schedule_data")
            return self.cursor.fetchall()
        
    def sel_data_id(self, data):
        with self.connection:
            self.cursor.execute("SELECT data_id FROM schedule_data WHERE data = :data", ({"data": data}))
            return self.cursor.fetchone()
        
    def sel_time(self, data_id):
        with self.connection:
            self.cursor.execute("SELECT time FROM schedule_games WHERE data_id = :data_id", ({"data_id": data_id}))
            return self.cursor.fetchall()
        
    def update(self, column, value, nextst, step):
        with self.connection:
            self.cursor.execute(f"UPDATE prog_who_reg SET {column} = :value, step = :nextst WHERE step = :step", ({"value": value, "nextst": nextst, "step": step}))

    def chek_guys(self, game_id):
        with self.connection:
            self.cursor.execute("""
                SELECT name, people, payment
                FROM schedule_games
                JOIN com_reg_to_games ON schedule_games.game_id = com_reg_to_games.game_id
                JOIN reg_users ON com_reg_to_games.user_id = reg_users.user_id
                WHERE schedule_games.game_id = :game_id
                AND schedule_games.step = 'complited'
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
            print(res)
            return res
        
    def sel_all_us(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT user_id FROM com_reg_to_games WHERE game_id = :game_id", ({"game_id": game_id}))
            res = self.cursor.fetchone()
            print(res)
            return res
        
    def sel_all_nickname(self, game_id):
        with self.connection:
            self.cursor.execute("SELECT username FROM reg_users JOIN com_reg_to_games ON reg_users.user_id = com_reg_to_games.user_id WHERE game_id = :game_id", ({"game_id": game_id}))
            return self.cursor.fetchall()

    def delete(self):
        with self.connection:
            self.cursor.execute("DELETE FROM prog_who_reg")

    def w_is_inside(self, table):
        with self.connection:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            res = self.cursor.fetchone()[0]
            print(res)
            if res == 0:
                return False
            else:
                return True
            
        
    def ex_step(self, table, step):
        with self.connection:
            self.cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE step = :step", ({"step": step}))
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
            self.cursor.execute("DELETE FROM schedule_data WHERE step != 'complited'")
            self.cursor.execute("DELETE FROM schedule_games WHERE step != 'complited'")



#        SELECT nickname FROM reg_users JOIN com_reg_to_games ON reg_users.user_id = com_reg_to_games.user_id WHERE game_id = :game_id
