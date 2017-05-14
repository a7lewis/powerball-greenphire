import operator
import random

class Ticket:
	firstname = ""
	lastname = ""
	whites = set()
	red = int
	
	def __init__(self,first,last,ws,r):
		self.firstname = first
		self.lastname = last
		self.whites = ws
		self.red = r
		
	def __str__(self):
		wstr = ""
		for w in self.whites:
			wstr = wstr + str(w) + ","
		wstr = wstr[:-1]
		return "[" + self.firstname + " " + self.lastname + "] numbers: " + wstr + " PowerBall: " + str(self.red)


def createNewTicket():

	#todo - any name validation?
	# maybe just check for duplicates
	# but requirements didnt say whether you could enter more than once
	# so leave it alone, each entry creates a new ticket.
	# identity validation by name alone is pretty weak anyway
	# if this had been an actual assignment, there would be a chance to clarify requirements
	userFirst = raw_input("Enter your first name: ")
	userLast = raw_input("Enter your last name: ")
	
	numLabel = ['1st','2nd','3rd','4th','5th']
	
	# whites - get 5 unique numbers between 1 and 69
	whites = set()
	
	yns = ""
	whiteMin = 1
	whiteMax = 69
	whitesRangeErrorString = " is not a number between " + str(whiteMin) + " and " + str(whiteMax) + ", try again"
	
	while len(whites) < 5:
		numberAskString = "select " + numLabel[len(whites)] + " # (" + str(whiteMin) + " thru " + str(whiteMax)
		
		exclStr = ""
		if len(whites) > 0:
			exclStr = " excluding "
			
		numberAskString = numberAskString + exclStr + yns + "): "
		
		userNumberString = raw_input(numberAskString)
		
		
		# todo - validate numberAskString, integer in range?
		try:
			userInt = int(userNumberString)
		except ValueError:
			print userNumberString + whitesRangeErrorString
			continue
		
		if( userInt > whiteMax or userInt < whiteMin ):
			print userNumberString + whitesRangeErrorString
			continue
		
		if( userInt in whites ):
			print userNumberString + " has already been chosen, please pick a different number"
			continue
			
		whites.add( userInt )
		
		# the exclusion list - string of all existing whites
		if len(whites) == 1:		
			yns = str(list(whites)[0])
		if len(whites) > 1:
			yns = ""
			for w in list(whites)[:-1] :
				yns = yns + str(w) + ", "		
			# chop off final ', ' then append ' and ' final white
			yns = yns[:-2]
			w = list(whites)[-1]
			yns = yns + " and " + str(w)
	
	# todo - the red ball (1-26)	
		
	#print "all done picking your numbers..." + yns
	
	haveRedBall = False
	redMin = 1
	redMax = 26
	redRangeErrorString = " is not a number between " + str(redMin) + " and " + str(redMax) + ", try again"
	
	while haveRedBall == False:
			
		numberAskString = "select Power Ball # (" + str(redMin) + " thru " + str(redMax) + "): "
		redBallString = raw_input(numberAskString)
		
		try:
			redInt = int(redBallString)
		except ValueError:
			print redBallString + redRangeErrorString
			continue
			
		if( redInt > redMax or redInt < redMin ):
			print redBallString + redRangeErrorString
			continue
			
		haveRedBall = True
		
	print "Powerball: " + str(redInt)
	aticket = Ticket(userFirst,userLast,whites,redInt)
	return aticket


def runContest(ticketlist):
	
	# debug - show that we have all of the tickets
	for t in ticketlist:
		print t
	
	whitecount = {}	
	# iterate the tickets - increment counters to track the most prevalent numbers
	for t in ticketlist:
		for w in t.whites:
			if w in whitecount:
				whitecount[w] = whitecount[w] + 1
			else:
				whitecount[w] = 1
			
	# whitecount now has counts of all white balls in all tickets
	
	# build ordered set of occurrence counts (eg if white ball 5 is chosen by 459 tickets, 459 goes into countSet)
	contestSet = set()
	contestCount = 5
	numNeeded = contestCount
	countset = set()	
	for k,v in whitecount.items():
		countset.add(v)
	
	# now filter the original whitecount by occurrences in descending order
	# keep going until enough numbers are picked to complete the contest set	
	reverseCountSet = sorted(countset,reverse=True)
	for r in reverseCountSet:
		if numNeeded > 0:
			#print "r: " + str(r)
			dfiltered = {k:v for k,v in whitecount.items() if v == r}
			numAvailable = len(dfiltered)
			numNeeded = contestCount - len(contestSet)
			print "numAvailable: " + str(numAvailable) + ", numNeeded: " + str(numNeeded) + " at " + str(r) + " occurrences"
			
			filteredvalues = "("
			for kf in dfiltered:
				filteredvalues = filteredvalues + str(kf) + ","
			filteredvalues = filteredvalues[:-1] + ")"
			print filteredvalues
			
			numAtThisCount = numAvailable - numNeeded
			
			# take all if doing so would not leave a surplus
			if numAvailable <= numNeeded:
				for kf in dfiltered:
					contestSet.add(kf)
					numNeeded -= 1
					print str(kf) + " added"			
			# numAvailable > numNeeded - randomly pick numNeeded from numAvailable
			else:			
				while numNeeded > 0:				
					picklist = list(dfiltered)
					ri = random.randint(0, len(dfiltered) - 1)
					#print str(ri) + " list is: " + str(len(dfiltered)) + " long"
					pickvalue = picklist[ri]
					contestSet.add(pickvalue)
					numNeeded -= 1
					picklist.remove(pickvalue)
					print "ri: " + str(ri) + " value: " + str(pickvalue) + " added"				
		else:
			print "done!"
		
		# debug - show the contestSet at each occurrence level as built
		print "Powerball winning number:"
		css = ""		
		for cs in sorted(contestSet):
			css += str(cs) + " "
		css = css[:-1] + " Powerball: "
		print css
	
	# at this point there must be a complete contest set
	# if only a single contestant enters a single ticket, that ticket will become the winner (all occurrences 1)
	
	# bonus todo - check all tickets to see if any are winners
			
	return
	
	

print "powerball, baby!"

tickets = []


# main loop - allow user to keep creating new tickets, or generating the winning ticket
while True:
	userTorC = raw_input("enter (C)ontest, (Q)uit, or enter to create a new ticket: ")
	
	#print "you said..." + userTorC
	
	if userTorC.upper() == "Q":
		quit()
	elif userTorC.upper() == "C":
		runContest(tickets)
	else:
		aticket = createNewTicket()
		tickets.append(aticket)
	
