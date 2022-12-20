import sqlite3
from django.conf import settings

DB_SETTINGS = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/maxim/PycharmProjects/coffeeShop/coffeeShop/db.sqlite3',
    }

class BaseManager:
    connection = None

    @classmethod
    def set_connection(cls, database_settings=DB_SETTINGS):
        connection = sqlite3.connect(database_settings['NAME'])
        cls.connection = connection

    @classmethod
    def _get_cursor(cls):
        return cls.connection.cursor()

    @classmethod
    def _execute_query(cls, query, params=None):
        cursor = cls._get_cursor()
        cursor.execute(query, params)

    def __init__(self, model_class):
        self.model_class = model_class

    def select(self, *field_names, chunk_size=2000):
        # Build SELECT query
        fields_format = ', '.join(field_names) if field_names else '*'
        query = f"SELECT {fields_format} FROM {self.model_class.table_name}"

        # Execute query
        cursor = self._get_cursor()
        cursor.execute(query)

        # Fetch data obtained with the previous query execution
        # and transform it into `model_class` objects.
        # The fetching is done by batches of `chunk_size` to
        # avoid to run out of memory.
        model_objects = list()
        is_fetching_completed = False
        while not is_fetching_completed:
            result = cursor.fetchmany(size=chunk_size)
            for row_values in result:
                keys, values = field_names, row_values
                row_data = dict(zip(keys, values))
                model_objects.append(self.model_class(**row_data))
            is_fetching_completed = len(result) < chunk_size

        return model_objects

    def bulk_insert(self, rows: list):
        # Build INSERT query and params:
        field_names = rows[0].keys()
        assert all(row.keys() == field_names for row in rows[1:])  # confirm that all rows have the same fields

        fields_format = ", ".join(field_names)
        values_placeholder_format = ", ".join([f'({", ".join(["%s"] * len(field_names))})'] * len(rows))

        query = f"INSERT INTO {self.model_class.table_name} ({fields_format}) " \
                f"VALUES {values_placeholder_format}"

        params = list()
        for row in rows:
            row_values = [row[field_name] for field_name in field_names]
            params += row_values

        # Execute query
        self._execute_query(query, params)

    def update(self, new_data: dict):
        # Build UPDATE query and params
        field_names = new_data.keys()
        placeholder_format = ', '.join([f'{field_name} = %s' for field_name in field_names])
        query = f"UPDATE {self.model_class.table_name} SET {placeholder_format}"
        params = list(new_data.values())

        # Execute query
        self._execute_query(query, params)

    def delete(self):
        # Build DELETE query
        query = f"DELETE FROM {self.model_class.table_name} "

        # Execute query
        self._execute_query(query)

    @classmethod
    def disconnect(self):
        self.connection.close()

BaseManager.set_connection()

class MetaModel(type):
    manager_class = BaseManager

    def _get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def objects(cls):
        return cls._get_manager()


class BaseModel(metaclass=MetaModel):
    table_name = ""

    def __init__(self, **row_data):
        for field_name, value in row_data.items():
            setattr(self, field_name, value)

    def __repr__(self):
        attrs_format = ", ".join([f'{field}={value}' for field, value in self.__dict__.items()])
        return f"<{self.__class__.__name__}: ({attrs_format})>\n"

class Coffee(BaseModel):
    table_name = 'human'
    manager_class = BaseManager

cof = Coffee.objects.select()
print(cof)
BaseManager.disconnect()
