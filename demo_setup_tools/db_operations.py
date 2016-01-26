import psycopg2


def refresh_materialized_views():
    conn = psycopg2.connect(dbname='nhclinical', user='odoo',
                            password='odoo')
    cursor = conn.cursor()
    cursor.execute("refresh materialized view ews0;")
    cursor.execute("refresh materialized view ews1;")
    cursor.execute("refresh materialized view ews1;")
    cursor.execute("refresh materialized view ward_locations;")
    cursor.execute("refresh materialized view param;")
    cursor.execute("refresh materialized view weight;")
    cursor.execute("refresh materialized view pbp;")




