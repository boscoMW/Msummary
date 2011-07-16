#version 1.3
#This script searches through the inbox to find any
#sms from mpesa and create a summary of monthly transactions

import inbox,appuifw,smsTypes,os,os.path,e32,progress
		 
appuifw.app.title=u"M-Summary"

pb = progress.TWProgressBar()#create progressbar and initialize it
pb.set_text(u"Please wait...")#set progressbar text

box = inbox.Inbox()
smsData=[[] for i in range(12)]#data structure for holding sms data
months = []
months2 = []
titles = (u"January",u"February",u"March",u"April",u"May",u"June",u"July",u"August",u"September",u"October",u"November",u"December")

app_lock = e32.Ao_lock()

def quit():
	appuifw.app.set_exit()

def back():
	app_lock.signal()

#assign key to options soft button
appuifw.app.menu = [(u"Back", back)]	
		 
appuifw.app.exit_key_handler=quit
app_lock = e32.Ao_lock()
	 
def addMonth(m):
	 m=m-1
	 if (m in months)==False:
		 months.append(m)

for sms_id in box.sms_messages():#loop through all the messages in the inbox
	 sender= box.address(sms_id) 
	 if(sender.find("MPESA"))!=-1:#if the message was sent by mpesa
		 msg = box.content(sms_id)
		 msgSp=msg.split()#split message into sections
		 if 'sent' in msgSp and ('for' in msgSp)!=True:#send cash transaction
			 smsInstance=smsTypes.sndCash()
			 smsTypes.parse(1,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'received' in msgSp:#Receive cash transaction
			 smsInstance=smsTypes.receive()
			 smsTypes.parse(2,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'Give' in msgSp:#Deposit cash transaction
			 smsInstance=smsTypes.deposit()
			 smsTypes.parse(3,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'Withdraw' in msgSp:#withdraw cash transaction
			 smsInstance=smsTypes.withdraw()
			 smsTypes.parse(4,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'bought' in msgSp and 'airtime' in msgSp:#purchase airtime transaction
			 smsInstance=smsTypes.buyAirtm()
			 smsTypes.parse(5,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'balance' in msgSp and 'was' in msgSp:#balance inquiry transaction
			 smsInstance=smsTypes.inquiry()
			 smsTypes.parse(6,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
		 elif 'sent' in msgSp and 'for' in msgSp:#bill payment transaction
			 smsInstance=smsTypes.bill()
			 smsTypes.parse(7,smsInstance,msgSp)
			 smsData[(smsInstance.getMonth()-1)].append(smsInstance)
			 addMonth(smsInstance.getMonth())
	 
	 numer= float(box.sms_messages().index(sms_id)+1)#update position of progress bar
	 denom=float(len(box.sms_messages()))
	 progress=int((numer/denom)*100)
	 pb.set_value(progress)
	 
for x in smsData:
	 x.reverse()#reverse to chronological order
months.sort()		 
for x in months:
     months2.append(titles[x])
	 
pb.close()#close progressbar
del pb
	 
#display menu for choice selection	 
choices=[u"Export Summary",u"View Summary",u"Quit"]
choice=0
while choice!=2 or choice !=None:
	 appuifw.app.screen="normal"
	 choice=appuifw.selection_list(choices,1)
	 
	 if choice==0:#user selects export 
		 index=appuifw.selection_list(months2,1)
		 if index!=None:
			PATH=u"E:\\Exports\\payload"
			if not os.path.exists(PATH):#create directory path if it does not exist
				os.makedirs(PATH)
			f= file(u"E:\\Exports\\payload\\"+months2[index]+"Data.txt","w+")#create file object with write permission set
			smsData[months[index]].reverse()
			closingBal=smsData[months[index]][len(smsData[months[index]])-1].getNewBal()
			opening=str(smsTypes.opening(index,smsData,months))
		
			print >>f,"Opening Balance:"+opening+" Kshs"
			for x in smsData[months[index]]:
				if x.getType()=="SND":
					print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  Out:    "+str(x.getAmt())+" Balance:    "+str(x.getNewBal())
				elif x.getType()=="WIT":
				        print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  Out:    "+str(x.getAmt())+" Balance:    "+str(x.getNewBal())
				elif x.getType()=="AIR":
					print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  Out:    "+str(x.getAmt())+" Balance:    "+str(x.getNewBal())
				elif x.getType()=="REC":
					print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  In:    "+str(x.getAmt())+"  Balance:    "+str(x.getNewBal())
				elif x.getType()=="DEP":
					print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  In:    "+str(x.getAmt())+"  Balance:    "+str(x.getNewBal())
				elif x.getType()=="INQ":
					print >> f,"  Date:  "+str(x.getDay())+"/"+str(x.getYear())+"  Type:    "+x.getType()+"  Out:    "+str(x.getCost())+" Balance:    "+str(x.getNewBal())
			print >> f,"Closing Balance: "+str(closingBal)+" Kshs"
			f.close()
			#print message confirming successful export
			appuifw.note(u"Export done","conf")
            		 
	 elif choice==1:#user selects view summary
		 index=appuifw.selection_list(months2,1)
		 if index >= 0:#get the selected month
			 appuifw.app.screen="large"
			 t=appuifw.Text()
			 appuifw.app.body=t
			 closingBal=smsData[months[index]][len(smsData[months[index]])-1].getNewBal()	
			 #write text in unicode to the current position of the cursor
			 t.font="title"
			 t.color=0xFFFFFFFF
			 t.style = (appuifw.HIGHLIGHT_ROUNDED)
			 t.add(u"    "+months2[index]+"    \n")
			 t.style=(appuifw.STYLE_UNDERLINE)
			 t.font="normal"
			 t.color=0x00000000
			 t.add(u"Opening Bal:"+str(smsTypes.opening(index,smsData,months))+"Kshs\n")
			 t.style=appuifw.HIGHLIGHT_ROUNDED

			 for x in smsData[months[index]]:
				 if x.getType()=="SND":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+"\nType:    "+x.getType()+"\nOut:    "+str(x.getAmt())+"\nBalance:    "+str(x.getNewBal())+"\n")
				 elif x.getType()=="WIT":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+" \nType:    "+x.getType()+" \nOut:    "+str(x.getAmt())+"\nBalance:    "+str(x.getNewBal())+"\n")
				 elif x.getType()=="AIR":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+" \nType:    "+x.getType()+" \nOut:    "+str(x.getAmt())+"\nBalance:    "+str(x.getNewBal())+"\n")
				 elif x.getType()=="REC":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+" \nType:    "+x.getType()+"\nIn:    "+str(x.getAmt())+"\nBalance:    "+str(x.getNewBal())+"\n")
				 elif x.getType()=="DEP":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+" \nType:    "+x.getType()+"\nIn:    "+str(x.getAmt())+"\nBalance:    "+str(x.getNewBal())+"\n")
				 elif x.getType()=="INQ":
					 t.add(u"\nDate:        "+str(x.getDay())+"/"+str(x.getYear())+" \nType:    "+x.getType()+" \nOut:    "+str(x.getCost())+"\nBalance:    "+str(x.getNewBal())+"\n")	
				 t.style=appuifw.STYLE_UNDERLINE
				 t.add(u" "*33)
				 t.style=appuifw.HIGHLIGHT_ROUNDED
			 t.add(u"Closing Balance: "+str(closingBal)+" Kshs")
			 t.set_pos(0)
			 app_lock.wait()
	 
	 elif choice == None or choice == 2:#User presses cancel key
		 exitsplash = appuifw.Text()
		 appuifw.app.body = exitsplash
		 appuifw.app.screen="large"
		 for x in range(6):
			 exitsplash.add(u"\n")
		 exitsplash.add(u"Thank you for using m-summary\n")
		 exitsplash.add(u"Press Exit to quit")
		 app_lock.wait()
		 
		 
#user chooses to quit
		 
