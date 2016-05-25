import itertools
import operator
import logging
import urllib2
import json

LOG = logging.getLogger(__name__)


def istopology(topology):
    for pair in itertools.combinations(topology, 2):
        if pair[0] & pair[1] not in topology:
            return False
    for family in (list(l) for l in itertools.chain.from_iterable(
            itertools.combinations(
                topology, t) for t in xrange(len(topology)+1))):
        if family != [] and reduce(operator.ior, family) not in topology:
            return False
    return True


def topologies(N, cores):
    LOG.info('Generating the finite topologies for N = %s\n', N)
    num_subsets = 2**N
    num_subsets_minus1 = num_subsets - 1
    num_subsets_plus1 = num_subsets + 1
    num_topologies = 1
    for item in (list(s) for s in itertools.chain.from_iterable(
            itertools.combinations(xrange(1, num_subsets_minus1),
                                   r) for r in xrange(1, num_subsets_plus1))):
        item.insert(0, 0)
        item.append(num_subsets_minus1)
        if istopology(item):
            num_topologies += 1
            LOG.info('%s', item)
    LOG.info('\nNumber of topolgies: %s', num_topologies)
    return num_topologies


def verify(N, num_topologies):
    f = urllib2.urlopen("https://oeis.org/search?fmt=json&q=id:A000798")
    doc = json.loads(f.read())
    expected = [int(n) for n in doc['results'][0]['data'].split(',')]
    if expected[N] == num_topologies:
        status = 'PASS'
    else:
        status = 'FAIL'
    LOG.info('Verifying against OEIS: %s', status)
    if status == 'PASS':
        return True
    return False
