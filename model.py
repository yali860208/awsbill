# -*- coding: UTF-8 -*-

import psycopg2
import json
import pandas as pd
import sqlalchemy as db
import matplotlib.pyplot as plt
import seaborn as sns

def sum_unblendedcost(usageaccountid):
    select_sum = '''SELECT product_productname, SUM(lineitem_unblendedcost)
        FROM all_product
        WHERE lineitem_usageaccountid = '%s'
        GROUP BY product_productname
        ORDER BY SUM(lineitem_unblendedcost) DESC;'''

    conn = None
    try:
        DATABASE_URL = 'postgres://tgwuinlzrbtyxe:f135cb7410e86409876a69670c12606e91fc827f30cd36d9f5a9fa464652ba45@ec2-54-147-93-73.compute-1.amazonaws.com:5432/dfc32m0vmd0m5l'
        # return product and sum of cost for json
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        data = usageaccountid + '.0'
        cur.execute(select_sum, (float(data),))

        return_json = {}
        for i,j in cur.fetchall():
            return_json[i] = j
        # save the pie figure
        # SQL_order= SQL_order.format(data)
        # DATABASE_URL = "postgresql://tgwuinlzrbtyxe:f135cb7410e86409876a69670c12606e91fc827f30cd36d9f5a9fa464652ba45@ec2-54-147-93-73.compute-1.amazonaws.com:5432/dfc32m0vmd0m5l"
        # engine = db.create_engine(DATABASE_URL)

        df_prod = pd.read_sql(select_sum, con = conn,params = (float(data),))
        OrRd_palette = sns.color_palette("OrRd")
        plt.figure(figsize = (10,10))

        plt.pie(df_prod['sum'],
                labels = df_prod['product_productname'],
                autopct = "%1.3f%%",
                pctdistance = 0.6,
                textprops = {"fontsize" : 12},
                colors = OrRd_palette
            )
        plt.savefig('C:/Users/user/Desktop/github/awsbill/static/pie_cost.jpg')
                    # bbox_inches='tight',
                    # pad_inches=0.0)
        # json.dumps(return_json, indent=4)
        return json.dumps(return_json, indent=4)

        cur.close()

        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
