"""PRISMS-CPFE - Materials Commons interface"""

# from prismscpfe_mcapi.main import prismscpfe_subcommand
from .main import prismscpfe_subcommand


def set_templates(value=None):
    """
    Enable swapping out templates
    """
    global templates

    if value is None:
        # dictionary of cmdname -> template_id
        templates = {
          'numerical-parameters': 'global_Crystal Plasticity Simulation: Input File',
          'Orientations': 'global_Crystal Plasticity Simulation: List of Orientations',
          'BoundaryConditions': 'global_Crystal Plasticity Simulation: Boundary Conditions',
          'GrainId': 'global_Crystal Plasticity Simulation: GrainIDs for every voxel',
          'Simulation': 'global_Crystal Plasticity Simulation',
        }
    else:
        templates = value

# set default template ids
set_templates()

# specify the version of PRISMS-CPFE these functions work for
VERSION = "1.0.0"
MCAPI_NAME = "prismscpfe"
MCAPI_DESC = "Create and inspect PRISMS-CPFE samples, processes, measurements, etc."
MCAPI_MODULE = "prismscpfe_mcapi"
MCAPI_SUBCOMMAND = "prismscpfe_subcommand"

__all__ = [
    'MCAPI_NAME',
    'MCAPI_DESC',
    'prismscpfe_subcommand',
    'set_templates']
