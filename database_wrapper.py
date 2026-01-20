import pymysql

class DatabaseWrapper:

    def __init__(self, host, user, password, database, port):
        self.db_config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': int(port), 
            'cursorclass': pymysql.cursors.DictCursor
        }
        self.create_table()

    def connect(self):
        return pymysql.connect(**self.db_config)

    def execute_query(self, query, params=()):
        conn = self.connect()
        last_id = None
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                # Catturiamo l'ID dell'ultimo inserimento
                last_id = cursor.lastrowid
        finally:
            conn.close()
        return last_id

    def fetch_query(self, query, params=()):
        conn = self.connect()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
            return result
        finally:
            conn.close()
    
    # --- METODI SPECIFICI ---

    def create_table(self):
        self.execute_query('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                completed BOOLEAN DEFAULT FALSE
            )
        ''')

    def get_tasks(self):
        tasks = self.fetch_query("SELECT * FROM tasks")
        # Conversione per compatibilità JSON
        for task in tasks:
            task['completed'] = bool(task['completed'])
        return tasks

    def add_task(self, title):
        # Ora restituisce l'ID creato
        return self.execute_query(
            "INSERT INTO tasks (title, completed) VALUES (%s, %s)", 
            (title, False)
        )

    def delete_task(self, task_id):
        self.execute_query(
            "DELETE FROM tasks WHERE id = %s", 
            (task_id,)
        )


    def toggle_task(self, task_id, completed):
        self.execute_query(
            "UPDATE tasks SET completed = %s WHERE id = %s",
            (completed, task_id)
        )