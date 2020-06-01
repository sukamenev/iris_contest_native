import sys
import config
from iglobal import iGlobal, getIris

import random
from random import seed
from random import randint

import time

# global ^catalog
c = iGlobal('catalog')
c.kill()

c.init(
  {'Storages':
     { 'id' : 1,
       'Properties':
        {'capacity':
           {'name': 'Capacity, GB',
            'sort': 100,
            'searchable': 1,
            'table_view': 1
           },
         'weight':
           {'name': 'Weight, kg',
            'sort': 800,
            'searchable': 1,
            'table_view': 1
           },
         'product_brief':
           {'name': 'Capacity, GB',
            'sort': 900,
            'searchable': 1,
            'table_view': 0
           }
       },
      'SSD':
        {'id' : 2,
         'Properties':
          {'endurance':
            {'name': 'Endurance, TBW',
             'sort': 200,
             'searchable': 1,
             'table_view': 1
            }
          },
         'AIC PCI-E': {'id': 3},
         'SATA':      {'id': 4},
         'M.2':       {'id': 5}
      },
      'HDD':
        {'id' : 6,
          'Properties':
          {'rpm':
            {'name': 'Rotate speed, RPM',
             'sort': 250,
             'searchable': 1,
             'table_view': 1
            }
          },
         'SAS':
           {'id' : 7},
         'SATA':
           {'id' : 8,
            'Properties':
            {'version':
              {'name': 'Version',
               'sort': 300,
               'searchable': 1,
               'table_view': 1
              }
            }
          }
        }
      }
    }          
)
              
index = iGlobal('index')
index.kill()

index.init(
 {
  'path': {
    1: "Storages",
    2: "Storages|SSD",
    3: "Storages|HDD",
    4: "Storages|SSD|AIC PCI-E",
    5: "Storages|SSD|SATA",
    6: "Storages|SSD|M.2",
    7: "Storages|HDD|SAS",
    8: "Storages|HDD|SATA"
  },
  'prop': {
    1: "capacity|weight|product_brief",
    2: "capacity|weight|product_brief|endurance",
    3: "capacity|weight|product_brief|rpm",
    4: "capacity|weight|product_brief|endurance",
    5: "capacity|weight|product_brief|endurance",
    6: "capacity|weight|product_brief|endurance",
    7: "capacity|weight|product_brief|rpm",
    8: "capacity|weight|product_brief|rpm|version"
  }
 }
)

# У нас есть список каталогов в которых мы создаём товары
# Выбираем каталог и создаём в нём товар с нужным списком свойств
aList = [4, 5, 6, 7, 8]
nTest = 300

print()
start = time.time()
print("IRIS native globals: adding of {0} goods".format(nTest))


good = iGlobal('good')
good.kill()

seed(1)
iris = getIris()

for x in range(nTest):
  nCatalog = random.choice(aList)
  aP = index.node('prop', nCatalog).get().split('|')
  for p in aP:
    id = x+1
    oGood = good.node(id)
    randomNumber = randint(0, 10000)
    iris.tStart()
    if p=='product_brief':
      oGood.node(p).set('Text value ' + str(id))
    else:
      oGood.node(p).set(randomNumber)
      
    oGood.node('name').set('Name ' + str(id))
    oGood.node('price').set(randomNumber/100)
    oGood.node('item_count').set(randomNumber)
    oGood.node('reserved_count').set(0)
    oGood.node('catalog').set(nCatalog)
    iris.tCommit()

end = time.time()
print('Total time {:.2f} sec'.format(end - start))
print()
    
# Теперь напишем процедуру, которая делает аналогичную встравку для MySql
#import mysql.connector
#from mysql.connector import Error

import pymysql

cacheProp = {
  1: [1, 2, 3],
  2: [1, 2, 3, 4],
  3: [1, 2, 3, 5],
  4: [1, 2, 3, 4],
  5: [1, 2, 3, 4],
  6: [1, 2, 3, 4],
  7: [1, 2, 3, 5],
  8: [1, 2, 3, 5, 6]
}

print("EAV (MySql backend): adding of {0} goods".format(nTest))

db = pymysql.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_DB)

cursor = db.cursor()

cursor.execute('DELETE FROM Good')
cursor.execute('DELETE FROM TextValues')
cursor.execute('DELETE FROM NumberValues')

for x in range(nTest):
  randomNumber = randint(0, 10000)
  nCatalog = random.choice(aList)
  id = x+1
  
  sSql = "INSERT INTO `Good` (`id`, `name`, `price`, `item_count`, `reserved_count`, `catalog_id`) VALUES (%s, %s, %s, %s, %s, %s)"
  cursor.execute(sSql, (id, 'Name ' + str(id), randomNumber/100, randomNumber, randomNumber, randomNumber))
  
  sSql = "INSERT INTO `TextValues` (`good_id`, `field_id`, `fValue`) VALUES (%s, %s, %s)"
  cursor.execute(sSql, (id, 2, 'Text value ' + str(id)))
  
  aP = cacheProp[nCatalog]
  for p in aP:
    sSql = "INSERT INTO `NumberValues` (`good_id`, `field_id`, `fValue`) VALUES (%s, %s, %s)"
    cursor.execute(sSql, (id, p, randomNumber))
  
  db.commit()
  
end = time.time()
print('Total time {:.2f} sec'.format(end - start))
print()

db.close()        
