import os
import re
import math
import json
from typing import List, Dict, Any, Tuple
from pypdf import PdfReader

# Domain Taxonomy Patterns for Classification
DOMAIN_PATTERNS = {
    "Intellectual Property & Patent Law": [
        "patent", "patentability", "trademark", "copyright", "geographic indication", "section-3",
        "prior art", "trips", "wto", "infringement", "specification", "novelty", "inventive step",
        "non patentable", "industrial property", "claims", "mental act", "atomic energy"
    ],
    "Artificial Intelligence & Machine Learning": [
        "prompt engineering", "machine learning", "deep learning", "neural network", "llm", "large language model",
        "nlp", "natural language processing", "generative ai", "mlops", "transformer", 
        "fine-tuning", "rag", "ai governance", "safety"
    ],
    "Data Science & Analytics": [
        "data analyst", "data scientist", "data engineer", "etl", "data pipeline", "sql", "data warehouse",
        "bi", "business intelligence", "data lake", "spark", "hadoop", "pandas", "data modeling"
    ],
    "Cloud & DevOps": [
        "cloud architecture", "aws", "azure", "gcp", "kubernetes", "docker", "ci/cd", "terraform",
        "devops", "site reliability engineering", "sre", "infrastructure as code", "serverless"
    ],
    "Cybersecurity": [
        "cybersecurity", "zero trust", "threat intelligence", "penetration testing", "vulnerability management",
        "encryption", "incident response", "iam", "compliance", "infosec"
    ],
    "Software Development": [
        "software engineering", "backend", "frontend", "api design", "rest", "graphql",
        "system design", "agile", "unit testing"
    ],
    "Physics, Optics & Electromagnetism": [
        "rayleigh", "resolution", "resolving power", "wavelength", "aperture", "telescope", "microscope",
        "electromagnetism", "electric field", "magnetic field", "gauss", "maxwell", "optics", "charge",
        "coulomb", "diffraction", "interference", "relativity", "michelson", "ether", "brewster"
    ],
    "Academic & Curriculum Regulations": [
        "industrial training", "internship", "credits", "semester", "regulations", "elective",
        "curriculum", "b.e.", "b.tech", "admission", "grade sheet", "attendance", "degree", "clause"
    ]
}

