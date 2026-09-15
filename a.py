import os
import sys
import uvicorn

if __name__ == "__main__":
    # Ensure current directory is in sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        
    print("=" * 65)
    print("   Professional Skill Definition RAG Prototype")
    print("   Authoritative Competency Engine (SFIA 8 & O*NET)")
    print("=" * 65)
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8000"))
    
    print(f" Starting Fullstack Server on http://{host}:{port}")
    print(f" - Login Page: http://localhost:{port}")
    print(" - Admin Dashboard & User RAG Assistant available")
    print(" - Persistent SQLite Database: data/skill_rag.db")
    print("=" * 65)
    
    uvicorn.run("backend.main:app", host=host, port=port, reload=False)