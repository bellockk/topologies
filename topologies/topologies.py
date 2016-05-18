#!/usr/bin/env python

import copy
import time
import logging
import multiprocessing
import argparse
import itertools

LOG = logging.getLogger(__name__)

stime = time.time()


class topology:
    """
    Define the topology class.  This makes the code contained within this
    module object oriented and allows its import into other functions to
    control data flow through multiple processors or networks.

    https://en.wikipedia.org/wiki/Finite_topological_space
    https://oeis.org/A000798
    """
    def __init__(self, nspace, num_cores):
        """
        This is the initialization function and when the topology class is
        instantiated this function will automatically be called.
        """
        # Generate the list of possible topologies
        masterlist = [i for i in range(nspace)]

        # Number of cores to use
        self.cores = num_cores

        subsets = powerset(masterlist)

        # Test all possibilites and construct the list of actual topologies

        self.num_topologies = 0
        self.find_topologies(masterlist, subsets)

        # Write the output file
        LOG.info('\nTotal Number of Topologies: %s' % self.num_topologies)

    def append_topology(self, topology):
        if topology:
            LOG.info(topology)
            self.num_topologies += 1
        self.workers.release()

    def find_topologies(self, masterlist, subsets):
        """
        This algorithm tests each possible topology on the given basis and
        returns a list of all actual topologies.
        """
        # Create a Pool
        if self.cores:
            processes = multiprocessing.cpu_count()
            queue_size = 1000
            pool = multiprocessing.Pool(processes)
            self.workers = multiprocessing.Semaphore(processes + queue_size)

        # Construct possible topolgies
        for item in powerset_generator(subsets[1:-1]):
            item.insert(0, [])
            item.append(masterlist)
            if item == [[], masterlist] or item == subsets:
                self.append_topology(item)
                continue

            # Test if item is a topology
            if self.cores:
                self.workers.acquire()
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
    for pair in itertools.combinations(item, 2):
        intersect = intersection(pair[0], pair[1])
        intersect.sort()
        if intersect not in item:
            test = 0
            break

    # Test that the union of any family of subsets is contained in the
    # possible topology.
    for family in powerset_generator(item):
        family_union = union(family)
        family_union.sort()
        if family_union not in item:
            test = 0
            break

    # If it passes all tests add the topology to the final list.
    if test:
        return item
    return None


class powerset_generator(object):

    def __init__(self, i, start_index=0):
        self.i = i
        self.start_index = start_index

    def __iter__(self):
        for subset in itertools.chain.from_iterable(
                itertools.combinations(self.i, r) for r in range(
                    self.start_index, len(self.i)+1)):
            yield list(subset)


def powerset(masterlist):
    """
    This funcion returns a list of all possible subsets that can be
    constructed from the master list.
    """
    return list(powerset_generator(masterlist))


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


def verify():
    import urllib2
    import json
    f = urllib2.urlopen("https://oeis.org/search?fmt=json&q=id:A000798")
    doc = json.loads(f.read())
    data = [int(n) for n in doc['results'][0]['data'].split(',')]


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
