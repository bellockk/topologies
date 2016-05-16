#!/usr/bin/env python2.2

import sys,copy,marshal,time 	#Imports standard modules needed for execution of this code
stime = time.time()
#Define the topology class.  This makes the code contained within this module object
#oriented and allows its import into other functions to control data flow through
#multiple processors or networks.

class topology:

#This is the initialization ofunction and when the topology class is instantiated this
#function will automatically be called.

	def __init__(self,nspace,logfile=None):
	
	#Generate the list of possible topologies
		
		self.logfile  = logfile
		if self.logfile != None:
			self.logoutput = open(logfile,'w')
		
		masterlist = []
		for i in xrange(int(nspace)):
			masterlist.append(i)
		
		allsubsets = self.allsubsets(masterlist)
		
		if 0:
			for subset in allsubsets:
				self.PrintToLog(subset)
			self.PrintToLog('\n')
	
	#Test all possibilites and construct the list of actual topologies
		
		a = self.topologies(masterlist,allsubsets)
		
	#Write the output file
		
		if 1:
			for item in a:
				self.PrintToLog(str(item)+'\n')
		if 1:
			self.PrintToLog('\nTotal Topologies: %s' % str(len(a)))
		if self.logfile:
			self.logoutput.close()
		
#This algorithm tests each possible topology on the given basis and
#returns a list of all actual topologies.
	
	def topologies(self,masterlist,allsubsets):
	
		topologies = [allsubsets]
		
	#Apply the tests for a topology.  If it passes all tests add it to topologies.
		length = 2**(len(allsubsets)-2)-1
		ilength = length
		curpct = -1
		while length>0:
			if 1:
				pct = 100 - int(float(length)/float(ilength)*100.0)
				if not pct%10 and pct !=curpct:
					curpct = pct
					print str(pct)+'%'
			length = length-1
			bindex = copy.deepcopy(length)
			item = [[]]
			subindex = 0
			teststr = ''
			while bindex >= 1:
				subindex = subindex + 1
				if bindex%2:
					item.append(allsubsets[subindex])
				bindex = bindex/2
			item.append(masterlist)
			
		#Test for possesion of the empty set and the basis
			test = 1
		
		#Test that the intersection of any two members of the possible topology is in the possible topology.
			if test:
				itemsubsets = item
				for i in xrange(len(itemsubsets)-1):
					if not test:
						break
					for j in xrange(i+1,len(itemsubsets)-1):
						intersection = self.intersection(itemsubsets[i],itemsubsets[j])
						intersection.sort()
						if intersection not in item:
							test = 0
							break
		
		#Test that the union of any family of subsets is contained in the possible topology.
			if test:
				nlength = 2**(len(item)-1)
				while nlength>0:
					nlength = nlength - 1
					nbindex = copy.deepcopy(nlength)
					family = []
					nsubindex = -1
					while nbindex >=1:
						nsubindex = nsubindex + 1
						if nbindex%2:
							family.append(item[nsubindex])
						nbindex = nbindex/2
					familyunion = self.union(family)
					familyunion.sort()
					if familyunion not in item:
						test = 0
						break
	
	#If it passes all tests add the topology to the final list.
			
			if test:
				topologies.append(item)
				
	#Return the resulting list of topologies
	
		return topologies
		
#This funcion returns a list of all possible subsets that can be constructed from the master list.

	def allsubsets(self,masterlist):
		
		subsets = [[]]
		for item in masterlist:
			for i in xrange(len(subsets)):
				alist = copy.deepcopy(subsets[i])
				alist.append(item)
				subsets.append(alist)
		return subsets

#This functino returns the union of the list of sets it recieves as an arguement.

	def union(self,setofsets):
		union = []
		combinedset = []
		for item in setofsets:
			for subitem in item:
				combinedset.append(subitem)
		for item in combinedset:
			if item not in union:
				union.append(item)
		return union
		
#This function returns the intersection of the two arguements that are sent to it.
#The function is restricted to the intersection of only two sets to improve performance.

	def intersection(self,setA,setB):
		
		intersection = []
		for item in setA:
			if item in setB:
				intersection.append(item)
		return intersection

#This function returns the compliment of a set relative to the masterlist.

	def compliment(self,subset,X):
		
		compliment = []
		for item in X:
			if item not in subset:
				compliment.append(item)
		return compliment
		
#This is a function which is not used by this class but that I am very proud of.
#It returns a list of all permutations of a given set without repeats.  It also
#does this by a method faster that binary logic substitution.

	def permutations(self,masterlist):
		
		permutations = []
		for item in masterlist:
			permutations.append([item])
		for item in xrange(len(masterlist)-1):
			newpermutations = []
			for item in permutations:
				for subitem in self.compliment(item,masterlist):
					newpermutations.append([subitem]+item)
				permutations = newpermutations
		return permutations
		
	def PrintToLog(self,string):
		if self.logfile == None:
			print string
		else:
			self.logoutput.write('%s\n'%string)
#This is the test algorithm.  If this module is executed on its own and not imported.
#This code will run after the topology class is defined.

if __name__ == '__main__':

	if len(sys.argv) == 1:
		print 'You must enter the value for nspace to evaluate.'
		sys.exit()
	nspace = sys.argv[1]
	if len(sys.argv) == 2:
		a = topology(sys.argv[1])   
	else:
		a = topology(sys.argv[1],sys.argv[2])
	ftime = time.time()
	ttime = round(ftime-stime,2)
	print 'Time to complete: %s'%str(ttime)
