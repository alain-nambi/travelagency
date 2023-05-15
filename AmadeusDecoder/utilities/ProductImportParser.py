from AmadeusDecoder.models.invoice.Fee import Product
from AmadeusDecoder.models.invoice.Clients import Client
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


class CustomerParser():

    '''Class used when importing customer create from Odoo via csv file'''

    def import_customer(file):
        df = pd.read_csv(file, encoding='utf-8', sep=';')
        df.replace({np.nan: None}, inplace=True)
        for index, row in df.iterrows():
            odoo_id, customer_type, intitule, telephone, mail, address, city, zipcode, country, customer_id = row['odoo_id'], 'Société' if row['is_company'] == True else 'Particulier', row['name'], row['phone'], row['email'], row['street2'], row['city'], row['zip'], row['country'], row['gpnr_id']

            customer = Client.objects.filter(odoo_id=odoo_id)

            if customer.exists():
                if customer_id is not None and customer.filter(pk=customer_id).exists():
                    customer.update(intitule=intitule, type=customer_type, address_1=address, city=city, country=country, telephone=telephone, email=mail, code_postal=zipcode)
                elif customer_id is not None and customer.filter(pk=customer_id).exists():
                    new_customer = Client(intitule=intitule, type=customer_type, address_1=address, city=city, country=country, telephone=telephone, email=mail, code_postal=zipcode)
                    new_customer.save()
            elif customer_id is not None and not customer.exists() and customer.filter(pk=customer_id).exists():
                new_customer = Client(intitule=intitule, type=customer_type, address_1=address, city=city, country=country, telephone=telephone, email=mail, code_postal=zipcode)
                new_customer.save()

