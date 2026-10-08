"""Compare fixed-step and theorem-budget Curveball on synthetic null models."""
import argparse
import json
import math
import platform
import random
import time
from pathlib import Path

from .sampler import budget, prepare_graph, run_steps


def verify_degrees(n, original, result):
    """Independent output check; no sampler or adjacency helpers used."""
    def degrees(edges):
        counts = [0] * n
        seen = set()
        for edge in edges:
            if not isinstance(edge, (list, tuple)) or len(edge) != 2:
                raise ValueError('malformed edge')
            u, v = edge
            if type(u) is not int or type(v) is not int or not 0 <= u < v < n:
                raise ValueError('invalid normalized simple edge')
            if (u, v) in seen:
                raise ValueError('repeated edge')
            seen.add((u, v))
            counts[u] += 1
            counts[v] += 1
        return counts
    if degrees(original) != degrees(result):
        raise ValueError('labeled degrees changed')
    return True


def fixtures():
    result = []
    for n in (20, 30, 50):
        rng = random.Random(131000 + n)
        # Synthetic heterogeneous networks, not measured application data.
        edges = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if rng.random() < (0.35 if u < n // 5 or v < n // 5 else 0.08)]
        result.append({'name': f'heterogeneous-{n}', 'n': n, 'edges': edges})
    return result


def campaign(k=7, repetitions=3):
    records = []
    inputs = fixtures()
    for case in inputs:
        n, edges = case['n'], case['edges']
        m = len(edges)
        pairs = math.comb(n, 2)
        bits = (math.comb(pairs, m) - 1).bit_length()
        certified_steps = budget(n, m, k)
        # Same spectral-to-TV calculation applied to the paper's lazy switch
        # chain; a sufficient bound, not measured or necessary mixing time.
        switch_gap_inverse = 24 * n * n * math.comb(n, 4)
        switch_budget = (7 * switch_gap_inverse * (bits + 2*k - 2) + 19) // 20
        for repetition in range(repetitions):
            modes = ('fixed_10m', 'certified') if repetition % 2 == 0 else ('certified', 'fixed_10m')
            for mode in modes:
                steps = certified_steps if mode == 'certified' else 10 * m
                start = time.perf_counter()
                adj = prepare_graph(n, edges)
                changed = run_steps(adj, steps, random.SystemRandom())
                output = [[u, v] for u, neighbors in enumerate(adj)
                          for v in sorted(neighbors) if u < v]
                seconds = time.perf_counter() - start
                verify_degrees(n, edges, output)
                record = {'case': case['name'], 'mode': mode,
                          'repetition': repetition, 'steps': steps,
                          'seconds': seconds, 'changed_trades': changed,
                          'degree_check': True, 'edges': output,
                          'conditional_tv_bound': f'2^-{k}' if mode == 'certified' else None,
                          'universe_log2_ceiling': bits,
                          'switch_sufficient_budget_not_run': switch_budget}
                records.append(record)
                print(case['name'], mode, steps, round(seconds, 4), flush=True)
    return {'schema_version': 1, 'python': platform.python_version(),
            'platform': platform.platform(), 'randomness': 'SystemRandom',
            'source_commit': 'fd4aeeb2ee4fc729c18d98444fed42fd0529eeeb',
            'k': k, 'repetitions': repetitions, 'inputs': inputs,
            'timing_scope': 'adjacency construction, kernel and output edge-list construction; excludes witness validation and JSON serialization',
            'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--k', type=int, default=7)
    parser.add_argument('--repetitions', type=int, default=3)
    parser.add_argument('--output', type=Path, default=Path('experiments/curveball/results.json'))
    args = parser.parse_args()
    if args.k < 1 or args.repetitions < 1:
        parser.error('k and repetitions must be positive')
    data = campaign(args.k, args.repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
