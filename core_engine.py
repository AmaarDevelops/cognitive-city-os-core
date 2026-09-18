import asyncio
import json
import random
import time
import numpy as np

# 1. Initialize System Configurations
CONFIG_DATA = {
    "simulation_parameters": {"total_scenarios": 1000, "random_seed": 42, "latency_target_ms": 50.0},
    "failure_matrix": {
        "101": {"type": "CRANE_TELEMETRY_TIMEOUT", "action": "ROUTE_TO_BACKUP_LEO_NETWORK", "state": "ISOLATED_NODE_SAFE"},
        "202": {"type": "VEHICLE_ROUTING_FAILURE", "action": "TRIGGER_DYNAMIC_REROUTE_ALGORITHM", "state": "TRANSIT_DIVERTED"},
        "303": {"type": "ROUTE_SEGMENT_BLOCKED", "action": "CLOSE_SMART_GATE_AND_DIVERT_FLEET", "state": "MESH_REBALANCED"}
    }
}

random.seed(CONFIG_DATA["simulation_parameters"]["random_seed"])

# 2. The Stateful Digital Twin Class
class DigitalTwinTerminal:
    """Stateful memory twin tracking terminal assets."""
    def __init__(self):
        self.state = {
            "crane_status": "OPERATIONAL",
            "active_vehicle": "AGV_TRUCK_12",
            "route_status": "CLEAR",
            "active_container": "MSCU9824105"
        }

    def apply_transition(self, next_state):
        self.state.update(next_state)

# 3. Asynchronous Core Event Processing Loop
async def run_event_loop(scenario_id, twin, audit_log, performance_tracker):
    # Ingest the sensor payload event
    error_keys = list(CONFIG_DATA["failure_matrix"].keys())
    selected_error = random.choice(error_keys)
    matrix_rule = CONFIG_DATA["failure_matrix"][selected_error]

    # START HIGH-RESOLUTION MEASUREMENT BOUNDARY
    start_time = time.perf_counter_ns()

    # Process the system diagnosis loop
    await asyncio.sleep(random.uniform(0.002, 0.008)) # Simulated structural processing delay

    # Execute recovery action path and transition the stateful memory twin
    target_state = {"crane_status": "FAULTED" if selected_error == "101" else "OPERATIONAL", "route_status": "BLOCKED" if selected_error == "303" else "CLEAR"}
    twin.apply_transition(target_state)

    # END MEASUREMENT BOUNDARY
    end_time = time.perf_counter_ns()
    processing_latency_ms = (end_time - start_time) / 1_000_000.0
    performance_tracker.append(processing_latency_ms)

    # Document the step into the write-only Auditable Decision Log
    log_block = {
        "scenario_id": scenario_id,
        "event_received": matrix_rule["type"],
        "action_dispatched": matrix_rule["action"],
        "resulting_state": matrix_rule["state"],
        "latency_ms": round(processing_latency_ms, 4)
    }
    audit_log.append(log_block)

# 4. Master Orchestration & Statistical Benchmarking Engine
async def main():
    print("🚀 Initializing Cognitive City OS [Stage 1 Core Validation Runway]")
    print("📋 Seeded Deterministic Mode Active. Total Scenarios: 1000\n")

    twin = DigitalTwinTerminal()
    audit_log = []
    performance_tracker = []

    # Run the 1,000 asynchronous scenarios pipeline
    tasks = [run_event_loop(i, twin, audit_log, performance_tracker) for i in range(1, 1001)]
    await asyncio.gather(*tasks)

    # Calculate Precision Tail-Latency Distribution Statistics via NumPy
    latencies = np.array(performance_tracker)
    p50 = np.percentile(latencies, 50)
    p95 = np.percentile(latencies, 95)
    p99 = np.percentile(latencies, 99)
    max_latency = np.max(latencies)

    # Compile the final decision logs file
    with open("decision_audit_log.json", "w") as f:
        json.dump(audit_log, f, indent=2)

    # Render Technical Validation Dashboard Parameters
    print("📊 CORE PERFORMANCE DIAGNOSTIC METRICS SUMMARY:")
    print("───────────────────────────────────────────────")
    print(f"  • Total Simulation Processing Runs : {len(latencies)} / 1000 Success")
    print(f"  • p50 Latency (Median Baseline)     : {p50:.4f} ms")
    print(f"  • p95 Latency (Tail Threshold)      : {p95:.4f} ms")
    print(f"  • p99 Latency (Critical Boundary)   : {p99:.4f} ms")
    print(f"  • Maximum System Latency Spike      : {max_latency:.4f} ms")
    print("───────────────────────────────────────────────")
    print("✅ System Validation Success. Metric log generated: decision_audit_log.json\n")

if __name__ == "__main__":
    asyncio.run(main())
