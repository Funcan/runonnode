import re
import string
import sys


def expand(range):
    """
    Give a node specification possibly containing a range (such as
    compute[1-3], return a list of nodes
    """
    nodes = []

    tidyrange = string.replace(range, " ", "").strip()

    match = re.match("(^[^\[,]+)(.*)", tidyrange)
    node = match.group(1)
    rest = match.group(2)
    if len(rest) == 0:
        nodes.append(node)
        return nodes

    if rest[0] == ',':
        nodes.append(node)
        nodes = nodes + expand(rest[1:])
        return nodes

    if rest[0] == '[':
        match = re.match("^\[(.*?)\](.*)", rest)
        noderange = match.group(1)
        rest = match.group(2)
        for n in _expand_range(noderange):
            nodes.append(node + str(n))
        if rest != '':
            if rest[0] != ',':
                print "Invalid range '%s'" % (range)
                return []
            else:
                nodes = nodes + expand(rest[1:])
        return nodes

    print "Should not get here!"
    return []

def _expand_range(range):
    results = []
    match = re.match("(^[0-9]+)(.*)", range)
    start = match.group(1)
    rest = match.group(2)
    match = re.match("^-([0-9]+)(.*)", rest)
    if match:
        end = match.group(1)
        rest = match.group(2)
    else:
        end = start

    if (start[0] == '0'):
        length = len(start)
    else:
    	length = 0

    for i in xrange(int(start), int(end)+1):
        results.append("%0*d" % (length, i))

    if rest != '':
        if rest[0] != ',':
            print "Invalid range expansion '%s'" % (range)
        results = results + _expand_range(rest[1:])

    return results


def runtests():
    tests = {"abc123": ["abc123"],
            "abc[123]": ["abc123"],
            "abc[1,2,3]": ["abc1", "abc2", "abc3"],
            "abc[1-3]": ["abc1", "abc2", "abc3"],
            "abc[1-3,5-6]": ["abc1", "abc2", "abc3", "abc5", "abc6"],
            "abc[1-3,5-6,8]": ["abc1", "abc2", "abc3", "abc5", "abc6", "abc8"],
            "abc[1-3,5-6,7]": ["abc1", "abc2", "abc3", "abc5", "abc6", "abc7"],
            "abc1,abc2": ["abc1", "abc2"],
            "abc[1-2],abc[4-5]": ["abc1", "abc2", "abc4", "abc5"],
            "abc1,abc[3-4],abc[6-7]": ["abc1", "abc3", "abc4", "abc6", "abc7"],
            "abc[01-03]": ["abc01", "abc02", "abc03"],
            "abc[0,1,3,2]": ["abc0", "abc1", "abc3", "abc2"],
            "abc[1, 2, 3]": ["abc1", "abc2", "abc3"],
            }

    for test in tests:
        result = expand(test)
        result.sort()
        expected = tests[test]
        expected.sort()
        if result == expected:
            print "PASSED:", test
        else:
            print "FAILED:", test, "got:", result

if __name__ == "__main__":
	if len(sys.argv) == 1:
		print "Usage: \t%s --tests" % (sys.argv[0])
		print "       \t%s <node spec>" % (sys.argv[0])
		sys.exit(1)
	if sys.argv[1] == "--tests":
		runtests()
	else:
		for n in expand(" ".join(sys.argv[1:])):
			print n
