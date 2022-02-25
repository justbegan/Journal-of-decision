from decision.models import *
from decision.views import *
#import pyodbc



def return_date_z(q):
    date_1 = str(q[5])
    date_1 = date_1.split(" ")
    return date_1[0]


def return_fio(query):
    fio = str(query[1]+" "+query[2]+" "+query[3])
    fio = fio.lower()
    fio = fio.title()
    return fio


def NVP_return_list(snils):
    pass
    # con = pyodbc.connect('DSN=ROS;UID=db2admin;PWD=DB2ljcneg')
    # snils = snils.replace("snils=", "")
    # snils = snils.replace("%20", " ")
    # query = "SELECT m.ra, m.fa, m.im, m.ot, coalesce(npt.name, '')  ||','|| coalesce(u.name, '') ||',дом '|| coalesce(trim(m.dom), '')||',корп. '|| coalesce(trim(m.kor), '') ||',кв. '|| coalesce(trim(m.kva), '')  as address, date(z.dz), z.nz " \
    #         "FROM PF.MAN as m left join kl.npt as npt on npt.re=16 and m.ra=npt.ra and m.punkt=npt.kod left join kl.ulica as u on u.re=16 and u.ra=m.ra and u.punkt=m.punkt and u.kod=m.ul left join (select id, dz, nz, rank() " \
    #         "OVER (PARTITION BY id ORDER BY dz DESC) AS RANK from pf.zajks) as z on z.id=m.id and z.rank=1 where m.npers ='"+snils+"'and m.pw=0"

    # cursor = con.cursor()
    # cursor.execute(query)
    # zz = cursor.fetchone()
    # return zz, return_fio(zz)






