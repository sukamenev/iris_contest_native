import sys
import config
from iglobal import iGlobal, getIris

import random
from random import seed
from random import randint

import time
import pymysql

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

# For MySQL relation catalog - properties
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

# Catalog list in which we'll create goods
aList = [4, 5, 6, 7, 8]
seed(1)
   
def runIrisAddTest(nTest):
  sRes =""

  start = time.time()
  sRes += "IRIS native globals: adding of {0} goods - ".format(nTest)

  good = iGlobal('good')
  good.kill()
  
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
  nTimeIrisCreate = end - start
  sRes += '{:.2f} sec'.format(nTimeIrisCreate)
  return nTimeIrisCreate
    
def runIrisReadTest(nTest):
  start = time.time()
  "IRIS native globals: access of {0} random goods - ".format(nTest)
  
  good = iGlobal('good')

  for x in range(nTest):
    id = randint(1, nTest)
    node = good.node(id)
    oIter = node.iterator()
    
    for subscript, value in oIter.items():
      "subscript= {}, value={}".format(subscript, value)

  end = time.time()
  nTimeIrisRead = end - start
  '{:.2f} sec'.format(nTimeIrisRead)
  
  return nTimeIrisRead

def runEAXAddTest(nTest):
  global cacheProp
  "EAV (MySql backend): adding of {0} goods - ".format(nTest)

#  db = pymysql.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_DB)
#  new version wants keywords
  db = pymysql.connect(host = config.MYSQL_HOST,
                       user=config.MYSQL_USER,
                       password=config.MYSQL_PASSWORD,
                       database=config.MYSQL_DB,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
  cursor = db.cursor()

  cursor.execute('DELETE FROM Good')
  cursor.execute('DELETE FROM TextValues')
  cursor.execute('DELETE FROM NumberValues')
  
  start = time.time()

  for x in range(nTest):
    randomNumber = randint(0, 10000)
    nCatalog = random.choice(aList)
    id = x+1
  
    sSql = "INSERT INTO `Good` (`id`, `name`, `price`, `item_count`, `reserved_count`, `catalog_id`) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(sSql, (id, 'Name ' + str(id), randomNumber/100, randomNumber, randomNumber, nCatalog))
  
    sSql = "INSERT INTO `TextValues` (`good_id`, `field_id`, `fValue`) VALUES (%s, %s, %s)"
    cursor.execute(sSql, (id, 2, 'Text value ' + str(id)))
  
    aP = cacheProp[nCatalog]
  
    for p in aP:
      sSql = "INSERT INTO `NumberValues` (`good_id`, `field_id`, `fValue`) VALUES (%s, %s, %s)"
      cursor.execute(sSql, (id, p, randomNumber))
  
    db.commit()
  
  end = time.time()
  nTimeEAXAdd = end - start

  return nTimeEAXAdd

def runEAXReadTest(nTest):
  global cacheProp
  
#  db = pymysql.connect(config.MYSQL_HOST, config.MYSQL_USER, config.MYSQL_PASSWORD, config.MYSQL_DB)
#  new version wants keywords
  db = pymysql.connect(host = config.MYSQL_HOST,
                       user=config.MYSQL_USER,
                       password=config.MYSQL_PASSWORD,
                       database=config.MYSQL_DB,
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)
  cursor = db.cursor()
  
  start = time.time()
  "EAV (MySql backend): access of {0} random goods - ".format(nTest)

  for x in range(nTest):
    id = randint(1, nTest)
  
    sSql = "SELECT * FROM `Good` WHERE `id`=%s"
    cursor.execute(sSql, (id))
    result = cursor.fetchone()
  
    sSql = "SELECT * FROM `NumberValues` WHERE `good_id`=%s"
    cursor.execute(sSql, (id))
    result = cursor.fetchall()
  
    sSql = "SELECT * FROM `TextValues` WHERE `good_id`=%s"
    cursor.execute(sSql, (id))
    result = cursor.fetchall()

  end = time.time()
  nTimeEAXRead = end - start
  db.close()
  
  '{:.2f} sec'.format(nTimeEAXRead)
  return nTimeEAXRead

