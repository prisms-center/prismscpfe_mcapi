"""mc prismspf equations subcommand"""

import sys
import os.path
import subprocess
import prismscpfe_mcapi
from materials_commons.cli import ListObjects
from materials_commons.cli.functions import make_local_project, make_local_expt


def get_Orientations_sample(expt, Orientations_id=None, out=sys.stdout):
    """
    Return a PRISMS-CPFE Orientations sample from provided Materials Commons
    experiment and optionally explicit sample id. Returns None if sample_id is None
    and zero or >1 PRISMS-CPFE Orientations samples exist in the experiment.

    Arguments:

        expt: mcapi.Experiment object

        sample_id: str, optional (default=None)
          Sample id to use explicitly

    Returns:

        Orientations: mcapi.Sample instance, or None
          A PRISMS-CPFE Orientations sample, or None if not found uniquely

    """
    if sample_id is None:
        candidate_Orientations = [proc for proc in expt.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates['Orientations']]
        if len(candidate_Orientations) == 0:
            out.write('Did not find a Orientations sample.\n')
            out.write('Use \'mc prismscpfe Orientations --create\' to create a Orientations sample, or --Orientations-id <id> to specify explicitly.\n')
            out.write('Aborting\n')
            return None
        if len(candidate_Orientations) > 1:
            out.write('Found multiple Orientations samples:')
            for cand in candidate_Orientations:
                out.write(cand.name + '  id: ' + cand.id + '\n')
            out.write('Use --Orientations-id <id> to specify explicitly\n')
            out.write('Aborting\n')
            return None
        Orientations_proc = candidate_Orientations[0]
        Orientations_proc.decorate_with_output_samples()
        return Orientations_proc.output_samples[0]
    else:
        # print("The sample id is: ")
        # print(sample_id[0])

        # This is broken, temporarily replaced by a more complicated work-around
        # Orientations = expt.get_sample_by_id(sample_id)

        sample_found = False
        for proc in expt.get_all_processes():
            for sample in proc.get_all_samples():
                if sample.id == sample_id[0]:
                    # print("Sample found with id of: ", sample.id)
                    Orientations = sample
                    sample_found = True
                    break
            if sample_found:
                break

    return Orientations


def create_Orientations_sample(expt, sample_name=None, verbose=False):
    """
    Create a PRISMS-CPFE Orientations Sample

    Assumes expt.project.path exists and adds files relative to that path.

    Arguments:

        expt: mcapi.Experiment object

        sample_name: str
          Name for sample, default is: Orientations

        verbose: bool
          Print messages about uploads, etc.

    Returns:

        proc: mcapi.Process instance
          The Process that created the sample
    """
    template_id = prismscpfe_mcapi.templates['Orientations']

    print("The template ID is: " + template_id)

    file_name = "orientations.txt"
    proc = expt.create_process_from_template(template_id)
    proc.rename('Orientations Input')
    
    if sample_name is None:
        sample_name = "Orientations Input"
    new_sample = proc.create_samples([sample_name])
    proc = expt.get_process_by_id(proc.id)
    Orientations_file = expt.project.add_file_by_local_path(file_name, verbose=verbose)
    proc.add_files([Orientations_file])
    
  

        # new_sample_list[-1][0].pretty_print(shift=0, indent=2, out=sys.stdout)

    return expt.get_process_by_id(proc.id)


class OrientationsSubcommand(ListObjects):
    desc = "(sample) PRISMS-CPFE Orientations"

    def __init__(self):
        super(OrientationsSubcommand, self).__init__(["prismscpfe", "Orientations"], "Orientations", "Orientations", desc="Creates a set of entities (samples) representing the Orientations.", expt_member=True, list_columns=['name', 'owner', 'template_name', 'id', 'mtime'], creatable=True)

    def get_all_from_experiment(self, expt):
        return [proc for proc in expt.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates[self.cmdname[-1]]]

    def get_all_from_project(self, proj):
        return [proc for proc in proj.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates[self.cmdname[-1]]]

    def create(self, args, out=sys.stdout):
        proj = make_local_project()
        expt = make_local_expt(proj)
        proc = create_Orientations_sample(expt, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')


    def add_create_options(self, parser):
        """
        """

    def list_data(self, obj):
        return {
            'name': _trunc_name(obj),
            'owner': obj.owner,
            'template_name': obj.template_name,
            'id': obj.id,
            'mtime': _format_mtime(obj.mtime)
        }
