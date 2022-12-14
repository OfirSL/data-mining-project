import argparse
import logging
import pymysql
from googletrans import LANGUAGES
# ____internal modules____
from common import read_from_config
from common import connection
from common import translate
import getting_shufersal_links
import database
import page_scraper

logging.basicConfig(filename='main.log',
                    format='%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s',
                    level=logging.INFO)

MYSQL_USER = read_from_config('MYSQL_USER')
MYSQL_PASSWORD = read_from_config('MYSQL_PASSWORD')
DATABASE_NAME = read_from_config('DATABASE_NAME')


def delete_database(user, password):
    """'delete_database' asks the client to delete the 'shufersal' database and if positive it deletes it."""
    delete_database_q = input(f"this will delete the existing '{DATABASE_NAME}' database, to proceed? [y/n]")
    if delete_database_q == 'y':
        try:
            database.delete_database(user, password, DATABASE_NAME)
            print(f'"{DATABASE_NAME}" database was deleted successfully.')
            logging.info(f'"{DATABASE_NAME}" database was deleted successfully: %s')
        except pymysql.err.OperationalError:
            print(f"Can't delete {DATABASE_NAME} database because it doesn't exist")
            logging.warning(f"Can't delete {DATABASE_NAME} database because it doesn't exist: %s")
            return
    elif delete_database_q == 'n':
        return
    else:
        delete_database(user, password)


def build_shufersal_tables(user, password):
    """'build_shufersal_database' creates the 'shufersal' database."""
    try:
        database.main(user, password)
        print(f'"{DATABASE_NAME}" database was created successfully.')
        logging.info(f'database was created successfully: %s')
    except pymysql.err.ProgrammingError:
        logging.warning(f'"{DATABASE_NAME}" database was not created successfully %s')
        raise pymysql.err.ProgrammingError


def check_sql_connection(user, password):
    try:
        connection(user, password)
        logging.info(f'MySQL connection established: %s', user)
        return True
    except pymysql.err.OperationalError:
        logging.critical(f'no MySQL connection established: %s', user)
        return False


def main():
    parser = argparse.ArgumentParser(description="""Welcome to the Shufersal scraper!
    the Shufersal scraper enables the user to scrab the data 
    from the online supermarket site of the Shufersal chain: https://www.shufersal.co.il""")

    parser.add_argument('-user', help='user name to mySQL data server')
    parser.add_argument('-password', help='password to mySQL data server')
    parser.add_argument('-url', help=f'specific category url from the "{DATABASE_NAME}" online site to parse and '
                        f'collect to the {DATABASE_NAME} database')
    parser.add_argument('-translate', nargs=3, metavar=('TABLE', 'COLUMN', 'LANGUAGE=ENGLISH'),
                        help=f'specific table and column from the "{DATABASE_NAME}" database to translate to '
                        f'the desired language (english by default). To see the available languages insert languages'
                             f' as the argument for LANGUAGE')
    parser.add_argument('-gl', action='store_true', help=f'get subcategories links to parse and fill category'
                        f' table')
    parser.add_argument('-all', action='store_true', help=f'get all links from category table, parse and fill'
                        f' "{DATABASE_NAME}" database')
    parser.add_argument('-c', action='store_true', help=f'create "{DATABASE_NAME}" database')
    parser.add_argument('-dc', action='store_true', help=f'delete existing "{DATABASE_NAME}"'
                        f' database and creating a new one')
    parser.add_argument('-d', action='store_true', help=f'delete "{DATABASE_NAME}" database')

    args = parser.parse_args()
    user = MYSQL_USER
    password = MYSQL_PASSWORD

    if check_sql_connection(user, password):
        logging.info(f'mySQL connection checkpoint: login completed successfully.')

        if args.d:
            delete_database(user, password)
            logging.info(f'Client successfully deleted the "shufersal" database: %s')

        if args.dc:
            delete_database(user, password)
            logging.info(f'Client successfully deleted the "shufersal" database: %s')
            try:
                build_shufersal_database(user, password)
                logging.info(f'Client successfully created a new "shufersal" database: %s')
            except pymysql.err.ProgrammingError:
                logging.warning(f'Client failed creating a new "shufersal" database: %s')
                return

        if args.c:
            try:
                build_shufersal_tables(user, password)
                logging.info(f'Client successfully created a new "shufersal" database: %s')
            except pymysql.err.ProgrammingError:
                logging.warning(f'Client failed creating a new "shufersal" database: %s')
                return

        if args.gl:
            print("Getting subcategories' links to parse")
            logging.info("Getting subcategories' links to parse")
            if database.check_database(user, password, DATABASE_NAME):
                getting_shufersal_links.get_urls(user, password)
                logging.info(f'Client succeeded generating the subcategories links to parse and fill'
                             f' category table creating a new "shufersal" database: %s')
            else:
                logging.warning(f'Client failed generating the subcategories links to parse and fill'
                                f' category table creating a new "shufersal" database: %s')
                return

        if args.url:
            if database.check_database(user, password, DATABASE_NAME):
                page_scraper.parse_data(user, password, args.url)
                logging.info(f'Client succeeded specifying category url from the "shufersal" online'
                             f' site to parse and collect to the shufersal database: %s', args.url)
            else:
                logging.warning(f'Client failed specifying category url from the "shufersal" online'
                                f' site to parse and collect to the shufersal database: %s', args.url)
                return

        if args.all:
            if database.check_database(user, password, DATABASE_NAME):
                if getting_shufersal_links.check_urls(user, password):
                    page_scraper.parse_data(user, password)
                    logging.info(f'Client succeeded getting all the links from category table to parse'
                                 f' and fill "shufersal" database: %s')
            else:
                logging.warning(f'Client failed getting all the links from category table to parse'
                                f' and fill "shufersal" database: %s')
                return

        if args.translate:
            if args.translate[2] == 'languages':
                print(LANGUAGES)
            elif database.check_database(user, password, DATABASE_NAME):
                logging.info(f'Starting to translate table "{args.translate[0]}", column "{args.translate[1]}".')
                print(f'Starting to translate table "{args.translate[0]}", column "{args.translate[1]}".')
                translate(user, password, args.translate[0], args.translate[1], args.translate[2])
                print(f'Successful translation of table "{args.translate[0]}", column "{args.translate[1]}".')
                logging.info(f'Client succeeded specifying table, colum and datatype from the "shufersal"'
                             f' database to translate from hebrew to {args.translate[2]}: %s',
                             (args.translate[0], args.translate[1]), args.translate[2])
            else:
                logging.warning(f'Client failed specifying table, colum and datatype from the "shufersal"'
                                f' database to translate from hebrew to {args.translate[2]}: %s',
                                (args.translate[0], args.translate[1]), args.translate[2])
                print(f'Unsuccessful translation of table "{args.translate[0]}", column "{args.translate[1]}".')
                return


if __name__ == '__main__':
    main()
