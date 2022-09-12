# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from UM.Extension import Extension
from UM.Application import Application
from UM.Logger import Logger

#from .DataApiService import DataApiService
from cura.Machines.ContainerTree import ContainerTree
from cura.CuraApplication import CuraApplication

""" Fetch materials from active BCN3D Printer and auto select them in the Material Selector """
class SyncMaterials(Extension):
    def __init__(self, application: CuraApplication):
        super().__init__()
        self._application = application
        self._testing = True
         
    def syncActivePrinterMaterials(self):
        if self._testing or CuraApplication.getInstance().getCuraAPI().account.isLoggedIn and Application.getInstance().getGlobalContainerStack().getMetaDataEntry("serial_number") :
            self.machine_manager = self._application.getMachineManager()

            # Fetch materials
            materials = self.fetchMaterials()

            # Set materials
            for m in materials:
                Logger.info(m)
                Logger.info(m.guid)
                self.setMaterialByGUID(m.pos, m.guid)
    
    def fetchMaterials(self):
        if self._testing:
            ext0 = type('ext1', (object,), {'pos': 0, 'guid': '9cfe5bf1-bdc5-4beb-871a-52c70777842d'})() #Ultimaker PLA RED
            ext1 = type('ext2', (object,), {'pos': 1, 'guid': '2433b8fb-dcd6-4e36-9cd5-9f4ee551c04c'})() #Ultimaker PLA GREEN
            materials = [ext0, ext1]
        else:
            serial_number_active_printer = Application.getInstance().getGlobalContainerStack().getMetaDataEntry("serial_number")
            materials = self._data_api_service.fetchMaterials(serial_number_active_printer) # [{pos: 0, guid: 123}, {pos:1, guid: 456}]
        return materials
    
    def setMaterialByGUID(self, position: str, material_GUID: str) -> bool:
        Logger.info(f"setMaterialByGUID")

        if self.machine_manager._global_container_stack is None:
            return False

        machine_definition_id = self.machine_manager._global_container_stack.definition.id
        position = str(position)
        extruder_stack = self.machine_manager._global_container_stack.extruderList[int(position)]
        nozzle_name = extruder_stack.variant.getName()

        materials = ContainerTree.getInstance().machines[machine_definition_id].variants[nozzle_name].materials
       
        for m in materials.items():
            material_node = m[1]
            Logger.info(material_node.guid)
            Logger.info(material_GUID)
            if material_node.guid == material_GUID:
                Logger.info(f"changed material")
                self.machine_manager.setMaterial(position, material_node)
                return True
        return False
