"""mc prismscpfe parameters subcommand"""

import sys
import prismscpfe_mcapi
from prismscpfe_mcapi.prismscpfe_parameter_parser import parse_parameters_file
from materials_commons.cli import ListObjects
from materials_commons.cli.functions import make_local_project, make_local_expt


def get_parameters_sample(expt, sample_id=None, out=sys.stdout):
    """
    Return a PRISMS-CPFE Input File sample from provided Materials Commons
    experiment and optionally explicit sample id. Returns None if sample_id is None
    and zero or >1 PRISMS-CPFE Input File samples exist in the experiment.

    Arguments:

        expt: mcapi.Experiment object

        sample_id: str, optional (default=None)
          Sample id to use explicitly

    Returns:

        parameters: mcapi.Sample instance, or None
          A PRISMS-CPFE Input File sample, or None if not found uniquely

    """
    if sample_id is None:
        candidate_parameters = [proc for proc in expt.get_all_processes() if proc.template_id == prismscpfe_mcapi.templates['input_parameters']]
        if len(candidate_parameters) == 0:
            out.write('Did not find a Numerical Parameters sample.\n')
            out.write('Use \'mc prismscpfe numerical-parameters --create\' to create a Numerical Parameters sample, or --parameters-id <id> to specify explicitly.\n')
            out.write('Aborting\n')
            return None
        if len(candidate_parameters) > 1:
            out.write('Found multiple Numerical Parameters samples:')
            for cand in candidate_parameters:
                out.write(cand.name + '  id: ' + cand.id + '\n')
            out.write('Use --parameters-id <id> to specify explicitly\n')
            out.write('Aborting\n')
            return None
        parameters_proc = candidate_parameters[0]
        parameters_proc.decorate_with_output_samples()
        return parameters_proc.output_samples[0]
    else:
        # print("The sample id is: ")
        # print(sample_id[0])

        # This is broken, temporarily replaced by a more complicated work-around
        # parameters = expt.get_sample_by_id(sample_id)

        sample_found = False
        for proc in expt.get_all_processes():
            for sample in proc.get_all_samples():
                if sample.id == sample_id[0]:
                    # print("Sample found with id of: ", sample.id)
                    parameters = sample
                    sample_found = True
                    break
            if sample_found:
                break

    return parameters


