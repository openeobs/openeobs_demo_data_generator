from passlib.context import CryptContext
import psycopg2


class ChangeAdminPassword(object):

    def __init__(self, database, password_string, admin_password):
        new_pass = CryptContext(['pbkdf2_sha512']).encrypt(password_string)
        conn_string = "host='localhost' dbname={db} user='odoo' " \
                      "password='{password}'".format(db=database,
                                                     password=admin_password)
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE res_users SET password_crypt='{password}' "
            "WHERE id=1;".format(password=new_pass)
        )

