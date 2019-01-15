class db:
    __initstr = '''
    CREATE TABLE actors (
        code INTEGER PRIMARY KEY,
        name TEXT,
        surname TEXT,
        secname TEXT,
        rank TEXT,
        experience TEXT
    );

    CREATE TABLE perfs (
        code INTEGER PRIMARY KEY,
        name TEXT,
        year TEXT,
        budget TEXT
    );

    CREATE TABLE emaips (
        id INTEGER PRIMARY KEY,
        perf TEXT,
        actorid TEXT,
        cost TEXT,
        role TEXT
    );
    '''

    __get_actor = 'SELECT * FROM actors;'
    __get_perf  = 'SELECT * FROM perfs;'
    __get_emaip = 'SELECT * FROM emaips;'

    __set_actor = '''
    INSERT INTO actors (name,
        surname,
        secname,
        rank,
        experience)
        VALUES (:1, :2, :3, :4, :5)
        ON CONFLICT DO UPDATE SET name=:1,
            surname=:2,
            secname=:3,
            rank=:4,
            experience=:5;
    '''
    __set_perf = '''
    '''
    __set_emaip = '''
    '''

    def __init__(self, actors, perfs, emaips):
        self.__clients = __clients
        pass

    def read(self, path):
        pass

    def write(self, path):
        pass

