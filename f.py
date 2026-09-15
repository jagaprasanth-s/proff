import json
from typing import List, Dict, Any, Tuple
from . import db

SFIA_CHUNKS = [
    {
        "chunk_index": 1,
        "skill_name": "Prompt Engineering",
        "category": "Artificial Intelligence & Machine Learning",
        "skill_type": "Technical Competency",
        "content": "Skill Code: PROMP-L4. Prompt Engineering is the systematic design, evaluation, and refinement of contextual prompts to guide foundation and large language models (LLMs) toward precise, verifiable outputs. Competencies include zero-shot/few-shot design, chain-of-thought prompting, guardrail implementation against prompt injection, and output formatting validation.",
        "definition": "The systematic design, evaluation, and refinement of contextual prompts to guide foundation models toward accurate, structured outputs.",
        "related_skills": ["Machine Learning", "Natural Language Processing", "Fine-Tuning"],
        "differences": {
            "vs Fine-Tuning": "Prompt Engineering optimizes instructions at inference without updating model weights; Fine-Tuning retrains internal weights on custom datasets.",
            "vs Traditional Programming": "Prompt Engineering steers probabilistic generative models via natural language constraints rather than deterministic control flow."
        }
    },
    {
        "chunk_index": 2,
        "skill_name": "Machine Learning Operations (MLOps)",
        "category": "Artificial Intelligence & Machine Learning",
        "skill_type": "Technical Competency",
        "content": "Skill Code: MLOPS-L5. MLOps is the operational discipline of applying DevOps principles to machine learning system lifecycles. It encompasses continuous integration, continuous delivery (CI/CD), automated data validation, model registry governance, concept drift monitoring, and scalable serving infrastructure.",
        "definition": "The operational framework for automating the deployment, governance, continuous monitoring, and lifecycle management of machine learning models in production.",
        "related_skills": ["DevOps", "Data Engineering", "Machine Learning"],
        "differences": {
            "vs Standard DevOps": "DevOps focuses on deterministic software code deployment; MLOps must additionally govern non-deterministic data drift, model retraining, and feature stores.",
            "vs Data Science": "Data Science focuses on research and model prototyping; MLOps focuses on production pipeline scalability and 24/7 reliability."
        }
    },
    {
        "chunk_index": 3,
        "skill_name": "Data Science",
        "category": "Data Engineering & Analytics",
        "skill_type": "Technical Competency",
        "content": "Skill Code: DATSC-L4. Data Science applies scientific methods, statistical modeling, algorithmic experimentation, and domain expertise to extract actionable insights and predictive capabilities from complex structured and unstructured datasets.",
        "definition": "The discipline of utilizing scientific, statistical, and algorithmic techniques to develop predictive hypotheses and discover actionable patterns in datasets.",
        "related_skills": ["Data Analytics", "Data Engineering", "Machine Learning"],
        "differences": {
            "vs Data Analytics": "Data Analytics describes historical business performance (what happened); Data Science constructs predictive mathematical models (what will happen).",
            "vs Data Engineering": "Data Engineers build ingestion pipelines and warehouses; Data Scientists explore hypotheses and train analytical models."
        }
    },
    {
        "chunk_index": 4,
        "skill_name": "Data Analytics",
        "category": "Data Engineering & Analytics",
        "skill_type": "Technical Competency",
        "content": "Skill Code: DAANA-L3. Data Analytics focuses on transforming structured data into actionable business intelligence through descriptive and diagnostic analytical techniques. Competencies include SQL data aggregation, KPI dashboarding (PowerBI, Tableau), metric cohort segmentation, and variance analysis.",
        "definition": "The practice of examining, transforming, and visualizing business datasets to diagnose performance trends and support decision-making.",
        "related_skills": ["Data Science", "Business Intelligence", "Data Governance"],
        "differences": {
            "vs Data Science": "Data Analytics is descriptive/diagnostic focusing on business metrics; Data Science is predictive/prescriptive using machine learning algorithms."
        }
    }
]

ONET_CHUNKS = [
    {
        "chunk_index": 1,
        "skill_name": "Cloud Security Architecture",
        "category": "Cybersecurity & Governance",
        "skill_type": "Architectural Standard",
        "content": "O*NET SOC 15-1212.00: Cloud Security Architecture defines security postures across multi-cloud environments. Encompasses Identity and Access Management (IAM), mutual TLS, micro-segmentation, posture management (CSPM), and automated vulnerability assessment.",
        "definition": "The architectural design and enforcement of security controls, identity boundaries, and cryptographic protection across multi-cloud and distributed infrastructure.",
        "related_skills": ["Zero Trust Architecture", "Cloud Infrastructure", "Penetration Testing"],
        "differences": {
            "vs Traditional Network Security": "Cloud Security relies on identity-centric perimeterless boundaries rather than static hardware firewall appliances."
        }
    },
    {
        "chunk_index": 2,
        "skill_name": "Zero Trust Architecture",
        "category": "Cybersecurity & Governance",
        "skill_type": "Architectural Standard",
        "content": "NIST SP 800-207 / O*NET 15-1212.00: Zero Trust is an enterprise cybersecurity architecture rooted in 'never trust, always verify'. Requires continuous authentication, microsegmentation, and ephemeral least-privilege access for all users, workloads, and devices.",
        "definition": "A security paradigm requiring continuous cryptographic verification and explicit authorization for every transaction, regardless of network location.",
        "related_skills": ["Cloud Security Architecture", "Identity & Access Management", "Network Segmentation"],
        "differences": {
            "vs Castle-and-Moat Security": "Perimeter defense trusts any device inside the internal network; Zero Trust enforces continuous re-authentication for every request."
        }
    },
    {
        "chunk_index": 3,
        "skill_name": "Site Reliability Engineering (SRE)",
        "category": "Cloud Infrastructure & DevOps",
        "skill_type": "Operational Discipline",
        "content": "O*NET SOC 15-1252.00: SRE applies software engineering practices to infrastructure operations. Core practices include defining Service Level Objectives (SLOs) and Error Budgets, blameless postmortems, toilsome task automation, and chaos testing.",
        "definition": "The practice of applying software engineering principles to automate system administration and guarantee target uptime and service reliability.",
        "related_skills": ["DevOps", "Infrastructure as Code", "Incident Response"],
        "differences": {
            "vs Traditional System Administration": "Sysadmins manually handle tickets and patch servers; SREs write software to automate failover and enforce error budgets."
        }
    }
]

def load_seed_data() -> Tuple[bool, str]:
    existing_docs = db.get_all_documents()
    if len(existing_docs) >= 2:
        return True, f"Database already contains {len(existing_docs)} documents."

    doc1_id = db.insert_document(
        filename="SFIA_8_AI_Data_Science_Standard.pdf",
        framework="SFIA 8 (Skills Framework for the Information Age)",
        file_size=1024 * 45
    )
    db.insert_chunks(doc1_id, SFIA_CHUNKS)

    doc2_id = db.insert_document(
        filename="ONET_28_Cloud_Cybersecurity_Framework.pdf",
        framework="O*NET 28.0 (Occupational Information Network)",
        file_size=1024 * 60
    )
    db.insert_chunks(doc2_id, ONET_CHUNKS)

    return True, "Successfully loaded official SFIA 8 and O*NET standards into SQLite."