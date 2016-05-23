import itertools
import operator
import time
import logging

LOG = logging.getLogger(__name__)


def topologies(N, cores):
    stime = time.time()
    num_subsets = 2**N
    num = 1
    logging.info([0, num_subsets])
    for item in [list(s) for s in itertools.chain.from_iterable(
            itertools.combinations(xrange(1, num_subsets - 1),
                                   r) for r in xrange(1, num_subsets+1))]:
        item.insert(0, 0)
        item.append(num_subsets-1)

        # Intersection of any two members
        test = True
        for pair in itertools.combinations(item, 2):
            if pair[0] & pair[1] not in item:
                test = False
                break
        if not test:
            continue

        # Union of any family
        for family in [list(s) for s in itertools.chain.from_iterable(
                itertools.combinations(item, r) for r in xrange(len(item)+1))]:
            if family != [] and reduce(operator.ior, family) not in item:
                test = False
                break
        if test:
            num += 1
        logging.info(item)
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
