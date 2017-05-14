import operator
import random
import logging,sys

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
		return self.firstname + " " + self.lastname + "  " + wstr + " PowerBall: " + str(self.red)
	
	# hack I dont entirely approve of this since it deliberately ignores name fields
	def __eq__(self,other):
		return (self.red == other.red) and (self.whites == other.whites)
		
	def __ne__(self,other):
		return not self.__eq__(other)


def pickNumberSet(minValue,maxValue,pickCount):

	numLabel = ['1st','2nd','3rd','4th','5th']
	if pickCount == 1:
		numLabel = ['Power Ball']
	
	yns = ""
	pickRangeErrorString = " is not a number between " + str(minValue) + " and " + str(maxValue) + ", try again"
	pickSet = set()
	while len(pickSet) < pickCount:
		numberAskString = "select " + numLabel[len(pickSet)] + " # (" + str(minValue) + " thru " + str(maxValue)
		
		exclStr = ""
		if len(pickSet) > 0:
			exclStr = " excluding "
			
		numberAskString = numberAskString + exclStr + yns + "): "
		
		userNumberString = raw_input(numberAskString)		
		
		# validate numberAskString, parses as integer, is in range, and not already picked
		try:
			userInt = int(userNumberString)
		except ValueError:
			print userNumberString + pickRangeErrorString
			continue	
		if( userInt > maxValue or userInt < minValue ):
			print userNumberString + pickRangeErrorString
			continue		
		if( userInt in pickSet ):
			print userNumberString + " has already been chosen, please pick a different number"
			continue
			
		pickSet.add( userInt )
		
		# the exclusion list - string of all existing numbers in pickSet
		if len(pickSet) == 1:		
			yns = str(list(pickSet)[0])
		if len(pickSet) > 1:
			yns = ""
			for w in list(pickSet)[:-1] :
				yns = yns + str(w) + ", "		
			# chop off final ', ' then append ' and ' final number
			yns = yns[:-2]
			w = list(pickSet)[-1]
			yns = yns + " and " + str(w)
	return pickSet

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
	
	whites = pickNumberSet(1,69,5)
	reds = pickNumberSet(1,26,1)
		
	aticket = Ticket(userFirst,userLast,whites,next(iter(reds)))
	return aticket


def pickWinningNumbers(ballCountDict,pickCount):
	
	# build ordered set of occurrence counts (eg if white ball 5 is chosen by 459 tickets, 459 goes into countSet)
	contestSet = set()
	numNeeded = pickCount
	countset = set()	
	for k,v in ballCountDict.items():
		countset.add(v)
	
	# now filter the original balls by occurrences in descending order
	# keep going until enough numbers are picked to complete the contest set	
	reverseCountSet = sorted(countset,reverse=True)
	for r in reverseCountSet:
		if numNeeded > 0:
			dfiltered = {k:v for k,v in ballCountDict.items() if v == r}
			numAvailable = len(dfiltered)
			numNeeded = pickCount - len(contestSet)
			logger.debug(  "numNeeded: " + str(numNeeded) + ", numAvailable: " + str(numAvailable) + " at " + str(r) + " occurrences" )
			
			filteredvalues = "("
			for kf in dfiltered:
				filteredvalues = filteredvalues + str(kf) + ","
			filteredvalues = filteredvalues[:-1] + ")"
			logger.debug( filteredvalues )
			
			numAtThisCount = numAvailable - numNeeded
			
			# take all if doing so would not leave a surplus
			if numAvailable <= numNeeded:
				for kf in dfiltered:
					contestSet.add(kf)
					numNeeded -= 1
					logger.debug( str(kf) + " added" )			
			# numAvailable > numNeeded - randomly pick numNeeded from numAvailable
			else:
				picklist = list(dfiltered)			
				while numNeeded > 0:				
					ri = random.randint(0, len(picklist) - 1)
					pickvalue = picklist[ri]
					contestSet.add(pickvalue)
					numNeeded -= 1
					picklist.remove(pickvalue)
					logger.debug( "ri: " + str(ri) + " value: " + str(pickvalue) + " added" )				
		else:
			logger.debug( "done!" )
		
		# debug - show the contestSet at each occurrence level as built
		logger.debug( "contestSet:" )
		css = ""		
		for cs in sorted(contestSet):
			css += str(cs) + " "
		css = css[:-1] + " Powerball: "
		logger.debug( css )
			
	return contestSet

def runContest(ticketlist):
	
	if len(ticketlist) == 0:
		print "no tickets created, cannot generate a winning ticket"
		return
	
	# show all of the tickets
	for t in ticketlist:
		print t
	
	whitecount = {}
	redcount = {}	
	# iterate the tickets - increment counters to track the most prevalent numbers
	for t in ticketlist:
		for w in t.whites:
			if w in whitecount:
				whitecount[w] += 1
			else:
				whitecount[w] = 1
				
		r = t.red
		if r in redcount:
			redcount[r] += 1
		else:
			redcount[r] = 1
			
	# pick desired number of winning balls from each color set
	logger.debug("pick the winning numbers")
	whiteSet = pickWinningNumbers(whitecount,5)
	logger.debug("pick the winning Power Ball")
	redSet = pickWinningNumbers(redcount,1)	
		
	# show winning ticket
	print "Powerball winning number:"
	css = ""		
	for cs in sorted(whiteSet):
		css += str(cs) + " "
	css = css + "Powerball: " + str(next(iter(redSet)))
	print css
	
	
	# at this point there must be a complete contest set
	# if only a single contestant enters a single ticket, that ticket will become the winner (all occurrences 1)
	
	# bonus - check all tickets to see if any are winners
	winningTicket = Ticket( "winning", "ticket", whiteSet, next(iter(redSet)) )
	foundWinner = False
	for t in ticketlist:
		if t == winningTicket:
			print "ding ding, we have a winner: " + str(t)
			foundWinner = True
	if not foundWinner:
		print "sorry, no winning ticket this time"
		
	return
	
# MAIN

logger = logging.getLogger()
logger.setLevel(logging.CRITICAL)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.NOTSET)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
	

tickets = []

debugFlag = False

# main loop - allow user to keep creating new tickets, or generating the winning ticket
while True:
	userInput = raw_input("enter (C)ontest, (Q)uit, or enter to create a new ticket: ")
	
	#print "you said..." + userTorC
	
	if userInput.upper() == "Q":
		quit()
	elif userInput.upper() == "C":
		runContest(tickets)
	elif userInput.upper() == "D":
		debugFlag = not debugFlag
		if debugFlag:
			logging.getLogger().setLevel(logging.DEBUG)
		else:
			logging.getLogger().setLevel(logging.CRITICAL)
		print "logging debug " + str(debugFlag)
	else:
		aticket = createNewTicket()
		tickets.append(aticket)
	
