import random
import sqlite3 as sql


class Generator:
    """
        Класс для создания и заполнения тестовой базы данных
    """
    def __init__(self) -> None:
        with sql.connect("ships.db") as con:
            self.cur = con.cursor()
            self.tables = ["ship", "hull", "weapon", "engine"]
            self.drop_tables()
            self.generate_tables()
            self.fill_tables()

    def drop_tables(self) -> None:
        """
            Удаляет таблицы в случае если такие уже есть
        :return: None
        """
        for i in self.tables:
            self.cur.execute(f"DROP TABLE IF EXISTS {i}s")

    def generate_tables(self) -> None:
        """
            Генерируем нужные таблицы и связи в них
        :return: None
        """
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tables[1]}s (
            hull TEXT NOT NULL PRIMARY KEY,
            armor INTEGER NOT NULL,
            type INTEGER NOT NULL,
            capacity INTEGER NOT NULL
            )""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tables[2]}s (
            weapon TEXT NOT NULL PRIMARY KEY,
            reload_speed INTEGER NOT NULL,
            rotation_speed INTEGER NOT NULL,
            diameter INTEGER NOT NULL,
            power_volley INTEGER NOT NULL,
            count INTEGER NOT NULL
            )""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tables[3]}s (
            engine TEXT NOT NULL PRIMARY KEY,
            power INTEGER NOT NULL,
            type INTEGER NOT NULL
            )""")
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.tables[0]}s (
            {self.tables[0]} TEXT NOT NULL PRIMARY KEY,
            {self.tables[1]} TEXT NOT NULL,
            {self.tables[2]} TEXT NOT NULL,
            {self.tables[3]} TEXT NOT NULL,
            FOREIGN KEY ({self.tables[1]}) REFERENCES {self.tables[1]}s ({self.tables[1]}),
            FOREIGN KEY ({self.tables[2]}) REFERENCES {self.tables[2]}s ({self.tables[2]}),
            FOREIGN KEY ({self.tables[3]}) REFERENCES {self.tables[3]}s ({self.tables[3]})
            )""")

    def get_dict_of_modules(self, module_name: str) -> list:
        """
            Возвращает лист названий модулей
        :param module_name: имя модуля
        :return: list
        """
        all_modules = []
        self.cur.execute(f"""SELECT {module_name} FROM {module_name}s""")
        tuple_modules = self.cur.fetchall()
        for i in tuple_modules:
            all_modules.append(i[0])
        return all_modules

    def fill_tables(self) -> None:
        """
            Заполняет сгренерированные таблицы
        :return: None
        """
        for i in range(6):
            self.cur.execute(f"""INSERT INTO {self.tables[3]}s VALUES (
            '{self.tables[3]}{i+1}', 
            '{random.randint(1,20)}', 
            '{random.randint(1,20)}'
            )""")

        for i in range(5):
            self.cur.execute(f"""INSERT INTO {self.tables[1]}s VALUES (
            '{self.tables[1]}{i + 1}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}'
            )""")

        for i in range(20):
            self.cur.execute(f"""INSERT INTO {self.tables[2]}s VALUES (
            '{self.tables[2]}{i + 1}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}', 
            '{random.randint(1, 20)}'
            )""")

        hulls = self.get_dict_of_modules(self.tables[1])
        weapons = self.get_dict_of_modules(self.tables[2])
        engines = self.get_dict_of_modules(self.tables[3])

        for i in range(200):
            self.cur.execute(f"""INSERT INTO ships VALUES (
            'ship{i + 1}', 
            '{weapons[random.randint(1, len(weapons) - 1)]}', 
            '{hulls[random.randint(1, len(hulls) - 1)]}', 
            '{engines[random.randint(1, len(engines) - 1)]}'
            )""")
