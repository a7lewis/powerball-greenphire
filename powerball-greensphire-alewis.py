import operator
import random
import logging,sys
import math

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
		for w in sorted(self.whites):
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

	# never tell me the odds
	combos = 1
	
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
			logger.debug( "numNeeded: %d, numAvailable: %d at %d occurrences" % (numNeeded,numAvailable,r) )
			
			filteredvalues = "occurrences " + str(r) + ": ("
			for kf in dfiltered:
				filteredvalues = filteredvalues + str(kf) + ","
			filteredvalues = filteredvalues[:-1] + ")"
			logger.debug( filteredvalues )
			
			# take all if doing so would not leave a surplus
			if numAvailable <= numNeeded:
				for kf in dfiltered:
					contestSet.add(kf)
					numNeeded -= 1
					logger.debug( str(kf) + " added" )			
			# numAvailable > numNeeded - randomly pick numNeeded from numAvailable
			else:
				f = math.factorial
				fNumAvail = f(numAvailable)
				fNumAvailMinusNeeded = f(numAvailable - numNeeded)
				fNumNeeded = f(numNeeded)
				logger.debug( "C = f(n) / ( f(n-c) * f(c) )" )
				logger.debug( "n=%d c=%d C = f(%d) / ( f(%d) * f(%d))" % (numAvailable,numNeeded,numAvailable,numAvailable-numNeeded,numNeeded) )
				logger.debug( "n=%d c=%d C = %d / (%d * %d)" % (numAvailable,numNeeded,fNumAvail,fNumAvailMinusNeeded,fNumNeeded) )
				combos = combos * ( fNumAvail / ( fNumAvailMinusNeeded * fNumNeeded ) )
			
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
		css = "contestSet ("		
		for cs in sorted(contestSet):
			css += str(cs) + ","
		css = css[:-1] + ")"
		logger.debug( css )
			
	return contestSet, combos

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
	
	# double bonus - calculate the possible combinations of winning ticket available
	
	logger.debug("pick the winning numbers")
	whiteSet, whiteCombos = pickWinningNumbers(whitecount,5)
	logger.debug("pick the winning Power Ball")
	redSet, redCombos = pickWinningNumbers(redcount,1)
	
	logger.debug( "combos white: " + str(whiteCombos) + ", red: " + str(redCombos)	)
		
	# show winning ticket
	print "Powerball winning number:"
	css = ""		
	for cs in sorted(whiteSet):
		css += str(cs) + " "
	css = css + "Powerball: " + str(next(iter(redSet)))
	print css
	
	print "There are %d tickets, and %d possible winning tickets" % ( len(ticketlist), whiteCombos * redCombos )
	print "There is a 1 in %d chance of a winning ticket being picked" % ((whiteCombos * redCombos) / len(ticketlist))
	
	
	# at this point there must be a complete contest set
	# if only a single contestant enters a single ticket, that ticket will become the winner (all occurrences 1)
	
	# bonus - check all tickets to see if any are winners
	winningTicket = Ticket( "winning", "ticket", whiteSet, next(iter(redSet)) )
	foundWinner = False
	for t in ticketlist:
		if t == winningTicket:
			print "ding ding, we have a winner: %s" % (t)
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
	userInput = raw_input("enter (C)ontest, (Q)uit, (D)ebug toggle, or enter to create a new ticket: ")
	
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
	