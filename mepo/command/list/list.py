from mepo.state.state import MepoState

def run(args):
    allcomps = MepoState.read_state()
    for comp in allcomps:
        print(comp.name, end=' ')
    print()
