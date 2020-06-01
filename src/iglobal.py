import irisnative
import atexit
import config

def getIris():
  global __IRIS_CONN, __IRIS
  if "__IRIS" in globals():
    return __IRIS
  
  __IRIS_CONN = irisnative.createConnection(config.IRIS_IP, config.IRIS_PORT, config.IRIS_NAMESPACE, config.IRIS_USER, config.IRIS_PASSWORD)
  __IRIS = irisnative.createIris(__IRIS_CONN)
  
  atexit.register(__IRIS_CONN.close)
  
  return __IRIS
  

class iGlobal:
  name = ""
  indices = ()

  def __init__(self, name, *indices):
    self.name = name
    self.indices = indices
    
  def __saveNode(self, d, a=[]):
    for k,v in d.items():        
      if isinstance(v, dict):
        b = a.copy()
        b.append(k)
        self.__saveNode(v, b)
      else:
        b = a.copy()
        b.append(k)
        b.insert(0, self.name)
        b.insert(0, v)
        i = getIris()
        i.set(*b)
    
  def init(self, tree):
    self.__saveNode(tree, *self.indices)
    
  def kill(self):
    i = getIris()
    return i.kill(self.name, *self.indices)
    
  def set(self, value):
    i = getIris()
    return i.set(value, self.name, *self.indices)
    
  def get(self):
    i = getIris()
    return i.get(self.name, *self.indices)
  
  def inc(self, value):
    i = getIris()
    return i.increment(value, self.name, *self.indices)
    
  def node(self, *ind):
    return iGlobal(self.name, *(self.indices + ind))
  
  def iterator(self):
    i = getIris()
    return i.iterator(self.name, *self.indices)
    
