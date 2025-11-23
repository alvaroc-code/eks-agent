# eks-agent

![Python](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white) ![License](https://img.shields.io/badge/license-MIT-green)

## 📝 Description

The eks-agent is a Site Reliability Engineering (SRE)-inspired agent built upon the Strands Agents SDK, designed to automate and streamline operational tasks within your EKS (Elastic Kubernetes Service) environment. Developed in Python, this agent provides a flexible and extensible framework for implementing proactive monitoring, automated remediation, and intelligent orchestration of your Kubernetes workloads. Key features include customizable alert handling, automated scaling policies, and integration with popular monitoring tools. Empower your team to focus on innovation by leveraging the eks-agent to ensure the reliability and efficiency of your EKS deployments.

## 🚀 Quick Start
#### 1. Clone the repo
```bash
git pull git@github.com:alvaroc-code/eks-agent.git && cd eks-agent
```
#### 2. Pull & tag image
```bash
sudo docker pull ghcr.io/alvaroc-code/eks-agent:latest && sudo docker image tag ghcr.io/alvaroc-code/eks-agent:latest eks-agent:latest
```
#### 3. Configure container environment
```bash
mv .env.sample .env (edit with your values)
```
#### 4. Run the agent
```bash
sudo docker run --rm -it --network=host -v ./.env:/app/.env eks-agent:latest -a <account-id> -r <region> -c <eks-cluster-name>
```

## 🛠️ Tech Stack

- 🐍 Python
- 🐳 Docker


## 📦 Key Dependencies

```
strands-agents: 1.0.0
strands-agents-tools: 0.2.0
```

## 📁 Project Structure

```
.
├── Dockerfile
├── LICENSE
└── app
    ├── __init__.py
    ├── eks_agent.py
    ├── entry_point.sh
    └── requirements.txt
```

## 🩺 Troubleshooting

If you encounter issues while running **eks-agent**, check the following:

#### 🐳 Docker Environment

- Ensure Docker is installed and running correctly.
- Try running a simple test container:
  ```bash
  docker run --rm -it --network=host -v ./.env:/app/.env --entrypoint /bin/bash eks-agent:latest
  ```
🔐 Environment File & Credentials

- Verify you have a valid .env file based on .env.sample.

- Ensure your AWS credentials are correct and not expired.

- Test your credentials:
```bash
aws sts get-caller-identity
```

#### ☸️ EKS Cluster Connectivity
- Make sure the EKS cluster you're targeting is reachable.

- You may need to connect to your corporate VPN or internal network.

- Verify your kubeconfig:
```bash
aws eks update-kubeconfig --region <region> --name <cluster-name>
kubectl get nodes
```
## 👥 Contributing
Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/alvaroc-code/eks-agent.git`
3. **Create** a new branch: `git checkout -b feature/your-feature`
4. **Commit** your changes: `git commit -am 'Add some feature'`
5. **Push** to your branch: `git push origin feature/your-feature`
6. **Open** a pull request

---



✨ This README was generated with readmebuddy.com and readme.so
![Python](https://img.shields.io/badge/-Python-blue?logo=python&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-blue?logo=docker&logoColor=white) [![ghcr.io](https://img.shields.io/badge/ghcr.io-eks--agent-blue?logo=docker)](https://github.com/alvaroc-code/eks-agent/pkgs/container/eks-agent) ![License](https://img.shields.io/badge/license-MIT-green)
