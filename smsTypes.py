class basicSms:
	 def __init__(self):
		 self.type = "none"
		 self.newBal = 0
		 self.day = 0
		 self.month = 0
		 self.year = 0
	 def setType(self,type):
		 self.type=type

	 def setNewBal(self,bal):
		 self.newBal=bal

	 def setDay(self,day):
		 self.day=day

	 def setMonth(self,month):
		 self.month=month

	 def setYear(self,year):
		 self.year=year

		 #get methods
	 def getType(self):
		 return self.type
	 def getNewBal(self):
		 return self.newBal
	 def getDay(self):
		 return self.day
	 def getMonth(self):
		 return self.month
	 def getYear(self):
		 return self.year

class sndCash(basicSms):
	 def setAmt(self,amt):
		 self.amt=amt
	 def setName(self,name):
		 self.receiverName=name
	 def setCost(self,cost):
		 self.cost=cost
		#get methods
	 def getAmt(self):
		 return self.amt
	 def getName(self):
		 return self.receiverName
	 def getCost(self):
		 return self.cost

class buyAirtm(basicSms):
	 def setAmt(self,amt):
		 self.amt=amt
	 def getAmt(self):
		 return self.amt

class withdraw(basicSms):
	 def setAmt(self,amt):
		 self.amt=amt
	 def getAmt(self):
		 return self.amt

class deposit(basicSms):
	 def setAmt(self,amt):
		 self.amt=amt
	 def getAmt(self):
		 return self.amt

class receive(basicSms):
	 def setAmt(self,amt):
		 self.amt=amt
	 def setSender(self,name):
		 self.name=name
	 #get methods
	 def getAmt(self):
		 return self.amt
	 def getSender(self):
		 return self.name

class inquiry(basicSms):
	 def getCost(self):
		 return self.cost
	 def getAmt(self):
		 return self.amt
	 def setCost(self,cost):
		 self.cost=cost
	 def setAmt(self,amt):
		 self.amt=amt

class bill(basicSms):
	 def getEntity(self):
		 return self.entity
	 def getAmt(self):
		 return self.amt
	 def setEntity(self,entity):
		 self.entity=entity
	 def setAmt(self,amt):
		 self.amt=amt
		 		 
