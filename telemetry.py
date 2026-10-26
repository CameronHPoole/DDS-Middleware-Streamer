from cyclonedds.idl import IdlStruct
from dataclasses import dataclass

@dataclass
class AltitudeState(IdlStruct, typename = "MissionOps.AltitudeState"):
    """Defines an IDL struct for the AltitudeState, including current alt (float) and time (int)

    Args:
        IdlStruct (_type_): _description_
        typename (str, optional): _description_. Defaults to "MissionOps.AltitudeState".
    """
    current_altitude: float
    timestamp: int