import time
import random

from cyclonedds.domain import DomainParticipant
from cyclonedds.pub import DataWriter
from cyclonedds.topic import Topic
from telemetry import AltitudeState

participant = DomainParticipant()
topic = Topic(participant, "AltitudeTelemetry", AltitudeState)
writer = DataWriter(participant, topic)

altitude = 1000.0

while True:
    altitude -= random.uniform(0.1, 0.2)
    msg = AltitudeState(current_altitude = altitude, timestamp = int(time.time()))
    writer.write(msg)
    print(f"Pub: {msg.current_altitude:.2f}m")
    time.sleep(0.1)
