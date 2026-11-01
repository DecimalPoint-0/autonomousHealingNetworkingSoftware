from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from simulator import NetworkSimulator
from ml_engine import MLEngine
from healer import AutonomousHealer
from datetime import datetime

app = FastAPI(title="AI Autonomous Network Healer API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
simulator = NetworkSimulator()
ml_engine = MLEngine()
healer = AutonomousHealer(simulator)

current_metrics = {}
history = []
healing_logs = []

async def simulation_loop():
    global current_metrics, history, healing_logs
    while True:
        # 1. Generate metrics
        metrics = simulator.generate_metrics()
        
        # 2. Predict anomaly
        prediction = ml_engine.predict(metrics)
        is_anomaly = (prediction == -1)
        
        # 3. Heal if necessary
        healing_result = healer.analyze_and_heal(metrics, is_anomaly)
        
        # Update state
        metrics['is_anomaly'] = is_anomaly
        if healing_result:
            metrics['healed'] = True
            metrics['action'] = healing_result['action']
            healing_logs.append({
                "timestamp": datetime.now().isoformat(),
                **healing_result
            })
        else:
            metrics['healed'] = False

        current_metrics = metrics
        history.append(metrics)
        if len(history) > 100:
            history.pop(0)
            
        await asyncio.sleep(2) # Run every 2 seconds

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulation_loop())

@app.get("/metrics")
async def get_metrics():
    return {
        "current": current_metrics,
        "history": history[-20:],
        "healing_logs": healing_logs[-10:]
    }

@app.post("/inject-fault/{fault_type}")
async def inject_fault(fault_type: str):
    simulator.inject_fault(fault_type)
    return {"status": "success", "message": f"Fault {fault_type} injected"}

@app.post("/clear-faults")
async def clear_faults():
    simulator.clear_fault()
    return {"status": "success", "message": "All faults cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
