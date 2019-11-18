import argparse
import configparser
import os.path
import psycopg2
from psycopg2 import sql

def make_story_table(cur):
    cur.execute("""
        CREATE TABLE story (
            id SERIAL PRIMARY KEY,
            title TEXT,
            url TEXT UNIQUE NOT NULL,
            html TEXT NOT NULL,
            descript TEXT,
            pub_date timestamp
        );
    """)

def make_writer_table(cur):
    cur.execute("""
        CREATE TABLE writer (
            id SERIAL PRIMARY KEY,
            name text
        );
    """)

def make_topic_table(cur):
    cur.execute("""
        CREATE TABLE topic (
            id SERIAL PRIMARY KEY,
            parent INTEGER,
            name text
        );
    """)

def make_authored_table(cur):
    cur.execute("""
        CREATE TABLE authored (
            story_id INTEGER NOT NULL REFERENCES story(id),
            writer_id INTEGER NOT NULL REFERENCES writer(id),
            PRIMARY KEY(story_id, writer_id)
        );
    """)

def make_topic_map(cur):
    cur.execute("""
        CREATE TABLE story_topic (
            story_id INTEGER NOT NULL REFERENCES story(id),
            topic_id INTEGER NOT NULL REFERENCES topic(id),
            PRIMARY KEY(story_id, topic_id)
        );
    """)

if __name__ == '__main__':
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-', '--config', type=str, default='tlappas_linux_db.conf',
        help='Creates database to store news story data. \
        Default is "create_db.conf".')
    
    args = parser.parse_args()
    conf_file = args.config

    # Find project folder
    proj_path = os.path.normpath(os.path.normcase(os.path.dirname(
        os.path.abspath(__file__))))
    try:
        proj_path = os.path.join(proj_path[:proj_path.index('src')-1])
    except:
        proj_path = ''

    # Read config values
    # Connect to database
    config = configparser.ConfigParser()
    config.read(os.path.join(proj_path, 'config', conf_file))
    default_db = config['db-params']['default-db']
    user = config['db-params']['user']
    db_name = config['db-params']['news-db']
    host = config['db-params']['host']
    passwd = config['db-params']['passwd']
    
    # TODO: Add additional processing for connectoin strings that require a 
    #   password.

    # Assume we can connect to the user's default database
    #   with the current user credentials 
    conn = psycopg2.connect('dbname={} user={} host={}'.format(default_db,
        user, host))

    # Create database
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    cur.execute(sql.SQL('CREATE DATABASE {};').format(sql.Identifier(db_name)))
    cur.close()
    conn.close()

    # Connect to the new database
    conn = psycopg2.connect('dbname={} user={} host={}'.format(db_name,
        user, host))
    cur = conn.cursor()

    # Add tables
    make_story_table(cur)
    make_writer_table(cur)
    make_topic_table(cur)
    make_authored_table(cur)
    make_topic_map(cur)

    cur.close()
    conn.commit()
    conn.close()