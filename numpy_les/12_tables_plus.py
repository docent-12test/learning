import numpy as np
import numpy.lib.recfunctions as rfn

companies = np.array([('Comp_A', 'Vlas & Co', 'Landbouw'),
                      ('Comp_D', 'Koren en Zonen', 'Landbouw'),
                      ('Comp_C','Koe en Kalf', 'Veeteelt') ,
                      ('Comp_B','Vos en Kip', 'Veeteelt')],
                     dtype=[('Company', 'U20'), ('Name', 'U20'), ('Sector', 'U20')])
print(companies)
print(companies['Sector' == 'Veeteelt'])  # fout
print(companies[companies['Sector'] == 'Veeteelt'])


m_type= [
    ("Company", "U20"),
    ("Mon", "f8"),
    ("Tue", "f8"),
    ("Wed", "f8"),
    ("Thu", "f8"),
    ("Fri", "f8"),
    ("Sat", "f8"),
    ("Sun", "f8"),
    ("Invoice","f8")
]
m = np.array(
    [('Comp_A', 1000, 1015, 1020 , 1050, 1120, 1121, 1125,0),
       ('Comp_C',   3450,  3456,  4323 ,  4323,  4340,   3000,   4340,0),
       ('Comp_B',  501, 500, 491, 492, 500, 499, 499,0),
       ('Comp_D',  90, 80, 70 , 60,30, 20 ,15,0)],
      dtype=m_type)



print("stijgend in weekend")
print(m[(m['Sun'] >  m['Fri'])])
print("dalend in week")
print(m[(m['Mon'] >=  m['Tue']) & (m['Tue'] >=  m['Wed']) & (m['Wed'] >=  m['Thu']) & (m['Thu'] >=  m['Fri'])])


m['Invoice'] = m['Sun'] - m['Mon']
print('basis factuur')
print(m)

print("boete voor weekend verbruik")
m['Invoice'] = np.where(m['Sun'] >  m['Fri'],m['Invoice']+10, m['Invoice'])
print(m)
print("10% korting voor wie in week alleen produceert")
m['Invoice'] = np.where((m['Mon'] >=  m['Tue']) & (m['Tue'] >=  m['Wed']) & (m['Wed'] >=  m['Thu']) & (m['Thu'] >=  m['Fri']),m['Invoice']*0.9, m['Invoice'])
print(m)


invoices = rfn.rec_join('Company',companies, m, jointype='inner')

for row in invoices:
    print(row )# print(rfn.rec_join('c_id', , courses, jointype='inner'))


i_rec = np.rec.array(invoices)
print(i_rec)
i_rec.Invoice *=10
i_rec.Company = np.char.upper(i_rec.Company )

print(i_rec)




