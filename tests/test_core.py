import sys, json, asyncio
sys.path.insert(0, '..')
from core_engine import DigitalTwinTerminal, CONFIG_DATA

def test_twin_state():
    t = DigitalTwinTerminal()
    assert t.state['crane_status'] == 'OPERATIONAL'
    t.apply_transition({'crane_status': 'FAULTED'})
    assert t.state['crane_status'] == 'FAULTED'

def test_config_has_1000():
    assert CONFIG_DATA['simulation_parameters']['total_scenarios'] == 1000