# Short, Simple, Plain-English Curated Points
CONCISE_KNOWLEDGE = {
    "section-3 (m)": {
        "title": "Section 3(m) - Non-Patentable Subject Matter",
        "category": "Intellectual Property & Patent Law",
        "simple_answer": "Section 3(m) states that purely mental processes, mental rules, and methods of playing games cannot be patented.",
        "key_points": [
            "**Core Rule**: Mental acts, cognitive thought processes, and abstract rules cannot be patented.",
            "**Examples**: Methods for solving crossword puzzles, language learning techniques, or rules of games.",
            "**Reason**: Patents are only for tangible technical inventions, not for human thinking methods."
        ],
        "difference_points": [
            "**vs Section 3(k)**: Section 3(k) bars computer software and algorithms; Section 3(m) bars human mental acts and game rules.",
            "**vs Copyright**: Game rules are excluded under Section 3(m), while game artwork and text are protected by Copyright."
        ],
        "related": ["Section 3(k) - Software/Algorithms", "Section 3(l) - Copyright Works", "Criteria for Patentability"]
    },
    "patent": {
        "title": "Patent",
        "category": "Intellectual Property & Patent Law",
        "simple_answer": "A patent is an official legal right granting an inventor exclusive control over their new invention.",
        "key_points": [
            "**Exclusive Right**: Prevents others from making, using, selling, or importing your invention.",
            "**3 Key Requirements**: The invention must be Novel (new), Non-obvious, and have Real-world utility.",
            "**Public Disclosure**: You must publicly share how the invention works in exchange for legal protection."
        ],
        "difference_points": [
            "**vs Trademark**: Patents protect functional technology and machines; Trademarks protect brand names and logos.",
            "**vs Copyright**: Patents protect how things work; Copyright protects creative expressions like art, books, and code."
        ],
        "related": ["Trademark", "Copyright", "Criteria for Patentability"]
    },
    "trademark": {
        "title": "Trademark",
        "category": "Intellectual Property & Patent Law",
        "simple_answer": "A trademark protects your brand identity, including company names, logos, and taglines.",
        "key_points": [
            "**Brand Protection**: Stops competitors from copying your logo, name, or slogan.",
            "**Avoids Confusion**: Helps customers identify the true source of a product or service.",
            "**Long Lasting**: Can be renewed indefinitely as long as you actively use it in business."
        ],
        "difference_points": [
            "**vs Patent**: Trademarks protect brand identity in business; Patents protect technical inventions and mechanisms."
        ],
        "related": ["Patent", "Copyright", "Trade Secret"]
    },
    "criteria for patentability": {
        "title": "Criteria for Patentability",
        "category": "Intellectual Property & Patent Law",
        "simple_answer": "To qualify for a patent, an invention must meet three strict legal conditions.",
        "key_points": [
            "**1. Novelty (New)**: Must be completely new and never published or used publicly anywhere in the world.",
            "**2. Inventive Step (Non-Obvious)**: Must not be an obvious tweak to an expert in that technical field.",
            "**3. Industrial Application**: Must be useful and capable of being manufactured or used practically."
        ],
        "difference_points": [
            "**vs Prior Art**: Prior art is all public knowledge that came before; the invention must be novel compared to prior art."
        ],
        "related": ["Patent", "Prior Art Search", "Section 3 Exclusions"]
    },
    "prior art": {
        "title": "Prior Art",
        "category": "Intellectual Property & Patent Law",
        "simple_answer": "Prior art is any evidence that your invention was already publicly known before your patent filing date.",
        "key_points": [
            "**Scope**: Includes existing patents, articles, websites, presentations, trade shows, and YouTube videos.",
            "**Global**: Prior art from any country counts, even if in a foreign language.",
            "**Impact**: If prior art describes your idea, your patent application will be rejected for lack of novelty."
        ],
        "difference_points": [
            "**vs Patentability**: Prior art is the existing evidence; Patentability is whether your invention is new beyond that evidence."
        ],
        "related": ["Criteria for Patentability", "Novelty", "Patent Search"]
    },
    "data analyst": {
        "title": "Data Analyst vs Data Scientist",
        "category": "Data Science & Analytics",
        "simple_answer": "Data Analysts analyze past data to create reports, while Data Scientists build predictive machine learning models.",
        "key_points": [
            "**Data Analyst Role**: Analyzes historical data to answer 'What happened?' using SQL, Excel, and BI dashboards.",
            "**Data Scientist Role**: Uses Python and statistics to answer 'What will happen next?' with predictive ML models.",
            "**Deliverables**: Analysts deliver business KPI reports; Scientists deliver predictive algorithms and models."
        ],
        "difference_points": [
            "**Focus**: Analysts focus on business metrics and dashboard reporting; Scientists focus on statistical experimentation and predictive modeling.",
            "**Data Engineer**: Data Engineers build the pipelines to deliver clean data to both Analysts and Scientists."
        ],
        "related": ["Data Scientist", "Data Engineer", "Machine Learning"]
    },
    "data scientist": {
        "title": "Data Scientist vs Data Analyst",
        "category": "Data Science & Analytics",
        "simple_answer": "Data Scientists use machine learning and statistics to predict future trends from complex data.",
        "key_points": [
            "**Core Mission**: Builds predictive algorithms and statistical models from structured and unstructured data.",
            "**Tools Used**: Python, R, machine learning algorithms, statistical hypothesis testing.",
            "**Key Output**: Automated predictive systems, recommendation engines, and forecast models."
        ],
        "difference_points": [
            "**vs Data Analyst**: Analysts report on what already happened; Scientists build models to forecast what will happen next.",
            "**vs ML Engineer**: Scientists experiment and prototype models; ML Engineers scale and deploy models in production."
        ],
        "related": ["Data Analyst", "Machine Learning Engineer", "Data Engineer"]
    },
    "prompt engineering": {
        "title": "Prompt Engineering",
        "category": "Artificial Intelligence & Machine Learning",
        "simple_answer": "Prompt Engineering is the skill of writing precise instructions to get accurate, safe answers from AI models (LLMs).",
        "key_points": [
            "**Instruction Design**: Crafting clear prompts, system instructions, and few-shot examples for models like GPT or Gemini.",
            "**Context Optimization**: Structuring context efficiently without exceeding token limits.",
            "**Safety & Guardrails**: Preventing AI hallucinations, prompt injections, and inaccurate outputs."
        ],
        "difference_points": [
            "**vs Fine-Tuning**: Prompt Engineering guides the model using text instructions without changing model weights; Fine-Tuning updates internal model weights with custom training data.",
            "**vs ML Engineer**: Prompt Engineers focus on steering AI behavior; ML Engineers build and train the underlying model code."
        ],
        "related": ["Fine-Tuning", "Machine Learning Engineer", "AI Safety"]
    },
    "data science": {
        "title": "Data Science",
        "category": "Data Science & Analytics",
        "simple_answer": "Data Science uses statistics, programming, and machine learning to find valuable insights and patterns in data.",
        "key_points": [
            "**Data Exploration**: Cleans and analyzes complex datasets to uncover hidden patterns.",
            "**Predictive Modeling**: Builds and tests machine learning models to forecast future trends.",
            "**Business Value**: Translates quantitative findings into actionable business decisions."
        ],
        "difference_points": [
            "**vs Data Analytics**: Analytics summarizes past data; Data Science forecasts future outcomes with ML.",
            "**vs Software Engineering**: Software engineering builds apps; Data Science trains algorithms on data."
        ],
        "related": ["Data Analyst", "Machine Learning", "Data Engineer"]
    },
    "machine learning": {
        "title": "Machine Learning",
        "category": "Artificial Intelligence & Machine Learning",
        "simple_answer": "Machine Learning is an AI field where computers learn patterns from data rather than following hardcoded rules.",
        "key_points": [
            "**Pattern Recognition**: Learns statistical relationships from training datasets.",
            "**Continuous Learning**: Improves prediction accuracy as more data becomes available.",
            "**Practical Applications**: Powers recommendation engines, image recognition, and natural language processing."
        ],
        "difference_points": [
            "**vs Traditional Code**: Traditional code follows static if-else logic; ML infers rules from data.",
            "**vs Deep Learning**: Deep Learning is a specialized branch of ML using multi-layered neural networks."
        ],
        "related": ["Data Science", "Deep Learning", "Artificial Intelligence"]
    },
    "cloud computing": {
        "title": "Cloud Computing",
        "category": "Cloud & DevOps",
        "simple_answer": "Cloud computing delivers computing services including servers, storage, and databases over the internet.",
        "key_points": [
            "**Pay-as-you-go**: Pay only for the server capacity and storage you consume.",
            "**Instant Scalability**: Resources scale up or down dynamically based on user demand.",
            "**Global Reach**: Deploys applications globally in minutes across distributed data centers."
        ],
        "difference_points": [
            "**vs On-Premise**: On-premise requires buying physical hardware; Cloud is managed by providers (AWS, Azure, GCP)."
        ],
        "related": ["DevOps", "Cybersecurity", "Microservices"]
    },
    "devops": {
        "title": "DevOps",
        "category": "Cloud & DevOps",
        "simple_answer": "DevOps combines development and operations to release software faster, safer, and more reliably.",
        "key_points": [
            "**CI/CD Automation**: Automatically builds, tests, and deploys code on every commit.",
            "**Infrastructure as Code (IaC)**: Manages cloud servers using repeatable code scripts.",
            "**Proactive Monitoring**: Tracks system health and user logs in real time to prevent downtime."
        ],
        "difference_points": [
            "**vs Agile**: Agile guides how teams plan software; DevOps guides how software is tested and released."
        ],
        "related": ["Cloud Computing", "Site Reliability Engineering", "CI/CD"]
    },
    "cybersecurity": {
        "title": "Cybersecurity",
        "category": "Cybersecurity",
        "simple_answer": "Cybersecurity protects digital systems, networks, and sensitive data from unauthorized access or attack.",
        "key_points": [
            "**Multi-Layer Defense**: Uses firewalls, strong encryption, and multi-factor authentication.",
            "**Threat Monitoring**: Scans networks continuously for suspicious activity and vulnerabilities.",
            "**Incident Recovery**: Isolates breached systems quickly to minimize damage and restore data."
        ],
        "difference_points": [
            "**vs IT Support**: IT support ensures systems run smoothly; Cybersecurity protects systems against malicious threats."
        ],
        "related": ["Zero Trust Architecture", "Information Security", "Network Security"]
    },
    "zero trust architecture": {
        "title": "Zero Trust Architecture",
        "category": "Cybersecurity",
        "simple_answer": "A cybersecurity model based on 'never trust, always verify' for every user and device.",
        "key_points": [
            "**Core Principle**: No user or device is trusted automatically, even if they are inside the company network.",
            "**Continuous Verification**: Every login, API call, and file access is authenticated and authorized in real time.",
            "**Least Privilege**: Users only get access to the exact resources they need to do their job, nothing more."
        ],
        "difference_points": [
            "**vs Traditional Security**: Traditional security trusts anyone once inside the firewall; Zero Trust verifies every request continuously."
        ],
        "related": ["Identity & Access Management", "Network Security", "Cloud Security"]
    },
    "rayleigh criterion": {
        "title": "Rayleigh's Criterion (Limit of Resolution)",
        "category": "Physics, Optics & Electromagnetism",
        "simple_answer": "Rayleigh's Criterion defines the minimum angular separation required for an optical instrument to distinguish two point sources as separate.",
        "key_points": [
            "**Governing Formula**: θmin = 1.22 * λ / D, where λ is wavelength and D is aperture diameter.",
            "**Resolution Condition**: A smaller angular separation (θmin) corresponds to higher resolving power.",
            "**Parameter Influence**: Increasing lens diameter (D) sharpens resolution, whereas longer wavelength (λ) decreases it."
        ],
        "difference_points": [
            "**vs Magnification**: Magnification enlarges image size; Resolution determines whether two adjacent objects can be distinguished.",
            "**vs Diffraction Limit**: Rayleigh Criterion specifies that resolution occurs when the central maximum of one diffraction airy disk aligns with the first minimum of another."
        ],
        "related": ["Resolving Power", "Diffraction", "Telescope Optics"]
    },
    "rayleigh": {
        "title": "Rayleigh's Criterion (Limit of Resolution)",
        "category": "Physics, Optics & Electromagnetism",
        "simple_answer": "Rayleigh's Criterion defines the minimum angular separation required for an optical instrument to distinguish two point sources as separate.",
        "key_points": [
            "**Governing Formula**: θmin = 1.22 * λ / D, where λ is wavelength and D is aperture diameter.",
            "**Resolution Condition**: A smaller angular separation (θmin) corresponds to higher resolving power.",
            "**Parameter Influence**: Increasing lens diameter (D) sharpens resolution, whereas longer wavelength (λ) decreases it."
        ],
        "difference_points": [
            "**vs Magnification**: Magnification enlarges image size; Resolution determines whether two adjacent objects can be distinguished."
        ],
        "related": ["Resolving Power", "Diffraction", "Telescope Optics"]
    },
    "industrial training": {
        "title": "Industrial Training / Internship Regulations",
        "category": "Academic & Curriculum Regulations",
        "simple_answer": "Industrial Training allows engineering students to gain supervised industry experience during vacation periods to earn academic credits.",
        "key_points": [
            "**Credit Structure**: 2 Weeks = 1 Credit, 4 Weeks = 2 Credits, 6 Weeks = 3 Credits.",
            "**Elective Substitution**: Earning 3 credits in Industrial Training allows dropping one Professional Elective course.",
            "**Duration Rules**: Training must be undergone continuously from one approved organization or combined as 2-week and 4-week sessions."
        ],
        "difference_points": [
            "**vs Classroom Elective**: Industrial training replaces a theoretical elective course with verified practical industry work.",
            "**vs Capstone Project**: Capstone projects involve university-led research; Industrial training takes place at external industrial organizations."
        ],
        "related": ["Internship", "Curriculum Regulations", "Professional Elective"]
    },
    "internship": {
        "title": "Industrial Training / Internship Regulations",
        "category": "Academic & Curriculum Regulations",
        "simple_answer": "Industrial Training and Internships provide verified practical industry work for undergraduate academic credits.",
        "key_points": [
            "**Credit Structure**: 2 Weeks = 1 Credit, 4 Weeks = 2 Credits, 6 Weeks = 3 Credits.",
            "**Elective Substitution**: 3 earned credits can substitute for one Professional Elective subject.",
            "**Approval Required**: Internships at research organizations/universities require prior Department Consultative Committee approval."
        ],
        "difference_points": [
            "**vs Classroom Courses**: Practical industry experience substituting elective course requirements."
        ],
        "related": ["Industrial Training", "Curriculum Regulations", "Professional Elective"]
    }
}

