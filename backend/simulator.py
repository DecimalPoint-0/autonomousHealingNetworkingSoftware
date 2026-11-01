import random
import time
from datetime import datetime

class NetworkSimulator:
    def __init__(self):
        self.normal_metrics = {
            "latency": (10, 30),      # ms
            "throughput": (800, 1000), # Mbps
            "packet_loss": (0, 0.5),   # %
            "cpu_usage": (15, 45),     # %
            "error_rate": (0, 0.1)     # %
        }
        self.active_fault = None
        self.fault_start_time = None

    def inject_fault(self, fault_type):
        """
        Types: 'congestion', 'ddos', 'hardware_failure', 'latency_spike'
        """
        self.active_fault = fault_type
        self.fault_start_time = time.time()
        print(f"DEBUG: Injected fault: {fault_type}")

    def clear_fault(self):
        self.active_fault = None
        self.fault_start_time = None
        print("DEBUG: Cleared all faults.")

    def generate_metrics(self):
        metrics = {}
        
        # Base normal values
        for key, (low, high) in self.normal_metrics.items():
            metrics[key] = round(random.uniform(low, high), 2)

        # Apply fault impacts
        if self.active_fault == 'congestion':
            metrics['latency'] *= random.uniform(3, 5)
            metrics['throughput'] *= random.uniform(0.2, 0.5)
            metrics['packet_loss'] += random.uniform(2, 5)
        
        elif self.active_fault == 'ddos':
            metrics['cpu_usage'] = round(random.uniform(85, 99), 2)
            metrics['latency'] *= random.uniform(10, 20)
            metrics['packet_loss'] += random.uniform(5, 15)
            metrics['error_rate'] += random.uniform(10, 30)

        elif self.active_fault == 'hardware_failure':
            metrics['throughput'] = round(random.uniform(0, 50), 2)
            metrics['packet_loss'] = round(random.uniform(50, 100), 2)
            metrics['error_rate'] = round(random.uniform(20, 50), 2)

        elif self.active_fault == 'latency_spike':
            metrics['latency'] = round(random.uniform(500, 1500), 2)
            metrics['packet_loss'] += random.uniform(1, 3)

        metrics['timestamp'] = datetime.now().isoformat()
        metrics['fault'] = self.active_fault if self.active_fault else "None"
        
        return metrics

if __name__ == "__main__":
    sim = NetworkSimulator()
    for _ in range(5):
        print(sim.generate_metrics())
        time.sleep(1)
