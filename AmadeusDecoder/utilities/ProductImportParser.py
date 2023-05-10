from AmadeusDecoder.models.invoice.Fee import Product
import pandas as pd
import numpy as np

class ProductParser():

    '''class used when import product from Odoo in fees'''

    def import_product(file):
        is_deleted = False
        df = pd.read_csv(file, encoding='utf-8', sep=';')
        df.replace({np.nan: None}, inplace=True)
        for index, row in df.iterrows():
            product_id, designation, code, cost, status, type = row['id'], row['name'] , row['code'] , row['price'], row['active'], row['deleted']
            product = Product.objects.filter(product_id=product_id)
            if status == "1":
                is_deleted = True
            if product.exists():
                if not is_deleted:
                    product.update(designation=designation, code=code, cost=cost, tax=0, total=cost, type=type)
                else:
                    product.delete()
            else:
                new_product = Product(designation=designation, code=code, cost=cost, tax=0, total=cost, product_id=product_id, type=type)
                new_product.save()


class CustomerParse():

    '''Class used when importing customer create from Odoo via csv file'''

    def import_customer(file):
        return None