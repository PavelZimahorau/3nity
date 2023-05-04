import pymysql
import configparser
import sys

def read_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config;

def get_connection():
    try:
        config = read_ini("Configuration/config.ini.py")

        connect = pymysql.connect(  host=config["DATABASE"]["HOST"],
                                    user=config["DATABASE"]["USERNAME"],
                                    password=config["DATABASE"]["PASSWORD"],
                                    db=config["DATABASE"]["DB"])

        print("Correct connection")
        return connect;
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Connectioon error: ", e)
        return None

def insert(connection, company_name, webSite):
    cur = connection.cursor()

    sql = """insert into `companies` (company_name, company_website)
             values (%s, %s) 
        """
    cur.execute(sql, (company_name, webSite))
    connection.commit()
    print("Record inserted")

def update(connection, company_name, newWebSite):
    cur = connection.cursor()

    sql = """update `companies` 
            set company_website = %s
             where  company_name = %s
        """
    cur.execute(sql, (newWebSite, company_name))
    connection.commit()
    print("Record Updated")

def delete(connection, company_name):
    cur = connection.cursor()

    sql = """delete from `companies` 
             where  company_name = %s
        """
    cur.execute(sql, (company_name))
    connection.commit()
    print("Record deleted")

def retriveCompanies(connection):
    cur = connection.cursor()
    sql = ('Select * from companies')
    cur.execute(sql)

    for row in cur.fetchall():
        print(row[0], " : ",  row[1], " : ", row[2])


connection = get_connection();
if (connection == None):
    sys.exit();

retriveCompanies(connection);
insert(connection, 'Google Inc', 'www.google.com')
retriveCompanies(connection);
update(connection, 'Google Inc', 'http://www.google.com')
retriveCompanies(connection);
delete(connection, 'Google Inc')
retriveCompanies(connection);