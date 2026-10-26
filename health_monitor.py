# health_monitor.py
from abc import ABC, abstractmethod
from cyclonedds.domain import DomainParticipant
from cyclonedds.sub import DataReader
from cyclonedds.topic import Topic
from telemetry import AltitudeState
import time

# 1. The Strict Contract (Abstract Base Class)
class BaseAltimeter(ABC):
    @abstractmethod
    def read_altitude(self) -> float:
        """Returns current altitude in meters."""
        pass

# 2. The Core Mission Logic (Hardware/Network Agnostic)
class FlightController:
    # Applying Dependency Injection
    def __init__(self, altimeter: BaseAltimeter):
        self.altimeter = altimeter

    def check_safety_violation(self) -> bool:
        altitude = self.altimeter.read_altitude()
        if altitude is not None and altitude < 500.0:
            print(f"SAFETY VIOLATION: Altitude dropped to {altitude:.2f}m")
            return True
        return False

# 3. The Physical/Middleware Implementation
class DDSAltimeter(BaseAltimeter):
    def __init__(self):
        self.participant = DomainParticipant()
        self.topic = Topic(self.participant, 'AltitudeTelemetry', AltitudeState)
        self.reader = DataReader(self.participant, self.topic)

    def read_altitude(self) -> float | None:
        # Reads the latest message from the DDS network
        for msg in self.reader.take_iter(timeout=1):
            return msg.current_altitude
        return None

if __name__ == "__main__":
    print("Listening for telemetry on DDS network...")
    
    # Instantiate the DDS reader and inject it into the controller
    dds_sensor = DDSAltimeter()
    controller = FlightController(dds_sensor)
    
    # Run the continuous monitor
    while True:
        controller.check_safety_violation()
        time.sleep(0.1)