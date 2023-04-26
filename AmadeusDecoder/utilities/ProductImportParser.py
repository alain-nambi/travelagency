from AmadeusDecoder.models.invoice.Fee import Product
import pandas as pd
import numpy as np

class ProductParser():

    '''class used when import product from Odoo in fees'''

    def import_product(file):
        is_deleted = False
        df = pd.read_csv(file, dtype=str, encoding='utf-8', sep=';')
        df.replace({np.nan: None}, inplace=True)
        for i, j in df.iterrows():
            product_id, designation, code, cost, status, type = j[0], j[1] , j[2] , j[3], j[5], j[6]
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