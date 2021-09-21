from mepo.state.state import MepoState
from mepo.utilities import mepoconfig

def run(args):
    if args.style:
        style = args.style
    elif mepoconfig.has_option('init','style'):
        allowed_styles = ['naked','prefix','postfix']
        style = mepoconfig.get('init','style')
        if style not in allowed_styles:
            raise Exception(f'Detected style [{style}] from .mepoconfig is not an allowed style: {allowed_styles}')
        else:
            print(f'Found style [{style}] in .mepoconfig')
    else:
        style = None

    allcomps = MepoState.initialize(args.config,style)

    if not style:
        print(f'Initializing mepo using {args.config}')
    else:
        print(f'Initializing mepo using {args.config} with {style} style')
