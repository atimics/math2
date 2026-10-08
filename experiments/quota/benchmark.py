"""Isolated dense/network/hybrid quota benchmarks with exact blossom matching."""
import argparse
import json
import math
import platform
import resource
import subprocess
import sys
import time
from pathlib import Path

from .gadgets import reduce_graph


def verify_factor(n, edges, quotas, factor):
    allowed = {tuple(sorted(e)) for e in edges}
    seen = set()
    degrees = [0] * n
    for edge in factor:
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            raise ValueError('malformed factor edge')
        if any(type(v) is not int for v in edge):
            raise ValueError('factor endpoints must be integers')
        e = tuple(sorted(edge))
        if e not in allowed or e in seen:
            raise ValueError('factor edge absent or repeated')
        seen.add(e)
        for v in e:
            degrees[v] += 1
    if degrees != quotas:
        raise ValueError('decoded factor violates degree quotas')
    return True


def cases():
    result = []
    for d in (32, 128, 256):
        result.append({'name': f'star-{d}-half', 'n': d + 1,
                       'edges': [[0, v] for v in range(1, d + 1)],
                       'quotas': [d // 2] + [int(v <= d // 2) for v in range(1, d + 1)]})
    for n in (8, 12):
        result.append({'name': f'clique-{n}', 'n': n,
                       'edges': [[u, v] for u in range(n) for v in range(u + 1, n)],
                       'quotas': [(n - 1) // 2] * n})
    result.append({'name': 'infeasible-triangle', 'n': 3,
                   'edges': [[0, 1], [1, 2], [0, 2]], 'quotas': [1, 1, 1]})
    return result


def worker(case, mode):
    import networkx as nx
    start = time.perf_counter()
    reduction = reduce_graph(case['n'], case['edges'], case['quotas'], mode)
    graph = nx.Graph()
    graph.add_nodes_from(range(reduction['vertex_count']))
    graph.add_edges_from(reduction['edges'])
    build_seconds = time.perf_counter() - start
    record = {'mode': mode, 'gadget_vertices': graph.number_of_nodes(),
              'gadget_edges': graph.number_of_edges(), 'build_seconds': build_seconds,
              'local_choices': {s: reduction['choices'].count(s)
                                for s in sorted(set(reduction['choices']))}}
    print(json.dumps(record), flush=True)
    start = time.perf_counter()
    matching = nx.max_weight_matching(graph, maxcardinality=True)
    solve_seconds = time.perf_counter() - start
    covered = set()
    for u, v in matching:
        if not graph.has_edge(u, v) or u in covered or v in covered:
            raise ValueError('invalid backend matching')
        covered.update((u, v))
    perfect = len(covered) == graph.number_of_nodes()
    factor = []
    if perfect:
        for u, v in matching:
            original = reduction['cross_edges'].get(tuple(sorted((u, v))))
            if original is not None:
                factor.append(list(original))
        factor.sort()
        verify_factor(case['n'], case['edges'], case['quotas'], factor)
    record.update(status='feasible' if perfect else 'infeasible',
                  solve_seconds=solve_seconds, total_seconds=build_seconds + solve_seconds,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                  factor=factor if perfect else None,
                  verified=perfect, backend='networkx.max_weight_matching',
                  backend_version=nx.__version__)
    print(json.dumps(record), flush=True)


def campaign(timeout=15, repetitions=3):
    import networkx as nx
    records = []
    for case in cases():
        for repetition in range(repetitions):
            for mode in ('dense', 'network', 'hybrid'):
                cmd = [sys.executable, '-m', 'experiments.quota.benchmark',
                       '--worker', json.dumps(case), '--mode', mode]
                try:
                    completed = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
                    lines = completed.stdout.splitlines()
                    if completed.returncode:
                        raise RuntimeError(completed.stderr)
                    record = json.loads(lines[-1])
                except subprocess.TimeoutExpired as exc:
                    stdout = exc.stdout or b''
                    if isinstance(stdout, bytes):
                        stdout = stdout.decode()
                    lines = stdout.splitlines()
                    record = json.loads(lines[0]) if lines else {'mode': mode}
                    record.update(status='timeout', timeout_seconds=timeout)
                record.update(case=case['name'], repetition=repetition)
                records.append(record)
                print(case['name'], mode, repetition, record['status'], flush=True)
    return {'schema_version': 1, 'python': platform.python_version(),
            'networkx': nx.__version__, 'platform': platform.platform(),
            'timeout_seconds': timeout, 'repetitions': repetitions,
            'memory_measurement': 'Linux per-worker peak RSS in KiB, including interpreter/backend',
            'cases': cases(), 'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--worker')
    parser.add_argument('--mode', choices=('dense', 'network', 'hybrid'))
    parser.add_argument('--timeout', type=float, default=15)
    parser.add_argument('--repetitions', type=int, default=3)
    parser.add_argument('--output', type=Path, default=Path('experiments/quota/results.json'))
    args = parser.parse_args()
    if args.worker:
        worker(json.loads(args.worker), args.mode)
        return
    if not math.isfinite(args.timeout) or args.timeout <= 0 or args.repetitions < 1:
        parser.error('timeout and repetitions must be positive')
    result = campaign(args.timeout, args.repetitions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
