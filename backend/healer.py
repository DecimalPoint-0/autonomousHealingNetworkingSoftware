import time

class AutonomousHealer:
    def __init__(self, simulator):
        self.simulator = simulator
        self.healing_history = []

    def analyze_and_heal(self, metrics, is_anomaly):
        if not is_anomaly:
            return None

        # Logic to determine what's wrong based on metrics
        action = None
        reason = "Unknown anomaly"

        if metrics['cpu_usage'] > 80:
            action = "Scaling up cloud resources & applying rate limiting"
            reason = "High CPU Load / Potential DDoS"
        elif metrics['packet_loss'] > 5:
            action = "Re-routing traffic via secondary fiber link"
            reason = "Network Congestion / Link Degradation"
        elif metrics['latency'] > 400:
            action = "Clearing routing cache & optimizing BGP paths"
            reason = "Latency Spike"
        elif metrics['throughput'] < 100:
            action = "Failing over to redundant hardware cluster"
            reason = "Hardware Failure / Critical Throughput Drop"

        if action:
            self.execute_healing(action, reason)
            return {"action": action, "reason": reason}
        
        return None

    def execute_healing(self, action, reason):
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "action": action,
            "reason": reason,
            "status": "In Progress"
        }
        self.healing_history.append(log_entry)
        
        print(f"HEALING: {action} due to {reason}")
        
        # Simulate time taken to fix
        time.sleep(1) 
        
        log_entry["status"] = "Success"
        
        # Tell the simulator to clear the fault
        self.simulator.clear_fault()
        
    def get_history(self):
        return self.healing_history
