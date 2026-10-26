# tests/test_health_monitor.py
import pytest
from unittest.mock import Mock

# We import the contract we defined earlier
from telemetry import AltitudeState
from health_monitor import FlightController, BaseAltimeter 

def test_nominal_altitude():
    """Happy path: System should not flag when above 500m."""
    mock_altimeter = Mock(spec=BaseAltimeter)
    mock_altimeter.read_altitude.return_value = 501.0
    
    controller = FlightController(mock_altimeter)
    assert controller.check_safety_violation() == False

def test_safety_violation_trigger():
    """Boundary condition: System must flag when dropping below 500m."""
    mock_altimeter = Mock(spec=BaseAltimeter)
    mock_altimeter.read_altitude.return_value = 499.9
    
    controller = FlightController(mock_altimeter)
    assert controller.check_safety_violation() == True
