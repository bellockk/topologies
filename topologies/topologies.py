#!/usr/bin/env python2.2

import sys
import copy
import time
import logging
import multiprocessing
import argparse

LOG = logging.getLogger(__name__)

stime = time.time()


class topology:
    """
    Define the topology class.  This makes the code contained within this
    module object oriented and allows its import into other functions to
    control data flow through multiple processors or networks.
    """
    def __init__(self, nspace, num_cores):
        """
        This is the initialization ofunction and when the topology class is
        instantiated this function will automatically be called.
        """
        # Generate the list of possible topologies
        masterlist = []
        for i in xrange(int(nspace)):
            masterlist.append(i)

        # Number of cores to use
        self.cores = num_cores

        subsets = allsubsets(masterlist)

        # Test all possibilites and construct the list of actual topologies

        self.num_topologies = 0
        self.find_topologies(masterlist, subsets)

        # Write the output file
        LOG.info('\nTotal Number of Topologies: %s' % self.num_topologies)

    def append_topology(self, topology):
        if topology:
            LOG.info(topology)
            self.num_topologies += 1


    def find_topologies(self, masterlist, subsets):
        """
        This algorithm tests each possible topology on the given basis and
        returns a list of all actual topologies.
        """
        self.append_topology(subsets)
        # Create a Pool
        if self.cores:
            pool = multiprocessing.Pool(multiprocessing.cpu_count())

        # Construct possible topolgies
        length = 2**(len(subsets)-2)-1
        while length > 0:
            # Generate potential topology to be tested
            length = length-1
            bindex = copy.deepcopy(length)
            item = [[]]
            subindex = 0
            while bindex >= 1:
                subindex = subindex + 1
                if bindex % 2:
                    item.append(subsets[subindex])
                bindex = bindex/2
            item.append(masterlist)

            # Test if item is a topology
            if self.cores:
                pool.apply_async(test_topology, (item,),
                                 callback=self.append_topology)
            else:
                self.append_topology(test_topology(item))
        if self.cores:
            pool.close()
            pool.join()


def test_topology(item):
    # Test for possesion of the empty set and the basis
    test = 1

    # Test that the intersection of any two members of the possible
    # topology is in the possible topology.
    if test:
        itemsubsets = item
        for i in xrange(len(itemsubsets)-1):
            if not test:
                break
            for j in xrange(i+1, len(itemsubsets) - 1):
                intersect = intersection(itemsubsets[i],
                                         itemsubsets[j])
                intersect.sort()
                if intersect not in item:
                    test = 0
                    break

    # Test that the union of any family of subsets is contained in the
    # possible topology.
    if test:
        nlength = 2**(len(item)-1)
        while nlength > 0:
            nlength = nlength - 1
            nbindex = copy.deepcopy(nlength)
            family = []
            nsubindex = -1
            while nbindex >= 1:
                nsubindex = nsubindex + 1
                if nbindex % 2:
                    family.append(item[nsubindex])
                nbindex = nbindex/2
            familyunion = union(family)
            familyunion.sort()
            if familyunion not in item:
                test = 0
                break

    # If it passes all tests add the topology to the final list.
    if test:
        return item
    return None


def allsubsets(masterlist):
    """
    This funcion returns a list of all possible subsets that can be
    constructed from the master list.
    """
    subsets = [[]]
    for item in masterlist:
        for i in xrange(len(subsets)):
            alist = copy.deepcopy(subsets[i])
            alist.append(item)
            subsets.append(alist)
    return subsets


def union(setofsets):
    """
    This function returns the union of the list of sets it recieves as an
    arguement.
    """
    return list(set().union(*setofsets))

def intersection(A, B):
    """
    This function returns the intersection of the two arguements that are
    sent to it.  The function is restricted to the intersection of only two
    sets to improve performance.
    """
    return list(set(A).intersection(B))


def compliment(subset, X):
    """
    This function returns the compliment of a set relative to the
    masterlist.
    """
    return [i for i in X if i not in subset]


def permutations(masterlist):
    """
    This is a function which is not used by this class but that I am very
    proud of.  It returns a list of all permutations of a given set without
    repeats.  It also does this by a method faster that binary logic
    substitution.
    """
    permutations = []
    for item in masterlist:
        permutations.append([item])
    for item in xrange(len(masterlist)-1):
        newpermutations = []
        for item in permutations:
            for subitem in compliment(item, masterlist):
                newpermutations.append([subitem]+item)
            permutations = newpermutations
    return permutations

# This is the test algorithm.  If this module is executed on its own and not
# imported.  This code will run after the topology class is defined.
if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description='Number of topologies on a set with n points.',
        prog='topologies')
    PARSER.add_argument('-j', metavar='N', type=int, dest='cores',
                        default=None, help='number of processing cores to use')
    PARSER.add_argument('points', metavar='N', type=int,
                        help='number of points in metric')
    PARSER.add_argument('-V', '--version', action='version',
                        version='%s(prog)s 1.0')
    ARGS = PARSER.parse_args()
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(message)s')
    topology(ARGS.points, ARGS.cores)
    ftime = time.time()
    ttime = round(ftime-stime, 2)
    LOG.info('Time to complete: %s', str(ttime))