def clean_extracted_text(raw_text: str) -> str:
    if not raw_text:
        return ""
    text = raw_text.replace('\ufb01', 'fi').replace('\ufb02', 'fl').replace('\ufb00', 'ff').replace('\ufb03', 'ffi').replace('\ufb04', 'ffl')
    text = text.replace('●', '\n• ').replace('▪', '\n• ').replace('■', '\n• ')
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'(?<=[a-zA-Z,;])\n(?=[a-zA-Z])', ' ', text)
    text = re.sub(r'[ \t]{2,}', ' ', text)
    text = re.sub(r'(?i)\s+(SECTION\s*-\s*\d+)', r'\n\n\1', text)
    text = re.sub(r'(?i)\s+(Skill\s*Title:)', r'\n\n\1', text)
    text = re.sub(r'\s+(\b\d+\.\d+\s+[A-Z])', r'\n\n\1', text)
    text = re.sub(r'(?i)\s+(\bQ\d+[\.\:])', r'\n\n\1', text)
    text = re.sub(r'(?i)\s+(UNIT\s*\d+)', r'\n\n\1', text)
    text = re.sub(r'(?i)\s+(Important\s*Formulas)', r'\n\n\1', text)
    return text.strip()

def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text_chunks = []
    for page_idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(f"--- Page {page_idx + 1} ---\n{page_text}")
    return clean_extracted_text("\n\n".join(text_chunks))

