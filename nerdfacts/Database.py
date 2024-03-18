
import psycopg2

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            database="postgres_db",
            host="postgres",
            user="user",
            password="pass",
            port="5432",
        )

    def close(self):
        self.connection.close()
        print("PostgreSQL connection is closed")

    def create_table(self):
        cursor = self.connection.cursor()
        # cursor.execute("DROP TABLE IF EXISTS pokemon")
        cursor.execute("""CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY, 
            name TEXT,
            types TEXT[],
            height INT,
            weight INT
            )""", 
        )
        self.connection.commit()
        cursor.close()

    def store_pokemon(self, pokemon):
        cursor = self.connection.cursor()
        cursor.execute("""INSERT INTO pokemon (
                       name, types, height, weight
                       ) VALUES (%s, %s, %s, %s)""", 
            (pokemon.name, 
             pokemon.types, 
             pokemon.height, 
             pokemon.weight
            )
        )
        self.connection.commit()
        cursor.close()

    def purge_pokemon(self):
        cursor = self.connection.cursor()
        cursor.execute("DELETE * FROM pokemon")
        self.connection.commit()
        cursor.close()

    def get_all_pokemon(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM pokemon")
        pokemon = cursor.fetchall()
        cursor.close()
        return pokemon

    def get_x_pokemon(self, x):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM pokemon LIMIT {x}")
        pokemon = cursor.fetchall()
        cursor.close()
        return pokemon
    
    def get_average_height(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT AVG(height) FROM pokemon")
        avg_height = cursor.fetchone()
        cursor.close()
        return avg_height
    
    def get_max_height(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, height FROM pokemon WHERE height = ( SELECT MAX(height) FROM pokemon)")
        poke_max_height = cursor.fetchone()
        cursor.close()
        return poke_max_height

    def get_type_counts(self):
        cursor = self.connection.cursor()
        cursor.execute("""
                       SELECT type, 
                       COUNT(*) 
                       FROM pokemon, unnest(types) type 
                       GROUP BY type
                       """)
        type_counts = cursor.fetchall()
        cursor.close()
        return type_counts