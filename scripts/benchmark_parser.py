import time
from grammar_parser import parse


def run_benchmark(iterations: int = 10000):
    samples = [
        'CLIMB TO 500 METERS',
        'DESCEND TO 100 METERS',
        'GO TO BRAVO',
        'GO TO WAYPOINT ALPHA',
        'FORMATION WEDGE',
        'LOITER',
        'LOITER FOR 20 SECONDS',
        'RTL',
        'RETURN HOME',
        'ABORT',
    ]

    durations = []
    for i in range(iterations):
        s = samples[i % len(samples)]
        t0 = time.perf_counter()
        r = parse(s)
        t1 = time.perf_counter()
        durations.append((t1 - t0) * 1000.0)  # ms
        if not r.success:
            raise RuntimeError(f"Benchmark parse failed for: {s}; errors={r.errors}")

    avg = sum(durations) / len(durations)
    worst = max(durations)
    print(f"benchmark_iterations={iterations} avg_ms={avg:.6f} worst_ms={worst:.6f}")
    return avg, worst


if __name__ == '__main__':
    run_benchmark(2000)