def create_parameters_sample(expt, sample_name=None, verbose=False):
    """
    Create a PRISMS-CPFE Numerical Parameters Sample

    Assumes expt.project.path exists and adds files relative to that path.

    Arguments:

        expt: mcapi.Experiment object

        sample_name: str
          Name for sample, default is: Numerical Parameters

        verbose: bool
          Print messages about uploads, etc.

    Returns:

        proc: mcapi.Process instance
          The Process that created the sample
    """
    template_id = prismscpfe_mcapi.templates['numerical-parameters']

    print("The template ID is: " + template_id)
    ## Process that will create samples
    proc = expt.create_process_from_template(template_id)

    proc.rename('Set ' + 'Numerical Parameters')

    ## Create sample
    if sample_name is None:
        sample_name = "Numerical Parameters"
    new_sample = proc.create_samples([sample_name])

    proc = expt.get_process_by_id(proc.id)

    # Populate the list of numerical parameter descriptors used in parameters.in (skipping anything in a subsection for now)
    # The order of entries is "descriptor string in parameters.in", "type", "default value", "the subsection name" (if applicable)
    parameter_descriptor_list = []
    parameter_descriptor_list.append(('Order of finite elements', 'string', '1', ''))
    parameter_descriptor_list.append(('Order of quadrature', 'string', '1', ''))
    parameter_descriptor_list.append(('Domain size X', 'string', '-1', ''))
    parameter_descriptor_list.append(('Domain size Y', 'string', '-1', ''))
    parameter_descriptor_list.append(('Domain size Z', 'string', '-1', ''))
    parameter_descriptor_list.append(('Subdivisions X', 'string', '1', ''))
    parameter_descriptor_list.append(('Subdivisions Y', 'string', '1', ''))
    parameter_descriptor_list.append(('Subdivisions Z', 'string', '1', ''))
    parameter_descriptor_list.append(('Refine factor', 'string', '-1', ''))
    parameter_descriptor_list.append(('Write Mesh To EPS', 'string', 'false', ''))

    parameter_descriptor_list.append(('Write Output', 'string', 'false', ''))
    parameter_descriptor_list.append(('Output Directory', 'string', '.', ''))
    parameter_descriptor_list.append(('Skip Output Steps', 'string', '-1', ''))

    parameter_descriptor_list.append(('Output Equivalent strain', 'string', 'false', ''))
    parameter_descriptor_list.append(('Output Equivalent stress', 'string', 'false', ''))
    parameter_descriptor_list.append(('Output Grain ID', 'string', 'false', ''))
    parameter_descriptor_list.append(('Output Twin fractions', 'string', 'false', ''))
	
    parameter_descriptor_list.append(('Boundary condition filename', 'string', 'BCinfo.txt', ''))
    parameter_descriptor_list.append(('BC file number of header lines', 'string', '2', ''))
    parameter_descriptor_list.append(('Number of boundary conditions', 'string', '-1', ''))
    parameter_descriptor_list.append(('Enable cyclic loading', 'string', 'false', ''))
    parameter_descriptor_list.append(('Cyclic loading face', 'string', '-1', ''))
    parameter_descriptor_list.append(('Cyclic loading direction', 'string', '-1', ''))
    parameter_descriptor_list.append(('Quarter cycle time', 'string', '-1', ''))
	
	
    parameter_descriptor_list.append(('Time increments', 'string', '-1', ''))
    parameter_descriptor_list.append(('Total time', 'string', '-1', ''))
    parameter_descriptor_list.append(('Maximum linear solver iterations', 'string', '-1', ''))
    parameter_descriptor_list.append(('Relative linear solver tolerance', 'string', '-1', ''))
    parameter_descriptor_list.append(('Maximum non linear iterations', 'string', '-1', ''))
    parameter_descriptor_list.append(('Absolute nonLinear solver tolerance', 'string', '-1', ''))
    parameter_descriptor_list.append(('Relative nonLinear solver tolerance', 'string', '-1', ''))  # Actually a list of strings
    parameter_descriptor_list.append(('Stop on convergence failure', 'string', 'false', ''))  # Actually a list of strings
    parameter_descriptor_list.append(('Enable adaptive Time stepping', 'string', 'false', ''))
    parameter_descriptor_list.append(('Adaptive load step factor', 'string', '-1', ''))
    parameter_descriptor_list.append(('Adaptive load increase Factor', 'string', '-1', ''))  # Actually a list of ints
    parameter_descriptor_list.append(('Succesive increment for increasing time step', 'string', '1', ''))

    parameter_descriptor_list.append(('Crystal Structure', 'fcc', ' '))

    parameter_descriptor_list.append(('Elastic Stiffness row 1', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Elastic Stiffness row 2', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Elastic Stiffness row 3', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Elastic Stiffness row 4', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Elastic Stiffness row 5', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Elastic Stiffness row 6', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Number of Slip Systems', 'string', '-1', ''))
    parameter_descriptor_list.append(('Latent Hardening Ratio', 'string', '-1', ''))
    parameter_descriptor_list.append(('Initial Slip Resistance', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Initial Hardening Modulus', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Power Law Exponent', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Saturation Stress', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Slip Directions File', 'string', 'slipDirections.txt', ''))
    parameter_descriptor_list.append(('Slip Normals File', 'string', 'slipNormals.txt', ''))
    parameter_descriptor_list.append(('Backstress Factor', 'string', '-1', ''))
    parameter_descriptor_list.append(('Twinning enabled', 'string', 'false', ''))
    parameter_descriptor_list.append(('Number of Twin Systems', 'string', '-1', ''))
    parameter_descriptor_list.append(('Initial Slip Resistance Twin', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Initial Hardening Modulus Twin', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Power Law Exponent Twin', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Saturation Stress Twin', 'string', '0,0,0,0,0,0', ''))  # Actually a list of doubles
    parameter_descriptor_list.append(('Twin Saturation Factor', 'string', '-1', ''))
    parameter_descriptor_list.append(('Twin Threshold Fraction', 'string', '-1', ''))
    parameter_descriptor_list.append(('Twin Directions File', 'string', 'twinDirections.txt', ''))
    parameter_descriptor_list.append(('Twin Normals File', 'string', 'twinNormals.txt', ''))
    parameter_descriptor_list.append(('Characteristic Twin Shear', 'string', '-1', ''))
	
    parameter_descriptor_list.append(('Stress Tolerance', 'string', '-1', ''))
    parameter_descriptor_list.append(('Max Plastic Slip L2 Norm', 'string', '-1', ''))
    parameter_descriptor_list.append(('Max Slip Search Iterations', 'string', '-1', ''))
    parameter_descriptor_list.append(('Max Solver Iterations', 'string', '-1', ''))
	
    parameter_descriptor_list.append(('Voxels in X direction', 'string', '-1', ''))
    parameter_descriptor_list.append(('Voxels in Y direction', 'string', '-1', ''))
    parameter_descriptor_list.append(('Voxels in Z direction', 'string', '-1', ''))
    parameter_descriptor_list.append(('Grain ID file name', 'string', 'grainID.txt', ''))
    parameter_descriptor_list.append(('Header Lines GrainID File', 'string', '-1', ''))
    parameter_descriptor_list.append(('Orientations file name', 'string', 'orientations.txt', ''))
	
    parameter_dictionary = parse_parameters_file()

    for parameter_descriptor in parameter_descriptor_list:
        # The standard case where a parameter is directly set in the parameters file
        if parameter_descriptor[0] in parameter_dictionary:
            parameter_value = parameter_dictionary[parameter_descriptor[0]]
            parameter_description = parameter_descriptor[0]

            if parameter_descriptor[1] == 'double':
                proc.add_number_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'int':
                proc.add_integer_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'string':
                proc.add_string_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'bool':
                proc.add_boolean_measurement(parameter_description, parameter_value)

        # The default value if the parameter isn't set in the parameters file
        elif len(parameter_descriptor[3]) < 1:
            parameter_value = parameter_descriptor[2]
            parameter_description = parameter_descriptor[0]

            if parameter_descriptor[1] == 'double':
                proc.add_number_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'int':
                proc.add_integer_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'string':
                proc.add_string_measurement(parameter_description, parameter_value)
            elif parameter_descriptor[1] == 'bool':
                proc.add_boolean_measurement(parameter_description, parameter_value)

        else:
            # Need to find all versions of the parameters in subsections
            base_subsection_name = parameter_descriptor[3]
            base_subsection_name = base_subsection_name[:-1]

            for entry in parameter_dictionary:
                if entry[:len(base_subsection_name)] == base_subsection_name and entry[-len(parameter_descriptor[0]):] == parameter_descriptor[0]:
                    parameter_value = parameter_dictionary[entry]
                    parameter_description = entry

                    if parameter_descriptor[1] == 'double':
                        proc.add_number_measurement(parameter_description, parameter_value)
                    elif parameter_descriptor[1] == 'int':
                        proc.add_integer_measurement(parameter_description, parameter_value)
                    elif parameter_descriptor[1] == 'string':
                        proc.add_string_measurement(parameter_description, parameter_value)
                    elif parameter_descriptor[1] == 'bool':
                        proc.add_boolean_measurement(parameter_description, parameter_value)




    # new_sample[0].pretty_print(shift=0, indent=2, out=sys.stdout)

    parameters_file = expt.project.add_file_by_local_path('parameters.in', verbose=verbose)  # I need to pass in the path to the PRISMS-CPFE app folder
    proc.add_files([parameters_file])
    parameters_fileSlipDirection = expt.project.add_file_by_local_path('slipDirections.txt', verbose=verbose)  # I need to pass in the path to the PRISMS-CPFE app folder
    proc.add_files([parameters_fileSlipDirection])
    parameters_fileNormalDirection = expt.project.add_file_by_local_path('slipNormals.txt', verbose=verbose)  # I need to pass in the path to the PRISMS-CPFE app folder
    proc.add_files([parameters_fileNormalDirection])

    parameters_fileTwinDirection = expt.project.add_file_by_local_path('twinDirections.txt', verbose=verbose)  # I need to pass in the path to the PRISMS-CPFE app folder
    proc.add_files([parameters_fileTwinDirection])
    parameters_fileTwinNormalDirection = expt.project.add_file_by_local_path('twinNormals.txt', verbose=verbose)  # I need to pass in the path to the PRISMS-CPFE app folder
    proc.add_files([parameters_fileTwinNormalDirection])
    return expt.get_process_by_id(proc.id)


class NumParametersSubcommand(ListObjects):
    desc = "(sample) PRISMS-CPFE Numerical Parameters"

    def __init__(self):
        super(NumParametersSubcommand, self).__init__(["prismscpfe", "numerical-parameters"], "Numerical Parameters", "Numerical_Parameters",
            desc="Uploads parameters.in and creates an entity (sample) representing the numerical parameters.",
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
        proc = create_parameters_sample(expt, verbose=True)
        out.write('Created process: ' + proc.name + ' ' + proc.id + '\n')


    def add_create_options(self, parser):
        #some_option_help = "Some option help info"
        #parser.add_argument('--some_option', action="store_true", default=False, help=some_option_help)
        return

    def list_data(self, obj):
        return {
            'name': _trunc_name(obj),
            'owner': obj.owner,
            'template_name': obj.template_name,
            'id': obj.id,
            'mtime': _format_mtime(obj.mtime)
        }