def parse(type,instance,msgSp):
	 if type==1:#send cash object
		 instance.setType("SND")#set the type
		 amount=currencyFormat(msgSp[2])
		 instance.setAmt(amount)#set amount sent
		 receiver=msgSp[5]+" "+msgSp[6]
		 instance.setName(receiver)
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("on")!=-1):
				 dateIdx=(i+1)
		 dateList=msgSp[dateIdx]
		 dateList=dateList.split("/")
		 instance.setDay(int(dateList[0]))
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("balance")!=-1):
				 balIdx=(i+2)
		 bal=currencyFormat(msgSp[balIdx])
		 instance.setNewBal(bal)#set new Balance
		 
	 elif type==2:#receive cash object
		 instance.setType("REC")
		 received=currencyFormat(msgSp[5])
		 instance.setAmt(received)#set received cash amount
		 sender=msgSp[7]+" "+msgSp[8]
		 instance.setSender(sender)#set sender details
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("balance")!=-1):
				 balIdx=(i+2)
		 bal=currencyFormat(msgSp[balIdx])
		 instance.setNewBal(bal)#set new Balance
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("on")!=-1):
				 dateIdx=(i+1)
		 dateList=msgSp[dateIdx]
		 dateList=dateList.split("/")
		 instance.setDay(int(dateList[0]))
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 
	 elif type==3:#deposit cash transaction
		 instance.setType("DEP")#set type
		 dateList=msgSp[3]
		 dateList=dateList.split("/")
		 instance.setDay(int(dateList[0]))#set dates
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("balance")!=-1):
				 balIdx=(i+2)
		 bal=currencyFormat(msgSp[balIdx])
		 instance.setNewBal(bal)#set new Balance
		 amt=currencyFormat(msgSp[8])
		 instance.setAmt(amt)#set deposit amount
		 
	 elif type==4:#withdraw cash transaction
		 instance.setType("WIT")#set type
		 dateList=msgSp[3].split("/")
		 instance.setDay(int(dateList[0]))#set dates
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 withAmt=currencyFormat(msgSp[8])
		 instance.setAmt(withAmt)#set amount withdrawn
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("balance")!=-1):
				 balIdx=(i+2)
		 bal=currencyFormat(msgSp[balIdx])
		 instance.setNewBal(bal)#set new Balance
		 
	 elif type==5:#purchase Airtime transaction
		 instance.setType("AIR")#set type
		 airAmt=currencyFormat(msgSp[4])
		 instance.setAmt(airAmt)#set airtime amount
		 if 'for' in msgSp:#purchasing airtime for another user
			 dateList=msgSp[10].split("/")
		 else:#purchasing airtime for oneself
			 dateList=msgSp[8].split("/")
		 instance.setDay(int(dateList[0]))#set dates
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 for i in xrange(len(msgSp)):
			 if(msgSp[i].find("balance")!=-1):
				 balIdx=(i+2)
		 bal=currencyFormat(msgSp[balIdx])
		 instance.setNewBal(bal)#set new Balance
		 
	 elif type==6:#balance inquiry sms
		 instance.setType("INQ")#set type
		 balance=currencyFormat(msgSp[6])
		 instance.setNewBal(balance)#set balance amount
		 dateList=msgSp[8].split("/")#extract the date
		 instance.setDay(int(dateList[0]))#set dates
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 instance.setCost(10)#service charge due to inquiry
		 
	 elif type==7:#bill payment sms
		 instance.setType("BIL")#set type
		 balance=currencyFormat(msgSp[len(msgSp)-1])
		 instance.setNewBal(balance)#set balance amount
		 for i in xrange(len(msgSp)):
			 if msgSp[i]=="on":
				 dateIdx=(i+1)
		 dateList=msgSp[dateIdx].split("/")#extract the date
		 instance.setDay(int(dateList[0]))#set dates
		 instance.setMonth(int(dateList[1]))
		 instance.setYear(int(dateList[2]))
		 ent=msgSp.index('to')+1
		 instance.setEntity(msgSp[ent])#set entity which received payment for the bill
		 amt=currencyFormat(msgSp[2])
		 instance.setAmt(amt)
	 
def opening(index, data, months):#method to find a months opening balance.
	 if index!= 0 and len(data[months[index]-1])!=0:
		 return data[months[index]-1][len(data[months[index]-1])-1].getNewBal()
	 else:
		 first=data[months[index]][0]#first sms for that month
		 if first.getType()=="DEP" or first.getType()=="REC":#first sms is deposit or receive
			opening=first.getNewBal()-first.getAmt()
			return opening
		 elif first.getType()=="AIR":#sms is buying of airtime
			opening=first.getNewBal()+first.getAmt()
			return opening
		 elif first.getType()=="WIT" or first.getType()=="SND":
			 opening=first.getNewBal()+service(first.getAmt())+first.getAmt()
			 return opening
		 elif first.getType()=="INQ":
			 opening=first.getNewBal()+first.getCost()
			 return opening
			 
def service(amount):#a lookup table for service charges
	 if amount >= 50 and amount <=100:
		 return 15
	 elif amount >= 101 and amount <=2500:
		 return 25
	 elif amount >= 2501 and amount <=5000:
		 return 45
	 elif amount >= 5001 and amount <=10000:
		 return 75
	 elif amount >= 10001 and amount <=20000:
		 return 145
	 elif amount >= 20001 and amount <=35000:
		 return 170
	 elif amount >= 35001 and amount <=50000:
		 return 250
	 elif amount >= 50001 and amount <=70000:
		 return 300
		 
def currencyFormat(amt):#extracts the currency amount irrespective of the format it is written in and returns an interger
	amt=amt.replace("Ksh","").replace(",","").strip()
	if '.' in amt:
		if amt[-1]=='.':
			amt=amt.replace('.',"")
			return int(amt)
		else:
			amt = amt[:amt.index('.')]
			return int(amt)
	else:
		return int(amt)


