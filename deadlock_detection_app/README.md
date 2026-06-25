# ⚡ Deadlock Expert Simulator

A premium, interactive educational web application designed to teach Operating Systems students the inner workings of Deadlock Detection and Avoidance algorithms.

## 🚀 Features

- **Interactive Dry Runs**: Step-by-step visual execution with expert logical explanations.
- **Deadlock Detection**: Live simulation of the detection algorithm with resource release tracking.
- **Banker's Algorithm**: Complete safety check for deadlock avoidance.
- **Dynamic RAG Graph**: Real-time Resource Allocation Graph using Graphviz.
- **Modern UI**: Glassmorphism design with gradients, animations, and custom CSS.
- **Analytics Dashboard**: Plotly-powered insights into resource utilization and process states.
- **Educational Content**: Theory sections covering Coffman conditions and algorithm complexity.

## 🛠️ Installation

1. Clone the repository or download the source code.
2. Ensure you have Python 3.8+ installed.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃 How to Run

Navigate to the project root and execute:
```bash
streamlit run deadlock_detection_app/app.py
```

## 📂 Folder Structure

```text
deadlock_detection_app/
│
├── app.py                # Main Streamlit application
│
├── algorithms/
│   ├── detection.py      # Deadlock Detection logic
│   ├── banker.py         # Banker's Safety algorithm
│   └── rag.py            # Graphviz RAG generator
│
├── components/
│   ├── sidebar.py        # Navigation & settings
│   ├── matrix_input.py   # Data editor components
│   ├── visualization.py  # Step-by-step dry run UI
│   └── charts.py         # Plotly analytics
│
├── utils/
│   ├── validators.py     # Input validation
│   └── helpers.py        # Data conversion
│
├── assets/
│   └── styles.css        # Premium design tokens
│
└── requirements.txt      # Dependency list
```

## 🧠 Algorithm Overview

The simulator implements the standard OS Deadlock Detection algorithm:
1. **Initialize** Work vector and Finish array.
2. **Find** a process that can complete using available resources.
3. **Execute** and release resources back to the Work vector.
4. **Repeat** until no more progress can be made.
5. **Detect** deadlock if any processes remain unfinished.

---
Built with ❤️ by Senior OS Expert & Antigravity AI.
