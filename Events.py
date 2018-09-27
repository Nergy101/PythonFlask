class loginFailedEvent: #timestamp, user(IP), triedPassword, failedCount,
  failedEventCount = 0;
  def __init__(self, timestamp, triedPassword):
    self.timestamp = timestamp
    self.triedPassword = triedPassword
    self.type = "loginFailedEvent"

  def Failed(self):
    self.failedEventCount += 1
    return self.failedEventCount

class loginSuccesEvent: #timestamp, user(IP), succesCounts
  SuccesEventCount = 0; # wann gemaakt is de count 0
  def __init__(self, timestamp):
    self.timestamp = timestamp
    self.type = "loginSuccesEvent"

  def Succes(self):
    self.SuccesEventCount += 1
    return self.SuccesEventCount
#
# class buttonPressedEvent:   #user(IP), timestamp, totalPushCount, buttonName, importance (by pushcount),
#   totalPushCount = 0
#   importance = 0
#   def __init__(self, buttonName, timestamp):
#     self.buttonName = buttonName
#     self.timestamp = timestamp
#
#   def Pushed(self):
#     self.totalPushCount += 1
#     return self.totalPushCount
#
#   def getImportance(self):
#     #bereken importance
#     #for now, pushcount in %
#     return ( (self.totalPushCount / 100) + 1) # percentage ??? iets idk

# class HackEvent:  #user(IP), timestamp, status(critical)
#   def __init__(self, name, age):
#     self.name = name
#     self.age = age
#
class pageVisitedEvent:
    totalVisitCount = 0
    def __init__(self, pageName, timestamp, ip):
        self.pageName = pageName
        self.timestamp = timestamp
        self.type = "pageVisitedEvent"
        self.ip = ip
    def Visited(self):
      self.totalVisitCount += 1
      return self.totalVisitCount