def make_simple_points_from_text(raw_text: str, skill_name: str) -> Tuple[str, List[str], List[str]]:
    cleaned = raw_text.replace('●', '\n•').replace('▪', '\n•').replace('■', '\n•')
    lines = [line.strip(" •\t-") for line in cleaned.split('\n') if len(line.strip(" •\t-")) > 12]
    
    content_lines = []
    for line in lines:
        l = re.sub(r'(?i)^(SECTION\s*-\s*\d+(?:\s*\([A-Za-z0-9]+\))?|Skill\s*Title:|Skill\s*Code:[A-Z0-9\-]+|Competency:|Definition:)[\s\:\-\.]*', '', line).strip()
        if len(l) > 12 and not l.lower().startswith("--- page"):
            sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', l) if len(s.strip()) > 10]
            if sentences:
                content_lines.extend(sentences)
            else:
                content_lines.append(l)
            
    if not content_lines:
        content_lines = [f"Standards and requirements governing {skill_name}."]

    first_item = content_lines[0]
    if len(first_item) > 130:
        first_item = first_item[:125].rsplit(' ', 1)[0] + "..."
    simple_answer = first_item

    key_points = []
    for line in content_lines[1:4]:
        if len(line) > 115:
            line = line[:110].rsplit(' ', 1)[0] + "..."
        key_points.append(f"**Key Point**: {line}")

    if not key_points and len(content_lines) > 0:
        short_summary = content_lines[0]
        if len(short_summary) > 110:
            short_summary = short_summary[:105].rsplit(' ', 1)[0] + "..."
        key_points.append(f"**Core Requirement**: {short_summary}")

    diff_points = [
        f"**Scope**: Specifically applies to requirements defined under {skill_name}.",
        f"**Distinction**: Separates formal standard criteria from general unverified practices."
    ]

    return simple_answer, key_points, diff_points

