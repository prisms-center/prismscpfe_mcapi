# prismscpfe_mcapi: The PRISMS-CPFE/Materials Commons CLI Plugin

This is the initial version of the Materials Commons command-line-interface plugin for PRISMS-CPFE, which is still under active development. The base Materials Commons CLI can be found [here](https://github.com/materials-commons/mcapi/tree/master/python).

This plugin assists you in creating a Materials Commons representation of crystal plasticity finite element simulations conducted with PRISMS-CPFE. From the directory of your PRISMS-CPFE app, it can create Materials Commons entities representing the numerical parameters, slip system information, GrianId (Initial Texture), and list of grain orientations as well as the process for the crystal plasticity simulation itself. The metadata is populated by automatically parsing PRISMS-CPFE files and command-line arguments.

## Basic Instructions:

### Installation
- Install mcapi (`pip install mcapi`)
- Clone the prismscpfe_mcapi repository (`git clone https://github.com/prisms-center/prismscpfe_mcapi`)
- Add the location of the prismscpfe_mcapi to your Python path (`export PYTHONPATH=$PYTHONPATH:/path/to/prismscpfe_mcapi`)
- Add the interface information for PRISMS-CPFE to your .materialscommons/config.json file (typically found in your home directory). It should look like (possibly with other interfaces given as well):

        {
            "apikey": "[redacted, put your real api key here]",
            "mcurl": "https://test.materialscommons.org/api",
            "interfaces": [
               { "name": "prismscpfe",
                 "desc":"Create PRISMS-CPFE samples, processes, measurements, etc.",
                 "subcommand":"prismscpfe_subcommand",
                 "module":"prismscpfe_mcapi"
               }
            ]
        }


### Uploading metadata for a simulation (each component seperately)
- Go to the app directory for the PRISMS-CPFE simulation being conducted
- Create the numerical parameters process and sample: `mc prismscpfe numerical-parameters --create`
- Create the simulation orientations process and sample: `mc prismscpfe Orientations --create`
- Create the GrainId (Initial Texture) process and sample: `mc prismscpfe GrainId --create`
- Create the Boundary Conditions process and sample: `mc prismscpfe BoundaryConditions --create`
- Get the list of sample ids from the samples created in the previous steps: `mc samp`
- Create the crystal plasticity finite element simulation process that takes all of the previously created samples as inputs: `mc prismscpfe simulation --create --input-sample-ids SAMPLE IDS`, where 'SAMPLE IDS' is replaced with a list of the sample ids from the input samples separated by spaces

## Help
Post any questions about using this plugin at the PRISMS-CPFE forum:

https://groups.google.com/forum/#!forum/prisms-cpfe-users
