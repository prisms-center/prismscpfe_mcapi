"""CPFE - Materials Commons CLI"""

import argparse
import sys
from io import BytesIO     # for handling byte strings
from io import StringIO    # for handling unicode strings
from prismscpfe_mcapi.numerical_parameters import NumParametersSubcommand
from prismscpfe_mcapi.grainid import GrainIdSubcommand
from prismscpfe_mcapi.orientations import OrientationsSubcommand
from prismscpfe_mcapi.boundaryconditions import BoundaryConditionsSubcommand
from prismscpfe_mcapi.simulation import SimulationSubcommand
from prismscpfe_mcapi.full_simulation import FullSimulationSubcommand


# import prismscpfe_mcapi.samples

prismscpfe_usage = [
    {'name':'numerical-parameters', 'desc': NumParametersSubcommand.desc, 'subcommand': NumParametersSubcommand()},
    {'name':'GrainId', 'desc': GrainIdSubcommand.desc, 'subcommand': GrainIdSubcommand()},
    {'name':'Orientations', 'desc': OrientationsSubcommand.desc, 'subcommand': OrientationsSubcommand()},
	{'name':'BoundaryConditions', 'desc': BoundaryConditionsSubcommand.desc, 'subcommand': BoundaryConditionsSubcommand()},
    {'name':'simulation', 'desc': SimulationSubcommand.desc, 'subcommand': SimulationSubcommand()} #,
    #{'name':'full-simulation', 'desc': FullSimulationSubcommand.desc, 'subcommand': FullSimulationSubcommand()}
]


def prismscpfe_subcommand(argv=sys.argv):
    usage_help = StringIO()
    usage_help.write("mc prismscpfe <command> [<args>]\n\n")
    usage_help.write("The mc prismscpfe commands are:\n")

    for interface in prismscpfe_usage:
        usage_help.write("  {:20} {:40}\n".format(interface['name'], interface['desc']))
    interfaces = {d['name']: d for d in prismscpfe_usage}

    parser = argparse.ArgumentParser(
        description='Materials Commons - PRISMS-CPFE command line interface',
        usage=usage_help.getvalue())
    parser.add_argument('command', help='Subcommand to run')

    if len(argv) < 3:
        parser.print_help()
        return

    # parse_args defaults to [1:] for args, but you need to
    # exclude the rest of the args too, or validation will fail
    args = parser.parse_args(argv[2:3])

    '''
    if args.command in interfaces:
        interfaces[args.command]['subcommand'](argv)
    else:
        print('Unrecognized command')
        parser.print_help()
        exit(1)
    '''

    if args.command == 'full-simulation':
        FullSimulationSubcommand(argv)
    elif args.command in interfaces:
        interfaces[args.command]['subcommand'](argv)
    else:
        print('Unrecognized command')
        parser.print_help()
        exit(1)