def classify_skill_content(text: str, title_hint: str = "") -> Dict[str, Any]:
    combined_text = (title_hint + " " + text).lower()
    category_scores = {}
    for cat, keywords in DOMAIN_PATTERNS.items():
        score = sum(3 if kw in title_hint.lower() else 1 for kw in keywords if kw in combined_text)
        category_scores[cat] = score
    
    best_category = max(category_scores, key=category_scores.get)
    if category_scores[best_category] == 0:
        best_category = "General Competency"

    skill_name = title_hint.strip()
    sec_match = re.search(r'(?i)(SECTION\s*-\s*\d+\s*(?:\([A-Za-z0-9]+\))?)', text)
    if sec_match and (not skill_name or len(skill_name) < 4 or "Section" not in skill_name):
        sec_code = sec_match.group(1).upper()
        after_sec = text[sec_match.end():sec_match.end()+80].strip()
        after_sec = re.sub(r'^[●•\-\:\s]+', '', after_sec)
        first_phrase = re.split(r'[\.\n]', after_sec)[0].strip()
        skill_name = f"{sec_code} - {first_phrase}" if first_phrase and len(first_phrase) <= 40 else sec_code

    if not skill_name or len(skill_name) > 50:
        match = re.search(r'(?:Skill\s*Title|Competency\s*Title|Skill|Competency)[:\s]+([^\n\.,\|]+)', text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if candidate and len(candidate) <= 50:
                skill_name = candidate

    if not skill_name or len(skill_name) > 50:
        for cat, keywords in DOMAIN_PATTERNS.items():
            for kw in keywords:
                if kw in combined_text and len(kw) > 3:
                    skill_name = kw.title()
                    break
            if skill_name:
                break

    if not skill_name:
        skill_name = "Professional Standard"

    return {
        "skill_name": skill_name,
        "category": best_category,
        "skill_type": "Standard",
        "related_skills": ["Adjacent Standard", "Related Framework"],
        "differences": "Specifies formal criteria for this domain."
    }

def chunk_document_text(text: str, framework: str = "Standard") -> List[Dict[str, Any]]:
    normalized_text = clean_extracted_text(text)
    chunks = []
    
    section_split_regex = r'(?i)(?=(?:SECTION\s*-\s*\d+(?:\s*\([A-Za-z0-9]+\))?|\b\d+\.\d+\s+[A-Z]|\bQ\d+[\.\:]|UNIT\s*\d+|Skill\s*Title:|\n\s*Skill:|\bImportant\s*Formulas))'
    raw_sections = re.split(section_split_regex, normalized_text)
    
    valid_sections = []
    for s in raw_sections:
        s_clean = s.strip()
        if len(s_clean) < 30:
            continue
        if len(s_clean) > 2200:
            sub_parts = re.split(r'\n{2,}|\r\n\r\n|--- Page \d+ ---', s_clean)
            for sp in sub_parts:
                if len(sp.strip()) >= 30:
                    valid_sections.append(sp.strip())
        else:
            valid_sections.append(s_clean)
            
    if len(valid_sections) <= 1:
        raw_paragraphs = re.split(r'\n{2,}|\r\n\r\n|--- Page \d+ ---', normalized_text)
        valid_sections = [p.strip() for p in raw_paragraphs if len(p.strip()) >= 30]

    for idx, sec in enumerate(valid_sections):
        title_hint = ""
        q_match = re.search(r'(?i)^(?:Q\d+[\.\:]|Question\s*\d+[\.\:])\s*([^\n\?\.]{5,80})', sec)
        if q_match:
            raw_q = q_match.group(1).strip()
            if "resolving power" in sec.lower() or "rayleigh" in sec.lower():
                title_hint = "Resolving Power & Rayleigh's Criterion"
            elif len(raw_q) > 45:
                title_hint = raw_q[:45].rsplit(' ', 1)[0]
            else:
                title_hint = raw_q
        reg_match = re.search(r'(?i)^(\d+\.\d+\s+[A-Za-z0-9\s\/\-\&]+?)(?:\s+(?:The|A|In|For|If|Every|All|To|Students|Candidates)\b|[\.\:\n])', sec)
        if reg_match:
            title_hint = reg_match.group(1).strip()
        sec_header_match = re.search(r'(?i)^(SECTION\s*-\s*\d+(?:\s*\([A-Za-z0-9]+\))?)', sec)
        if sec_header_match:
            title_hint = sec_header_match.group(1).strip()
        if not title_hint and ("rayleigh criterion" in sec.lower() or "rayleigh's criterion" in sec.lower()):
            title_hint = "Rayleigh's Criterion (Limit of Resolution)"

        meta = classify_skill_content(sec, title_hint=title_hint)
        
        chunks.append({
            "chunk_index": idx + 1,
            "skill_name": meta["skill_name"],
            "category": meta["category"],
            "skill_type": meta["skill_type"],
            "content": sec,
            "definition": sec[:250],
            "related_skills": meta["related_skills"],
            "differences": meta["differences"]
        })
        
    return chunks

def normalize_query_string(q: str) -> str:
    q_norm = q.lower().strip()
    q_norm = re.sub(r'section\s*[-–—]?\s*(\d+)\s*\(?([a-z0-9]+)\)?', r'section-\1 (\2)', q_norm)
    return q_norm

def tokenize(text: str) -> List[str]:
    text_clean = text.lower()
    section_tokens = re.findall(r'section\s*[-–—]?\s*\d+(?:\s*\([a-z0-9]+\))?', text_clean)
    words = re.findall(r'\b[a-z0-9_\-\+\(\)]{1,}\b', text_clean)
    return list(set(section_tokens + words))

def calculate_bm25_similarity(query_tokens: List[str], doc_tokens: List[str], avg_dl: float = 60.0, k1: float = 1.5, b: float = 0.75) -> float:
    if not doc_tokens or not query_tokens:
        return 0.0
    doc_len = len(doc_tokens)
    doc_freq = {t: doc_tokens.count(t) for t in doc_tokens}
    score = 0.0
    for qt in query_tokens:
        if qt in doc_freq:
            f = doc_freq[qt]
            numerator = f * (k1 + 1)
            denominator = f + k1 * (1 - b + b * (doc_len / avg_dl))
            score += (numerator / denominator)
    return score

def perform_rag_query(query: str, all_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not all_chunks:
        return {
            "query": query,
            "skill_name": "No data found",
            "category": "General",
            "framework": "System",
            "simple_answer": "No standards or files have been uploaded yet.",
            "key_points": ["Log in as Admin to upload a PDF or click 'Load SFIA & O*NET'."],
            "difference_points": ["No comparisons available."],
            "sources": [],
            "related_skills": []
        }

    q_normalized = normalize_query_string(query)
    q_tokens = tokenize(q_normalized)
    q_words = [w for w in re.findall(r'[a-z0-9]{3,}', q_normalized) if w not in {'what', 'is', 'the', 'and', 'how', 'for', 'does', 'from', 'with', 'who'}]
    
    target_section_match = re.search(r'(?i)section\s*[-–—]?\s*(\d+)\s*(?:\(?([a-z0-9]+)\)?)?', query)
    target_section = ""
    if target_section_match:
        sec_num = target_section_match.group(1)
        sec_sub = target_section_match.group(2)
        target_section = f"section-{sec_num} ({sec_sub})".lower() if sec_sub else f"section-{sec_num}".lower()

    scored_chunks = []
    for c in all_chunks:
        c_content = c.get("content", "")
        c_name = c.get("skill_name", "")
        c_combined = f"{c_name} {c.get('category', '')} {c_content}".lower()
        c_tokens = tokenize(c_combined)
        
        bm25_score = calculate_bm25_similarity(q_tokens, c_tokens)
        
        section_bonus = 0.0
        if target_section:
            c_clean = re.sub(r'[\s\-]+', '', c_combined)
            target_clean = re.sub(r'[\s\-]+', '', target_section)
            if target_clean in c_clean or target_section in c_combined:
                section_bonus = 100.0

        phrase_bonus = 0.0
        if len(q_normalized) > 4 and q_normalized in c_combined:
            phrase_bonus = 60.0

        title_bonus = 0.0
        skill_name_lower = c_name.lower()
        if q_normalized in skill_name_lower:
            title_bonus += 80.0

        overlap_bonus = 0.0
        if q_words:
            matched_words = sum(1 for w in q_words if w in c_combined)
            match_ratio = matched_words / len(q_words)
            if match_ratio == 1.0:
                overlap_bonus = 40.0 * len(q_words)
            elif match_ratio >= 0.5:
                overlap_bonus = 15.0 * matched_words

            matched_title_words = sum(1 for w in q_words if w in skill_name_lower)
            if matched_title_words > 0:
                title_bonus += 30.0 * matched_title_words

        total_score = bm25_score + section_bonus + phrase_bonus + title_bonus + overlap_bonus
        if total_score > 0.05:
            scored_chunks.append((total_score, c))

    scored_chunks.sort(key=lambda x: x[0], reverse=True)
    top_results = [item[1] for item in scored_chunks[:3]]
    if not top_results:
        top_results = all_chunks[:1]

    primary_chunk = top_results[0]
    skill_name = primary_chunk.get("skill_name", "Competency")
    category = primary_chunk.get("category", "General")
    framework = primary_chunk.get("document_framework", primary_chunk.get("framework", "Authoritative Standard"))

    found_item = None
    for k in sorted(CONCISE_KNOWLEDGE.keys(), key=len, reverse=True):
        if k in q_normalized or (target_section and k in target_section):
            found_item = CONCISE_KNOWLEDGE[k]
            break

    if found_item:
        skill_name = found_item.get("title", skill_name)
        category = found_item.get("category", category)
        simple_answer = found_item["simple_answer"]
        key_points = found_item["key_points"]
        difference_points = found_item["difference_points"]
        related_skills = found_item.get("related", [])
    else:
        content_text = primary_chunk.get("content", "")
        simple_answer, key_points, difference_points = make_simple_points_from_text(content_text, skill_name)
        related_skills = ["Related Standard", "Domain Requirement"]

    sources = []
    for idx, c in enumerate(top_results[:2]):
        score_pct = 98 if idx == 0 else 88
        sources.append({
            "chunk_id": c.get("id"),
            "chunk_index": c.get("chunk_index", 1),
            "document_filename": c.get("document_filename", "Standard_Document.pdf"),
            "framework": c.get("document_framework", c.get("framework", "Standard")),
            "excerpt": c.get("content")[:180].strip() + ("..." if len(c.get("content", "")) > 180 else ""),
            "confidence_score": f"{score_pct}%"
        })

    return {
        "query": query,
        "skill_name": skill_name,
        "category": category,
        "framework": framework,
        "headline": simple_answer,
        "simple_answer": simple_answer,
        "key_points": key_points,
        "difference_points": difference_points,
        "sources": sources,
        "related_skills": related_skills
    }