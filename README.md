# Comparison of IRIS Native Globals API and EAV-approach in relational db (MySQL)
![Logo: IRIS Native API and EAV-approach](https://community.intersystems.com/sites/default/files/inline/images/images/attention_last.png)
## About EAV-model
The EAV-model is designed to store hierarchical and sparse structures in relational databases.

The EAV-approach is widespread among programmers, but with the advent of IRIS Native API, is it worth using it further?

## My articles about EAV-model and IRIS globals

[Entity-attribute-value model in relational databases. Should globals be emulated on tables? Part 1.](https://community.intersystems.com/post/entity-attribute-value-model-relational-databases-should-globals-be-emulated-tables-part-1)

[Entity-attribute-value model in relational databases. Should globals be emulated on tables? Part 2.](https://community.intersystems.com/post/entity-attribute-value-model-relational-databases-should-globals-be-emulated-tables-part-2)

### Wikipedia

[About EAV-model](https://en.wikipedia.org/wiki/Entity%E2%80%93attribute%E2%80%93value_model)

## Purpose of this project

Make a comparison of the performance approaches on the numbers.
I want to see how much time it takes to create thousands of products, as well as to access them using IRIS Native API and EAV (MySQL).

## Data model in project

The structure of the demo data that we will store:

![The structure of the demo data](https://community.intersystems.com/sites/default/files/inline/images/images/data_structure1.png)

Global for this structure created in beginning [schema.py](src/schema.py).

SQL schema [schema.sql](src/schema.sql).

## Original tools inside my project

I created a great library in Python [iglobal.py](src/iglobal.py) that allows you to work with globals in an object-oriented way.

```
node = good.node('index1', 'index2')

node.set(5)
node.inc(2)
i = node.iterator()

print(node.get())

good.kill()
```

You may initialize whole tree with one operation:

```
good = iGlobal('good')

good.init(
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
      }
    }
  }
)
```

## Estimated container build time
First time running ~2-15 minutes. Depending on the speed of your internet.
After the 1st time running the next ones will perform better and take few seconds.

# Usage
## Build containers
```
docker-compose build
```

## Run containers
```
docker-compose up -d
```

## Run application

After starting containers open another terminal (under *root* user) and type commands:
```
docker ps
```

See IRIS container name (column NAMES)


```
# Go in IRIS container
docker exec -it IRIS_CONTAINER_NAME bash
# inside container
cd /app
python3 schema.py
```
