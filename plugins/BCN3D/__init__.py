# Copyright (c) 2018 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

#from . import SyncMaterials
from .SyncMaterialsAction import SyncMaterialsMachineAction

def getMetaData():
    return {}

def register(app):
    return { 
        #"extension": SyncMaterials.SyncMaterials(app),
        "machine_action": [SyncMaterialsMachineAction.SyncMaterialsMachineAction(app)]
     }
