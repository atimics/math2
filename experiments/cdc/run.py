"""Produce independently checked, bounded CDC experiment records."""
import argparse
import json
import platform
from pathlib import Path

from .construction import affine_witness, construct_cover
from .graphs import fixtures, generalized_petersen
from .search import compress_cover, solve_cover
from .verify import verify_cover, verify_palette_clique


def campaign(time_limit=5.0, node_limit=100000, fixtures_only=False):
    import scipy
    graphs = fixtures()
    if not fixtures_only:
        graphs += [generalized_petersen(n, k) for n, k in [(7, 2), (8, 3), (9, 2)]]
    graphs.append(dict(fixtures()[3], name='petersen-k6-palette'))
    records = []
    for graph in graphs:
        if graph['name'] == 'petersen-k6-palette':
            flow = [6, 5, 3, 7, 1, 5, 2, 1, 4, 4, 4, 7, 3, 2, 6]
            construction = {'status': 'found', 'method': 'specified_nonzero_flow',
                            'witness': affine_witness(graph, flow)}
        else:
            construction = construct_cover(graph, node_limit=node_limit)
        if construction['status'] != 'found':
            records.append({'graph': graph, 'construction': construction})
            continue
        construction['verification'] = verify_cover(graph, construction['witness'])
        compression = compress_cover(construction['witness'], 5, node_limit=node_limit)
        if compression['witness'] is not None:
            compression['verification'] = verify_cover(graph, compression['witness'])
        if graph['name'] == 'petersen-k6-palette':
            compression['metadata']['clique_certificate'] = verify_palette_clique(
                construction['witness'], [1, 2, 3, 5, 6, 7], 5)
        searches = {}
        for k in (4, 5):
            result = solve_cover(graph, k, time_limit=time_limit)
            if result['witness'] is not None:
                result['verification'] = verify_cover(graph, result['witness'])
            searches[str(k)] = result
        records.append({'graph': graph, 'construction': construction,
                        'compression_to_five': compression, 'unrestricted': searches})
    return {'schema_version': 1,
            'environment': {'python': platform.python_version(), 'scipy': scipy.__version__},
            'scope': 'Selected simple connected bridgeless cubic graphs; not exhaustive.',
            'limits': {'time_limit_per_milp_seconds': time_limit, 'node_limit': node_limit},
            'records': records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('experiments/cdc/results.json'))
    parser.add_argument('--time-limit', type=float, default=5.0)
    parser.add_argument('--node-limit', type=int, default=100000)
    parser.add_argument('--fixtures-only', action='store_true')
    args = parser.parse_args()
    result = campaign(args.time_limit, args.node_limit, args.fixtures_only)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    for record in result['records']:
        print(record['graph']['name'], record['construction']['status'],
              record.get('compression_to_five', {}).get('status'),
              {k: v['status'] for k, v in record.get('unrestricted', {}).items()})


if __name__ == '__main__':
    main()
