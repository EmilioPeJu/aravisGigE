from iocbuilder import Device, AutoSubstitution, SetSimulation
from iocbuilder.arginfo import *

from iocbuilder.modules.asyn import AsynPort
from iocbuilder.modules.ADCore import ADCore, ADBaseTemplate, includesTemplates, makeTemplateInstance

@includesTemplates(ADBaseTemplate)
class aravisCameraTemplate(AutoSubstitution):
    TemplateFile="aravisCamera.template"

class aravisCamera(AsynPort):
    '''Creates a aravisCamera camera areaDetector driver'''
    Dependencies = (ADCore,)
    # This tells xmlbuilder to use PORT instead of name as the row ID
    UniqueName = "PORT"
    _SpecificTemplate = aravisCameraTemplate
    def __init__(self, PORT, ID, CLASS, BUFFERS = 50, MEMORY = -1, **args):
        # Init the superclass
        self.__super.__init__(PORT)
        # Update the attributes of self from the commandline args
        self.__dict__.update(locals())
        # Make an instance of our template
        makeTemplateInstance(self._SpecificTemplate, locals(), args)
        # Backwards compatible Manta
        if CLASS == "AVT_Manta":
            CLASS += "_1_42"
        # Init the camera specific class
        class _tmp(AutoSubstitution):
            ModuleName = aravisCamera.ModuleName
            TrueName = "_%s" % CLASS
            TemplateFile = "%s.template" % CLASS
        makeTemplateInstance(_tmp, locals(), args)

    # __init__ arguments
    ArgInfo = _SpecificTemplate.ArgInfo + makeArgInfo(__init__,
        PORT    = Simple('Port name for the camera', str),
        ID      = Simple('Cam ip address, hostname, MAC address, or ID <manufacturer>-<serial>, (e.g. Prosilica-02-2166A-06844)', str),
        CLASS   = Choice('Camera class for custom commands',
                         ["AVT_Manta_1_42", "AVT_Manta_1_44", "AVT_Manta_1_44_4",
                          "AVT_Mako_1_52", "Prosilica_GC", "Baumer_TXG",
                          "JAI_6740", "JAI_CM140", "PGR_Flea3", "Sony_CVC_EH6300",
                          "Baumer_HXG20", "PSL_SCMOS", "PGR_Blackfly_13E4C-CS",
                          "Basler_piA640_210gm", "SVS_evo4050",
                          "Photonfocus_DR1_D2048x1088_192_G2"]),
        BUFFERS = Simple('Maximum number of NDArray buffers to be created for '
                         'plugin callbacks', int),
        MEMORY  = Simple('Max memory to allocate, should be maxw*maxh*nbuffer '
                         'for driver and all attached plugins', int))

    # Device attributes
    LibFileList = ['aravisCamera']
    DbdFileList = ['aravisCameraSupport']

    def Initialise(self):
        print '# aravisCameraConfig(portName, cameraName, ' \
            'maxBuffers, maxMemory)'
        print 'aravisCameraConfig("%(PORT)s", "%(ID)s", ' \
            '%(BUFFERS)d, %(MEMORY)d)' % self.__dict__

def aravisCamera_sim(aravisCamera=aravisCamera, **kwargs):
    kwargs.pop("ID")
    kwargs.pop("CLASS")
    return aravisCamera(ID="Fake_1", CLASS="Fake", **kwargs)

SetSimulation(aravisCamera, aravisCamera_sim)
