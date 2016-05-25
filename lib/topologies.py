import itertools
import operator
import time
import logging
import progressbar

LOG = logging.getLogger(__name__)


def istopology(topology):
    """
    Tests a possible topology.

    It is assumed that possible topolgies are constructed with the null set and
    the complete set, so those tests are not made here.

    Parameters
    ----------
    topology : list
        Set to run tests for topology on

    Returns
    -------
    result: bool
        True if the input list passes the tests for a topology, false
        otherwise.
    """
    # Intersection of any two members is in the topology
    for pair in itertools.combinations(topology, 2):
        if pair[0] & pair[1] not in topology:
            return False

    # Union of any family is in the topology
    for family in (list(l) for l in itertools.chain.from_iterable(
            itertools.combinations(
                topology, t) for t in xrange(len(topology)+1))):
        if family != [] and reduce(operator.ior, family) not in topology:
            return False
    return True


def topologies(N, cores):
    stime = time.time()
    num_subsets = 2**N
    num = 1
    pbar = progressbar.ProgressBar(
        widgets=[progressbar.Percentage(), progressbar.Bar()],
        maxval=2**(2**N)).start()
    pbar_counter = 0
    for item in (list(s) for s in itertools.chain.from_iterable(
            itertools.combinations(xrange(1, num_subsets - 1),
                                   r) for r in xrange(1, num_subsets+1))):
        item.insert(0, 0)
        item.append(num_subsets-1)

        if istopology(item):
            num += 1
        pbar_counter += 1
        pbar.update(pbar_counter)
    pbar.finish()
    ftime = time.time()
    ttime = round(ftime-stime, 2)
    LOG.info('Number of topolgies: %s', num)
    LOG.info('Time to complete: %s', str(ttime))
    if verify()[N] == num:
        status = 'PASS'
    else:
        status = 'FAIL'
    LOG.info('Verifying against OEIS: %s', status)


def verify():
    import urllib2
    import json
    f = urllib2.urlopen("https://oeis.org/search?fmt=json&q=id:A000798")
    doc = json.loads(f.read())
    return [int(n) for n in doc['results'][0]['data'].split(',')]
