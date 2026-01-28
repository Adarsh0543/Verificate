# 🔗 verificate: Decentralized Verification for a Trusted World

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey?style=for-the-badge&logo=flask)
![Ethereum](https://img.shields.io/badge/Ethereum-Solidity-black?style=for-the-badge&logo=ethereum)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**verificate** is a blockchain-based digital certificate issuance and verification system designed to eliminate certificate fraud. By leveraging Ethereum smart contracts, it ensures that certificates are tamper-proof, transparent, and globally verifiable without the need for centralized intermediaries.

---

## 📖 Table of Contents
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Key Features](#-key-features)
- [Installation & Setup](#-installation--setup)
- [Usage Workflow](#-usage-workflow)
- [Screenshots](#-screenshots)

---

## 🚩 Problem Statement
Traditional certification systems suffer from critical vulnerabilities:
* **Fraud:** Easy creation of fake or forged certificates.
* **Inefficiency:** Manual, time-consuming verification processes.
* **Centralization Risks:** Databases can be hacked, altered, or suffer downtime.
* **Physical Loss:** Paper certificates can be lost or damaged.

## 💡 Solution
**verificate** solves these issues by shifting trust from a central authority to the **Blockchain**.
* **Immutability:** Once issued, a certificate cannot be altered or deleted.
* **Decentralization:** Anyone with the Certificate ID can verify validity instantly.
* **Smart Automation:** Logic is handled by Smart Contracts.

---

## 🏗 System Architecture
The project follows a robust 3-layer architecture:

### 1. Frontend (Client Layer)
* **Interface:** HTML, CSS, JavaScript.
* **Templating:** Flask Jinja2 templates for dynamic rendering.
* **User Roles:** Admin, Institutions, Students/Verifiers.

### 2. Backend (Application Layer)
* **Controller:** **Flask (Python)** acts as the central logic handler.
* **Responsibilities:** Validates inputs, manages user sessions, connects to the database (for auth), generates PDF certificates, and sends emails.
* **Bridge:** Uses **Web3.py** to communicate with the Ethereum blockchain via RPC.

### 3. Blockchain (Data & Trust Layer)
* **Platform:** Ethereum (Ganache for local development).
* **Logic:** **Solidity Smart Contracts** handle the registration of institutions and storage of certificate hashes.
* **Storage:** Permanent, tamper-proof record keeping.

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Blockchain** | Ethereum, Solidity, Ganache |
| **Backend** | Python, Flask, Web3.py |
| **Frontend** | HTML5, CSS3, JavaScript, Jinja2 |
| **Database** | SQLite (User Auth & Temp Data only) |
| **Tools** | VS Code, MetaMask (optional), SMTP (Email) |

---

## 🚀 Key Features
* **Tamper-Proof Records:** Certificates are stored on the blockchain.
* **Role-Based Access:**
    * **Admin:** Verifies and approves Institutions.
    * **Institution:** Issues certificates to students.
    * **User/Verifier:** Verifies certificates using a unique ID.
* **Automated Emailing:** Sends OTPs for login and PDF certificates upon issuance.
* **PDF Generation:** Automatically generates a downloadable PDF certificate.
* **Global Verification:** Verify anywhere using a unique 36-char Certificate ID.

---
