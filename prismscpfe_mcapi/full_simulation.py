"""mc prismspf full-simulation subcommand"""

import sys
import argparse
import prismscpfe_mcapi
from prismscpfe_mcapi.numerical_parameters import get_parameters_sample
from materials_commons.cli import ListObjects
from materials_commons.cli.functions import make_local_project, make_local_expt

class FullSimulationSubcommand:
    desc = "(sample) PRISMS-CPFE Simulation"

    def __init__(self, argv):

        parser = argparse.ArgumentParser(
            description='Creates the entire set of input samples and processes for a simulation',
            prog='mc prismscpfe full-simulation')

        parser.add_argument('--create', action='store_true', help='Creates the input processes, input samples, and the simulation prcoess.')

        num_cores_help = "Add the number of cores to be used in the simulation"
        parser.add_argument('--num-cores', default=-1, help=num_cores_help)


        if argv[3] == '--create':
            self.create(parser, argv)
        else:
            parser.print_help()

    def create(self, parser):
        out = sys.stdout

        proj = make_local_project()
        expt = make_local_expt(proj)

        sample_list = []

        proc = prismscpfe_mcapi.numerical_parameters.create_parameters_sample(expt, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')
        sample_list.extend(proc.output_samples)

        proc = prismscpfe_mcapi.GrainID.create_GrainID_sample(expt, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')
        sample_list.extend(proc.output_samples)
		
        proc = prismscpfe_mcapi.Orientations.create_Orientations_sample(expt, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')
        sample_list.extend(proc.output_samples)
