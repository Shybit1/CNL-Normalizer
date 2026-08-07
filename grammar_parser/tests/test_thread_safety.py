import concurrent.futures
from grammar_parser import parse


def test_thread_safety_concurrent_parses():
    commands = [
        'CLIMB TO 500 METERS',
        'GO TO BRAVO',
        'FORMATION WEDGE',
        'LOITER FOR 10 SECONDS',
        'RTL',
    ] * 200

    def worker(cmd):
        r = parse(cmd)
        return r.success

    with concurrent.futures.ThreadPoolExecutor(max_workers=32) as ex:
        results = list(ex.map(worker, commands))

    assert all(results)
