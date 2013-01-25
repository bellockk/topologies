#!/usr/bin/env python

import sys,copy


class topology:
        """
        Define the topology class.  This makes the code contained within this module object
        oriented and allows its import into other functions to control data flow through
        multiple processors or networks.
        """
        def __init__(self,masterlist):
            """
            This is the initialization function and when the topology class is instantiated this
            function will automatically be called.
            """
            #Generate the list of possible topologies.

                allsubsets = self.allsubsets(masterlist)
                a = self.topologies(masterlist,allsubsets)
                outfile = open('topology_out.txt','w')
                for item in a:
                    outfile.write(str(item)+'\n')
                outfile.write('\nTotal Topologies: '+str(len(a)))
                outfile.close()


        def topologies(self,masterlist,allsubsets):
            """
            This algorith assembles a list of possible topologies on a given basis and tests
            each one to see if it satisfies the conditions for a topology.  It returns the
            topologies that are found.
            """
            topologies = [allsubsets]

            #Apply the tests for a topology.  If it passes all tests add it to topologies.
                length = 2**(len(allsubsets)-2)-1
                #for bindex in xrange(1,length+1):
                while length>0:
                    if not length%10000:
                        print length
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
                        #print length-allptopologies.index(item)

                #Test that the intersection of any two members of the possible topolgy is in the possible topology.

                        test = 1
                        #itemsubsets = self.allsubsets(item)
                        #del itemsubsets[0]
                        itemsubsets = item
                        for i in xrange(len(itemsubsets)-1):
                            if not test:
                                break
                            for j in xrange(i+1,len(itemsubsets)-1):
                                intersection = self.intersection(itemsubsets[i],itemsubsets[j])
                                        intersection.sort()
                                        if intersection not in item:
                                            test=0
                                                break

        #If it passes all tests add the topology to the final list.
                        if test:
                            topologies.append(item)

        #Return the resulting list of topologies

                return topologies


        def allsubsets(self,masterlist):
            """
            This function returns a list of all possible subsets that can be constructed from the masterlist.
            """
            subsets = [[]]
                for item in masterlist:
                    for i in xrange(len(subsets)):
                        alist = copy.deepcopy(subsets[i])
                                alist.append(item)
                                subsets.append(alist)
                return subsets



        def union(self,setofsets):
            """
            This function returns the union of the list of sets it recieves as an arguement.
            """
            union = []
                combinedset = []
                for item in setofsets:
                    for subitem in item:
                        combinedset.append(subitem)
                for item in combinedset:
                    if item not in union:
                        union.append(item)
                return union


        def intersection(self,setA,setB):
            """
            This function returns the intersection of the two arguements that are sent to it.
            The function is restricted to the intersection of only two sets to improve performance.
            """
            intersection = []
                for item in setA:
                    if item in setB:
                        intersection.append(item)
                return intersection



        def compliment(self,subset,X):
            """
            This function returns the compliment of a set relative to the masterlist.
            """
            compliment = []
                for item in X:
                    if item not in subset:
                        compliment.append(item)
                return compliment



        def permutations(self,masterlist):
            """
            This is a function which is not used by this class but that I am very proud of.
            It returns a list of all permutations of a given set without repeats.  It also
            does this by a method faster than binary logic substitution.
            """
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


#This is the test algorithm.  If this module is executed on its own and not imported.
#This code will run after the topology class is defined.

if __name__ == '__main__':

    a = topology(['a','b','c'])
