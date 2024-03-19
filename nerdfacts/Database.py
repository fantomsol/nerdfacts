import psycopg2


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            database="postgres_db",
            host="postgres",
            # host="localhost",
            user="user",
            password="pass",
            port="5432",
        )

    def close(self):
        self.connection.close()
        print("PostgreSQL connection is closed")

    def _run_query(self, query, fetch, data=None):
        cursor = self.connection.cursor()
        cursor.execute(query, data)
        self.connection.commit()
        if fetch == "one":
            return cursor.fetchone()
        elif fetch == "all":
            return cursor.fetchall()
        else:
            return

    def create_table(self):
        return self._run_query(
            """CREATE TABLE IF NOT EXISTS pokemon (
            id SERIAL PRIMARY KEY,
            name TEXT,
            types TEXT[],
            height FLOAT,
            weight FLOAT
            )""",
            "none",
        )

    def store_pokemon(self, pokemon):
        self._run_query(
            query="""INSERT INTO pokemon (
                          name, types, height, weight
                            ) VALUES (%s, %s, %s, %s)""",
            fetch="none",
            data=(pokemon.name, pokemon.types, pokemon.height, pokemon.weight),
        )

    def purge_pokemon(self):
        return self._run_query("DROP TABLE IF EXISTS pokemon", "none")

    def get_all_pokemon(self):
        return self._run_query("SELECT * FROM pokemon", "all")

    def get_x_pokemon(self, x):
        return self._run_query(f"SELECT * FROM pokemon LIMIT {x}", "all")

    def get_average_height(self):
        return self._run_query("SELECT AVG(height) FROM pokemon", "one")

    def get_average_weight(self):
        return self._run_query("SELECT AVG(weight) FROM pokemon", "one")

    def get_tallest(self):
        return self._run_query(
            "SELECT name, height FROM pokemon WHERE height = ( SELECT MAX(height) FROM pokemon)",
            "one",
        )

    def get_shortest(self):
        return self._run_query(
            "SELECT name, height FROM pokemon WHERE height = ( SELECT MIN(height) FROM pokemon)",
            "one",
        )

    def get_heaviest(self):
        return self._run_query(
            "SELECT name, weight FROM pokemon WHERE weight = ( SELECT MAX(weight) FROM pokemon)",
            "one",
        )

    def get_lightest(self):
        return self._run_query(
            "SELECT name, weight FROM pokemon WHERE weight = ( SELECT MIN(weight) FROM pokemon)",
            "one",
        )

    def get_avg_height_per_type(self):
        return self._run_query(
            """
                       SELECT type, 
                       AVG(height) 
                       FROM pokemon, unnest(types) type 
                       GROUP BY type
                       """,
            "all",
        )

    def get_avg_weight_per_type(self):
        return self._run_query(
            """
                       SELECT type, 
                       AVG(weight) 
                       FROM pokemon, unnest(types) type 
                       GROUP BY type
                       """,
            "all",
        )

    def get_type_counts(self):
        return self._run_query(
            """
                       SELECT type, 
                       COUNT(*) 
                       FROM pokemon, unnest(types) type 
                       GROUP BY type
                       """,
            "all",
        )

    def get_total_count(self):
        return self._run_query("SELECT COUNT(*) FROM pokemon", "one")[0]
