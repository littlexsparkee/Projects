import argparse
import os.path as o
from pathlib import Path
import itertools
from stdlib_list import stdlib_list

libraries = stdlib_list("3.8")

def readfile(file):
    f = open(path(file), "r").readlines()
    return f

def extract_modules(file, results = {}):
    packages = [parse(x) for x in readfile(file) if 'import' in x]
    if packages:
        results[file] = packages
        for p in packages:
            if p not in libraries:
                extract_modules(p)
    return results

def parse(statement):
    return statement.rstrip().split()[1].replace('.','/')

def format(mod, main):
    m = extract_modules(main)
    unique_mods = set(list(itertools.chain(*[[x] + y for x,y in zip(m, m.values())])))
    unused = all([mod + '.' not in ''.join(readfile(x)) for x in unique_mods if x not in libraries])
    if unused:
        return ' '.join([mod, '(unused)'])
    elif mod in libraries:
        return ' '.join([mod, '(stdlib)'])
    else:
        return mod

def path(mod):
    dir = o.dirname(parser.input)
    return o.join(dir, mod + '.py')

def gen_graphs(file):
    out = []
    deps = extract_modules(file)
    for x in deps[file]:
        if x in deps.keys():
            for y in deps[x]:
                out.append([y, x])
        else:
            out.append([x])
    return [' <- '.join([format(y, file) for y in x] + [file]) for x in out]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dependency graph tool')
    parser.add_argument('--input', type=str, dest='input',
                        help='Specify file to generate for')
    gen_graphs(Path(parser.input).stem)
