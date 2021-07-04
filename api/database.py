from peewee import *
import hashlib
from datetime import datetime

#database = MySQLDatabase('fast_db', )

#database = pymysql.connect(user='presta', password='pr3st4', host='127.0.0.1', port=3306, database='fast_db', cursorclass=pymysql.cursors.DictCursor, autocommit=True)

database = PostgresqlDatabase('fast_db', host='localhost', port=5432, user='postgres', password='postgres')

class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'users'

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))

        return h.hexdigest()

class Movie(Model):
    title = CharField(max_length=50, unique=True)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = 'movies'

class  UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    review = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

    class Meta:
        database = database
        table_name = 'user_reviews'

