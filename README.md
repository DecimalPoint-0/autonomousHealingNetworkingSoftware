# AI-Driven Autonomous Network Healing System

An intelligent, self-healing network management system that uses machine learning to detect anomalies and automatically apply corrective actions.

## 🚀 Features
- **AI Anomaly Detection**: Uses Scikit-learn's Isolation Forest to identify abnormal network patterns.
- **Autonomous Healing**: Automatically executes corrective actions (scaling, re-routing, hardware failover) based on detected faults.
- **Real-time Monitoring**: High-fidelity dashboard built with React and Recharts.
- **Fault Injection**: Simulation suite to test system resilience against DDoS, Congestion, and Hardware failure.

## 🛠️ Tech Stack
- **Backend**: FastAPI (Python), Scikit-learn, Pandas, NumPy.
- **Frontend**: React (Vite), Recharts, Framer Motion, Lucide React.
- **Design**: Premium Glassmorphism UI with Neon aesthetics.

## 🚦 Getting Started

### Backend Setup
1. Navigate to `/backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python main.py`

### Frontend Setup
1. Navigate to `/frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`

## 🧠 ML Model Details
The system utilizes an **Isolation Forest** algorithm. It is trained on "normal" network behavior metrics:
- Latency (ms)
- Throughput (Mbps)
- Packet Loss (%)
- CPU Usage (%)
- Error Rate (%)

When metrics deviate significantly from the learned distribution, the system triggers an "Anomaly" state, which initiates the Healing Engine.
