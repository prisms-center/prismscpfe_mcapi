"""mc prismscpfe simulation subcommand"""

import sys
import glob
import prismscpfe_mcapi
from prismscpfe_mcapi.numerical_parameters import get_parameters_sample
from materials_commons.cli import ListObjects
from materials_commons.cli.functions import make_local_project, make_local_expt

def get_simulation_sample(expt, sample_id=None, out=sys.stdout):
    """
    Return a PRISMS-CPFE Simulation sample from provided Materials Commons
    experiment and optionally explicit sample id. Returns None if sample_id is None
    and zero or >1 PRISMS-CPFE Simulation samples exist in the experiment.

    Arguments:

        expt: mcapi.Experiment object

        sample_id: str, optional (default=None)
          Sample id to use explicitly

    Returns:

        simulation: mcapi.Sample instance, or None
          A PRISMS-CPFE Simulation sample, or None if not found uniquely

    """
    if sample_id is None:
        candidate_simulation = [proc for proc in expt.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates['simulation']]
        if len(candidate_simulation) == 0:
            out.write('Did not find a Crystal Plasticity Simulation sample.\n')
            out.write('Use \'mc prismscpfe simulation --create\' to create a Simulation sample, or --simulation -id <id> to specify explicitly.\n')
            out.write('Aborting\n')
            return None
        if len(candidate_simulation) > 1:
            out.write('Found multiple Simulation samples:')
            for cand in candidate_simulation:
                out.write(cand.name + '  id: ' + cand.id + '\n')
            out.write('Use --simulation -id <id> to specify explicitly\n')
            out.write('Aborting\n')
            return None
        simulation_proc = candidate_simulation[0]
        simulation_proc.decorate_with_output_samples()
        return simulation_proc.output_samples[0]
    else:
        # print("The sample id is: ")
        # print(sample_id[0])

        # This is broken, temporarily replaced by a more complicated work-around
        # simulation = expt.get_sample_by_id(sample_id)

        sample_found = False
        for proc in expt.get_all_processes():
            for sample in proc.get_all_samples():
                if sample.id == sample_id[0]:
                    # print("Sample found with id of: ", sample.id)
                    simulation = sample
                    sample_found = True
                    break
            if sample_found:
                break

    return simulation


def create_simulation_sample(expt, sample_list, sample_name=None, verbose=False):
    """
    Create a PRISMS-CPFE Simulation Sample

    Assumes expt.project.path exists and adds files relative to that path.

    Arguments:

        expt: mcapi.Experiment object

        sample_list: a list of mcapi.Sample object containing the input information for the simulation

        sample_name: str
          Name for sample, default is: Phase Field Simulation

        verbose: bool
          Print messages about uploads, etc.

    Returns:

        proc: mcapi.Process instance
          The Process that created the sample
    """
    template_id = prismscpfe_mcapi.templates['Simulation']

    print("The template ID is: " + template_id)
    # Process that will create samples
    proc = expt.create_process_from_template(template_id)

    # Hardcoding the name of the template
    # proc = expt.create_process_from_template('global_Create Samples')

    proc.rename('Run ' + 'Simulation')

    proc = expt.get_process_by_id(proc.id)

    print("Adding input sample(s)...")
    proc.add_input_samples_to_process(sample_list)
    print("Finshed adding input sample(s).")

    sample_name = "Simulation Results"
    new_sample = proc.create_samples([sample_name])

    # Get the names of all of the *.vtu files in the cwd
    vtu_file_names = glob.glob('*vtu')
    print(vtu_file_names)

    result_files = []
    for vtu_file in vtu_file_names:
        result_files.append(expt.project.add_file_by_local_path(vtu_file, verbose=verbose))

      # I need to pass in the path to the PRISMS-PF app folder
    for file in result_files:
        file.direction = 'out'

    proc.add_files(result_files)

    #new_sample.link_files(result_files)
    for sample in new_sample:
        sample.link_files(result_files)

    return expt.get_process_by_id(proc.id)


class SimulationSubcommand(ListObjects):
    desc = "(sample) PRISMS-CPFE Simulation"

    def __init__(self):
        super(SimulationSubcommand, self).__init__(["prismscpfe", "simulation"], "Simulation", "Simulations",
            desc="Creates an entity (sample) representing the simulation itself.",
            expt_member=True,
            list_columns=['name', 'owner', 'template_name', 'id', 'mtime'],
            creatable=True)

    def get_all_from_experiment(self, expt):
        return [proc for proc in expt.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates[self.cmdname[-1]]]

    def get_all_from_project(self, proj):
        return [proc for proc in proj.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates[self.cmdname[-1]]]

    def create(self, args, out=sys.stdout):
        proj = make_local_project()
        expt = make_local_expt(proj)

        # Get the necessary input samples

        sample_list = []
        for sample_id in args.input_sample_ids:
            sample_found = False
            for proc in expt.get_all_processes():
                for sample in proc.get_all_samples():
                    if sample.id == sample_id:
                        # print("Sample found with id of: ", sample.id)
                        matching_sample = sample
                        sample_found = True
                        break
                if sample_found:
                    break
            sample_list.append(matching_sample)

        # parameters_sample = get_parameters_sample(expt, args.input_sample_ids[0], out)

        proc = create_simulation_sample(expt, sample_list, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')


    def add_create_options(self, parser):
        input_id_help = "Specify in sample ids explicitly"
        parser.add_argument('--input-sample-ids', nargs='*', default=None, help=input_id_help)

        return

    def list_data(self, obj):
        return {
            'name': _trunc_name(obj),
            'owner': obj.owner,
            'template_name': obj.template_name,
            'id': obj.id,
            'mtime': _format_mtime(obj.mtime)
        }
