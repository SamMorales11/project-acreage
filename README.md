# Acreage | Premium Real Estate Analytics 🏢

[![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?logo=vue.js&logoColor=white)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?logo=vercel&logoColor=white)](https://vercel.com/)
[![Hosted on Hugging Face](https://img.shields.io/badge/AI_Backend-Hugging_Face-FFD21E?logo=huggingface&logoColor=black)](https://huggingface.co/)

> **Acreage** is a sophisticated, real-time real estate analytics dashboard that uses a **Random Forest Regression** model to estimate property market values based on architectural and locational parameters. 

Built with a high-performance decoupled architecture, the application features a modern enterprise-grade UI and integrates **Explainable AI (XAI)** to provide transparent, data-driven financial insights.

🔗 **[Live Demo: View Acreage Here]** *(<- Replace this with your Vercel URL)*

---

## ✨ Key Features

* **Real-time Valuation Engine**: Instant property price estimation powered by a trained Random Forest Regressor.
* **Explainable AI (XAI)**: Visualizes the algorithmic feature importance distribution (e.g., how much Lot Area vs. Location impacts the final price) using interactive Chart.js graphics.
* **Enterprise UI/UX**: A responsive, dark-mode-optimized interface utilizing glassmorphism, built with Tailwind CSS.
* **Decoupled Architecture**: Independent frontend (Vite/Vue) and backend (FastAPI) communication via RESTful endpoints.

## 🛠️ Tech Stack

**Frontend (Client)**
* Framework: Vue.js 3 (Composition API)
* Build Tool: Vite
* Styling: Tailwind CSS v4
* Data Visualization: Chart.js
* Hosting: Vercel

**Backend (API & Machine Learning)**
* Framework: FastAPI
* Machine Learning: Scikit-Learn (Random Forest)
* Data Manipulation: Pandas, NumPy
* Hosting: Hugging Face Spaces (Dockerized)

---

## 🚀 Getting Started (Local Development)

If you want to run this project locally, follow these steps:

### Prerequisites
* Node.js (v18+)
* Python (3.10+)
* Git

### 1. Clone the repository
```bash
git clone [https://github.com/yourusername/project-acreage.git](https://github.com/yourusername/project-acreage.git)
cd project-acreage
