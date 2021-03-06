import pymysql


from pymysql.cursors import DictCursor
from contextlib import closing
from vk_bot.core.sql.vksql import auth
from vk_bot.config import *
conn = auth()
with conn.cursor() as cursor:
    query = "CREATE TABLE IF NOT EXISTS admins (id int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS ban (id int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS {} (id int)".format(tablechat)
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS prefix (id int, name varchar(40))"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS smehgen (id int, count int, smeh varchar(40), smehslova varchar(40))"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS prefix (id int, name varchar(40))"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS {} (id int)".format(chathello)
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS relation (id int, id2 int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS vips (id int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS yourphoto (id int, command varchar(40), public varchar(666), number int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS yourgroup (id int, command varchar(40), public varchar(666), number int)"
    cursor.execute(query)
    query = "CREATE TABLE IF NOT EXISTS economy (id int, money int)"
    cursor.execute(query)
    conn.commit()
    query = "CREATE TABLE IF NOT EXISTS quotes (uid int, yourtext varchar(80), text varchar(80))"
    cursor.execute(query)
    conn.commit()
