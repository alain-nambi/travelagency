from django.test import TestCase
from AmadeusDecoder.models.user.Users import Office, User
from AmadeusDecoder.models.pnr.Pnr import Pnr
from AmadeusDecoder.models.pnr.Currency import Currency
from AmadeusDecoder.models.pnr.Contact import Contact
from AmadeusDecoder.models.pnr.Passenger import Passenger
from AmadeusDecoder.models.pnr.PnrPassenger import PnrPassenger
from AmadeusDecoder.models.invoice.Invoice import Invoice
from AmadeusDecoder.models.invoice.InvoiceDetails import InvoiceDetails

# Create your tests here
class CRUDTestCase(TestCase):
    
    def setUp(self):
        # Offices
        office1 = Office(name='Office 1', location='Office 1 location')
        office1.save()
        office2 = Office(name='Office 2', location='Office 2 location')
        office2.save()
        # Users
        admin = User(name='MGBI 1', surname='', username='admin', password='032984530257-1984', birth_date='2000-08-30', type='Administrateur')
        admin.save()
        manager1 = User(name='Manager', surname='1', username='manage1', password='032984530257-1984', birth_date='2000-08-30', type='Manager')
        manager1.save()
        manager2 = User(name='Manager', surname='2', username='manage2', password='032984530257-1984', birth_date='2000-08-30', type='Manager')
        manager2.save()
        control_agent = User(name='Controller', surname='', username='controller', password='032984530257-1984', birth_date='2000-08-30', type='Contrôleur')
        control_agent.save()
        affair_center_agent = User(name='Affair', surname='Center', username='affair', password='032984530257-1984', birth_date='2000-08-30', type='Centre Affaire')
        affair_center_agent.save()
        
        user2 = User(office=office1, name='USER 1', surname='user 1', username='user1', password='032984530257-1984', birth_date='2000-08-30', type='Agent de comptoir')
        user2.save()
        user3 = User(office=office1, name='USER 2', surname='user 2', username='user2', password='032984530257-1984', birth_date='2000-08-30', type='Agent de comptoir')
        user3.save()
        user4 = User(office=office2, name='USER 3', surname='user 3', username='user3', password='032984530257-1984', birth_date='2000-08-30', type='Agent de comptoir')
        user4.save()
        cashier1 = User(office=office1, name='CASHIER 1', surname='cashier 1', username='cashier1', password='032984530257-1984', birth_date='2000-08-30', type='Caisse')
        cashier1.save()
        cashier2 = User(office=office2, name='CASHIER 2', surname='cashier 2', username='cashier2', password='032984530257-1984', birth_date='2000-08-30', type='Caisse')
        cashier2.save()
        cashier3 = User(office=office2, name='CASHIER 3', surname='cashier 3', username='cashier3', password='032984530257-1984', birth_date='2000-08-30', type='Caisse')
        cashier3.save()
        
        #currency
        currency = Currency(name='Euro', code='EUR')
        currency.save()
        # pnr
        currency = Currency.objects.get(code='EUR')
        pnr1 = Pnr(agent=user2, state='', number='UBZ0IO', creationdate='2022-08-25', type='ALTEA', currency=currency)
        pnr1.save()
        pnr2 = Pnr(agent=user2, state='', number='UBZ0I3', creationdate='2022-08-25', type='ALTEA', currency=currency)
        pnr2.save()
        pnr3 = Pnr(agent=user4, state='', number='UBZ0I2', creationdate='2022-08-25', type='ALTEA', currency=currency)
        pnr3.save()
        pnr4 = Pnr(state='', number='UBZ0II', creationdate='2022-08-25', type='ALTEA', currency=currency, 
                   otherinformations=['BILLETS NON REMMBOURSABLES ET MODIFIABLES AVEC FRAIS', 'BILLETS NON REMBOURSABLES ET NON MODIFIABLES SI NO SHOW', 'NO SHOW= NON PRESENTATION A L ENREGISTREMENT DES VOLS RESERVES'],
                   ssr={'meal-P1': 'MEAL', 'luggage': '10Kg'})
        pnr4.save()
        # contact
        contact1 = Contact(pnr=pnr1, contacttype='Email', value='pnr1@gmail.com', owner='owner1')
        contact1.save()
        contact2 = Contact(pnr=pnr1, contacttype='Phone', value='pnr1@gmail.com', owner='owner2')
        contact2.save()
        contact3 = Contact(pnr=pnr2, contacttype='Email', value='pnr2@gmail.com', owner='owner3')
        contact3.save()
        contact4 = Contact(pnr=pnr3, contacttype='Email', value='pnr3@gmail.com', owner='owner4')
        contact4.save()
        # passengers
        passenger1 = Passenger(name='SILVA', surname='ARNALDO', designation='MR')
        passenger1.save()
        passenger2 = Passenger(name='SILVA', surname='MATHIAS', designation='MR')
        passenger2.save()
        passenger3 = Passenger(name='BOUCHAUD', surname='LEONE', designation='MR')
        passenger3.save()
        passenger4 = Passenger(name='ANNA', surname='MARIA', designation='MR')
        passenger4.save()
        passenger5 = Passenger(name='GEORGES', surname='LUCAS', designation='MR')
        passenger5.save()
        pnr_pass_assoc1 = PnrPassenger(pnr=pnr1, passenger=passenger1)
        pnr_pass_assoc1.save()
        pnr_pass_assoc2 = PnrPassenger(pnr=pnr1, passenger=passenger2)
        pnr_pass_assoc2.save()
        pnr_pass_assoc3 = PnrPassenger(pnr=pnr2, passenger=passenger3)
        pnr_pass_assoc3.save()
        pnr_pass_assoc4 = PnrPassenger(pnr=pnr3, passenger=passenger4)
        pnr_pass_assoc4.save()
        pnr_pass_assoc5 = PnrPassenger(pnr=pnr4, passenger=passenger5)
        pnr_pass_assoc5.save()
        # invoice
        invoice1 = Invoice(pnr=pnr1, transmitter='TravelAgency', follower=user2, reference='orderX')
        invoice1.save()
        invoice_detail1 = InvoiceDetails(invoice=invoice1)
        invoice_detail1.save()
        invoice2 = Invoice(pnr=pnr2, transmitter='TravelAgency', follower=user2, reference='orderX')
        invoice2.save()
        invoice_detail2 = InvoiceDetails(invoice=invoice2)
        invoice_detail2.save()
        invoice3 = Invoice(pnr=pnr3, transmitter='TravelAgency', follower=user2, reference='orderX')
        invoice3.save()
        invoice_detail3 = InvoiceDetails(invoice=invoice3)
        invoice_detail3.save()
        invoice4 = Invoice(pnr=pnr4, transmitter='TravelAgency', follower=user2, reference='orderX')
        invoice4.save()
        invoice_detail4 = InvoiceDetails(invoice=invoice4)
        invoice_detail4.save()
        
    
    def users_test(self):
        # Test users and office's relation
        user_with_no_office = User.objects.first()
        self.assertIsNone(user_with_no_office.office)
        user_with_office = User.objects.get(id=6)
        self.assertIsNotNone(user_with_office.office)
        # Test office and users' relation
        office = Office.objects.select_related().first()
        self.assertEqual(len(office.users.all()), 3)
        self.assertEqual(office.users.first().name, 'USER 1')
    
    def pnr_test(self):
        # pnr
        pnr = Pnr.objects.get(ssr__contains={'meal-P1': 'MEAL'})
        self.assertEqual(pnr.number, 'UBZ0II')
        self.assertTrue(pnr.otherinformations[1] == 'BILLETS NON REMBOURSABLES ET NON MODIFIABLES SI NO SHOW')
        # pnr and agent
        agent = User.objects.get(name='USER 1')
        self.assertQuerysetEqual(agent.pnrs.all(), [Pnr.objects.get(number='UBZ0I3'), Pnr.objects.get(number='UBZ0IO')], ordered=False)
        self.assertQuerysetEqual(User.objects.filter(type='Manager').first().pnrs.all(), [])
        pnr = Pnr.objects.get(number='UBZ0I2')
        self.assertEqual(pnr.agent.name, 'USER 3')
        # pnr and currency
        currency = Currency.objects.get(code='EUR')
        self.assertEqual(len(currency.pnrs.all()), 4)
        self.assertEqual(pnr.currency.code, 'EUR')
        # pnr and contact
        pnr1 = Pnr.objects.get(number='UBZ0IO')
        self.assertEqual(pnr.contacts.all()[0].value, 'pnr3@gmail.com')
        self.assertEqual(len(pnr1.contacts.all()), 2)
        # pnr and passengers
        self.assertEqual(len(pnr1.passengers.all()), 2)
        self.assertEqual(pnr1.passengers.first().passenger.name, 'SILVA')
        # pnr and invoice
        self.assertEqual(pnr1.invoice.detail.total, 0)
        
    def test(self):
        self.users_test()
        self.pnr_test()

        
        