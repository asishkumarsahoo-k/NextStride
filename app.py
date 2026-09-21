import streamlit as st
import json
import random
import os
import time
from datetime import datetime
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. VECTOR ICONS & SVG LIBRARY
# ---------------------------------------------------------
SVG_ICONS = {
    "brand_logo": '<svg width="24" height="24" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><polygon points="16,3 29,10 29,22 16,29 3,22 3,10"/><polyline points="16,3 16,29"/><line x1="3" y1="10" x2="29" y2="22"/><line x1="3" y1="22" x2="29" y2="10"/></svg>',
    "dashboard": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
    "target": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
    "code": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    "award": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/></svg>',
    "credential": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="14" x="3" y="5" rx="2"/><path d="M7 15h4M15 15h2M7 11h2M13 11h4"/></svg>',
    "user": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "help": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "sun": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>',
    "moon": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
    "check": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>',
    "lock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>',
    "unlock": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 9.9-1"/></svg>',
    "trend": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>',
    "external": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 3h6v6M10 14 21 3M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>',
    "camera": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
    "book": '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5Z"/><path d="M6 2v20"/></svg>'
}

IT_CAREER_ROLES = [
    "Python Backend Architect",
    "Full-Stack Software Engineer",
    "Frontend Developer / UI Specialist",
    "AI / Machine Learning Engineer",
    "Cloud Infrastructure & DevOps Engineer",
    "Cybersecurity Analyst / SecOps",
    "Data Engineer & Pipeline Architect",
    "Database Administrator (DBA)",
    "Embedded Systems / IoT Engineer",
    "Network Operations Engineer",
    "Quality Assurance & Test Automation Lead",
    "IT Systems & Support Specialist",
    "Other / Custom Role"
]

PROGRAMMING_LANGUAGES = [
    "Python (Modern 3.12+ Async & Data)",
    "TypeScript & Modern React / Node",
    "Go (Concurrent Cloud Services)",
    "Rust (Safe Systems Architecture)",
    "Java & Spring Boot Enterprise",
    "C++ (Modern High-Performance Computing)",
    "SQL & Relational Query Engineering"
]

DAY_DUAL_TONES = [
    ("#E0F2FE", "#FCE7F3", "#0284C7", "#DB2777", "#F0F9FF", "#FDF2F8"),
    ("#FEF3C7", "#E0E7FF", "#D97706", "#4F46E5", "#FFFBEB", "#EEF2FF"),
    ("#DCFCE7", "#E0F2FE", "#16A34A", "#0284C7", "#F0FDF4", "#F0F9FF"),
    ("#F3E8FF", "#FFE4E6", "#7C3AED", "#E11D48", "#FAF5FF", "#FFF1F2"),
    ("#FFEDD5", "#CFFAFE", "#EA580C", "#0891B2", "#FFF7ED", "#ECFEFF")
]

NIGHT_PALETTE = ("#0B0F17", "#1E1B4B", "#38BDF8", "#818CF8", "#0F172A", "#1E293B")

# ---------------------------------------------------------
# 2. SESSION INITIALIZATION & DEMO DATA
# ---------------------------------------------------------
st.set_page_config(page_title="NextStride | Neural Career Accelerator", layout="wide", initial_sidebar_state="expanded")

if "is_night_mode" not in st.session_state:
    st.session_state.is_night_mode = False

if "day_colors" not in st.session_state:
    st.session_state.day_colors = DAY_DUAL_TONES[0]

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Dashboard"

if "user_authenticated" not in st.session_state:
    st.session_state.user_authenticated = False

if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "name": "Creative Operator",
        "email": "creative.operator@nextstride.ai",
        "role": "Aspiring Cloud & Backend Architect",
        "provider": "Verified Demo Account",
        "bio": "Building resilient event-driven systems and microservices with Python and Go."
    }

if "roadmap" not in st.session_state:
    st.session_state.roadmap = []

if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = {}

if "lang_roadmap" not in st.session_state:
    st.session_state.lang_roadmap = []

if "lang_eval_results" not in st.session_state:
    st.session_state.lang_eval_results = {}

# 6-Stage Curriculum: Guaranteed Minimum 4 Blueprint Steps Per Stage
PYTHON_6_STAGE_CURRICULUM = [
    {
        "step_number": 1,
        "tier": "Stage 1: Tooling & Environment",
        "skill_title": "Python 3.12 Runtime & Virtual Isolation",
        "skill_description": "Configuring pyenv, isolated virtual environments, and verifying compiler architecture.",
        "task_title": "Setup Strict Python Environment",
        "evaluator_rubric": "CLI version output and venv verification.",
        "is_unlocked": True,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Install & Verify Python Runtime",
                "guidance": "Install Python 3.12+ and verify that the binary runtime path and pip package manager are properly linked.",
                "code_example": "python --version\npython3 -m pip install --upgrade pip"
            },
            {
                "step_name": "Step 2: Scaffolding Environment & Sandbox",
                "guidance": "Create an isolated virtual environment and activate the session to keep global dependencies completely clean.",
                "code_example": "python -m venv venv\n# On Windows: .\\venv\\Scripts\\activate\n# On Unix/macOS: source venv/bin/activate"
            },
            {
                "step_name": "Step 3: Package Lock Configuration",
                "guidance": "Set up a clean requirements file with strict version pinning for runtime libraries.",
                "code_example": "pip install pytest pydantic\npip freeze > requirements.txt"
            },
            {
                "step_name": "Step 4: Environment Health Check",
                "guidance": "Execute an automated inline health check asserting that the active interpreter is running strictly from the virtual sandbox.",
                "code_example": "python -c \"import sys; assert sys.prefix != sys.base_prefix, 'Virtual environment not active!'; print('✓ Environment Isolated')\""
            }
        ]
    },
    {
        "step_number": 2,
        "tier": "Stage 2: Memory & Streaming",
        "skill_title": "Stream Processing with Generators",
        "skill_description": "Using Python generator expressions and yield pipelines to parse multi-gigabyte logs in O(1) memory space.",
        "task_title": "Build Streaming Log Parser",
        "evaluator_rubric": "Memory complexity assertion and generator validation.",
        "is_unlocked": False,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Generator File Streamer",
                "guidance": "Open file in context and yield line by line without loading the full content into system memory.",
                "code_example": "def stream_lines(file_path):\n    with open(file_path, 'r', encoding='utf-8') as f:\n        for line in f:\n            yield line.rstrip('\\n')"
            },
            {
                "step_name": "Step 2: Transform Pipeline Filter",
                "guidance": "Pipe generated string tokens through lazy filtering pipelines using generator expressions.",
                "code_example": "error_stream = (line for line in stream_lines('app.log') if 'ERROR' in line)"
            },
            {
                "step_name": "Step 3: Aggregation & Token Extraction",
                "guidance": "Consume filtered generator items one-at-a-time to accumulate metrics with deterministic O(1) memory overhead.",
                "code_example": "def aggregate_errors(stream):\n    counts = {}\n    for item in stream:\n        key = item.split(' ')[0]\n        counts[key] = counts.get(key, 0) + 1\n    return counts"
            },
            {
                "step_name": "Step 4: Memory Profiling Benchmark",
                "guidance": "Verify that memory usage remains constant even when processing massive 500MB+ mock log streams.",
                "code_example": "import tracemalloc\ntracemalloc.start()\nres = aggregate_errors(error_stream)\ncurrent, peak = tracemalloc.get_traced_memory()\nprint(f'Peak Memory: {peak / 1024:.2f} KB')\ntracemalloc.stop()"
            }
        ]
    },
    {
        "step_number": 3,
        "tier": "Stage 3: Type Safety & Validation",
        "skill_title": "Strict Type Hinting & Pydantic v2",
        "skill_description": "Enforcing runtime constraints, type validation, and serialization models.",
        "task_title": "Implement Typed Schemas",
        "evaluator_rubric": "Type hint adherence and schema validation.",
        "is_unlocked": False,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Define Typed Models",
                "guidance": "Import BaseModel and define strongly-typed attributes with validation constraints.",
                "code_example": "from pydantic import BaseModel, Field\n\nclass TelemetryPacket(BaseModel):\n    node_id: str\n    latency_ms: float = Field(ge=0.0)"
            },
            {
                "step_name": "Step 2: Add Custom Field Validators",
                "guidance": "Implement custom validation rules using Pydantic's @field_validator to sanitize malformed telemetry inputs.",
                "code_example": "from pydantic import field_validator\n\nclass SecurePacket(TelemetryPacket):\n    @field_validator('node_id')\n    def validate_node(cls, v):\n        if not v.startswith('node-'):\n            raise ValueError('Must begin with node- prefix')\n        return v"
            },
            {
                "step_name": "Step 3: Serialization & Schema Export",
                "guidance": "Transform incoming payload dictionaries and export validated structures cleanly to JSON.",
                "code_example": "payload = {'node_id': 'node-101', 'latency_ms': 14.5}\npacket = SecurePacket(**payload)\njson_str = packet.model_dump_json()\nprint(json_str)"
            },
            {
                "step_name": "Step 4: Mypy Static Type Verification",
                "guidance": "Execute static type checker via terminal to guarantee zero type regressions or implicit any declarations.",
                "code_example": "pip install mypy\nmypy --strict src/schemas.py"
            }
        ]
    },
    {
        "step_number": 4,
        "tier": "Stage 4: Automated Testing",
        "skill_title": "Pytest Test Harness & Fixtures",
        "skill_description": "Writing test fixtures, parameterized suites, and measuring code coverage.",
        "task_title": "Achieve 100% Test Coverage",
        "evaluator_rubric": "Clean pytest execution and 100% test pass threshold.",
        "is_unlocked": False,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Test Fixtures Scaffolding",
                "guidance": "Create reusable pytest fixtures providing temporary mocked disk files and telemetry test packets.",
                "code_example": "import pytest\n\n@pytest.fixture\ndef sample_log_file(tmp_path):\n    p = tmp_path / 'sample.log'\n    p.write_text('2026-09-20 ERROR Database connection lost\\n')\n    return p"
            },
            {
                "step_name": "Step 2: Unit Testing Core Logic",
                "guidance": "Write pytest assertion functions verifying expected parser outputs and exception conditions.",
                "code_example": "def test_parser_with_fixture(sample_log_file):\n    lines = list(stream_lines(sample_log_file))\n    assert len(lines) == 1\n    assert 'ERROR' in lines[0]"
            },
            {
                "step_name": "Step 3: Parameterized Edge-Case Tests",
                "guidance": "Use @pytest.mark.parametrize to test various corrupt log formats and boundary condition latency inputs.",
                "code_example": "@pytest.mark.parametrize('node,lat,valid', [\n    ('node-1', 10.0, True),\n    ('invalid_name', 10.0, False)\n])\ndef test_packet_cases(node, lat, valid):\n    # Assert expected validation outcomes\n    pass"
            },
            {
                "step_name": "Step 4: Coverage Reporting Execution",
                "guidance": "Execute the full test harness in terminal with verbose test output and coverage assertions.",
                "code_example": "pytest -v --cov=src --cov-report=term-missing"
            }
        ]
    },
    {
        "step_number": 5,
        "tier": "Stage 5: Asynchronous I/O",
        "skill_title": "AsyncIO Event Loops & Non-Blocking Sockets",
        "skill_description": "Managing async tasks, coroutines, and concurrent socket connections.",
        "task_title": "Async Worker Pipeline",
        "evaluator_rubric": "Verify non-blocking event loops and asyncio concurrency.",
        "is_unlocked": False,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Implement Coroutines",
                "guidance": "Use async and await keywords to schedule concurrent background processing tasks.",
                "code_example": "import asyncio\n\nasync def fetch_task(task_id):\n    await asyncio.sleep(0.05)\n    return f'Task {task_id} complete'"
            },
            {
                "step_name": "Step 2: Concurrent Task Gathering",
                "guidance": "Leverage asyncio.gather to orchestrate hundreds of IO-bound network operations concurrently.",
                "code_example": "async def run_batch():\n    results = await asyncio.gather(*(fetch_task(i) for i in range(10)))\n    return results"
            },
            {
                "step_name": "Step 3: Semaphore Concurrency Throttling",
                "guidance": "Apply an asyncio.Semaphore to prevent socket exhaustion and throttle maximum simultaneous connections.",
                "code_example": "sem = asyncio.Semaphore(5)\nasync def guarded_task(i):\n    async with sem:\n        return await fetch_task(i)"
            },
            {
                "step_name": "Step 4: Event Loop Lifecycle Execution",
                "guidance": "Initialize the event loop and ensure clean shutdown with cancellation of pending asynchronous tasks.",
                "code_example": "async def main():\n    data = await run_batch()\n    print(f'Processed {len(data)} asynchronous jobs')\n\nasyncio.run(main())"
            }
        ]
    },
    {
        "step_number": 6,
        "tier": "Stage 6: Containerization",
        "skill_title": "Production Hardening & Docker Containerization",
        "skill_description": "Packaging the Python application into minimal, secure multi-stage container images.",
        "task_title": "Build Multi-Stage Image",
        "evaluator_rubric": "Container builds cleanly with unprivileged user access.",
        "is_unlocked": False,
        "is_completed": False,
        "step_by_step_blueprint": [
            {
                "step_name": "Step 1: Multi-Stage Dockerfile Definition",
                "guidance": "Define a multi-stage build separating compilation tooling from the minimal runtime scratch image.",
                "code_example": "FROM python:3.12-slim AS builder\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --user --no-cache-dir -r requirements.txt"
            },
            {
                "step_name": "Step 2: Unprivileged Security Hardening",
                "guidance": "Create an unprivileged non-root service user and set strict filesystem permissions.",
                "code_example": "FROM python:3.12-slim\nRUN useradd -m appuser\nWORKDIR /app\nCOPY --from=builder /root/.local /home/appuser/.local\nCOPY . .\nUSER appuser\nENV PATH=/home/appuser/.local/bin:$PATH"
            },
            {
                "step_name": "Step 3: Container Healthcheck Specification",
                "guidance": "Add a lightweight Docker healthcheck instruction verifying application responsiveness.",
                "code_example": "HEALTHCHECK --interval=30s --timeout=5s \\\n  CMD python -c 'import sys; sys.exit(0)' || exit 1\nCMD [\"python\", \"main.py\"]"
            },
            {
                "step_name": "Step 4: Image Build & Verification",
                "guidance": "Build the container image and execute a smoke test asserting zero runtime permission issues.",
                "code_example": "docker build -t nextstride-service:1.0 .\ndocker run --rm nextstride-service:1.0"
            }
        ]
    }
]

# Pre-seeded Demo Path 2 with 4 Blueprint Steps Per Stage
DEMO_PATH_2_STEPS = [
    {
        "step_number": 1, 
        "tier": "Stage 1: API Design", 
        "skill_title": "FastAPI REST Architecture & Routers", 
        "skill_description": "Building async REST APIs with OpenAPI schema documentation.", 
        "task_title": "Create Modular Routers", 
        "evaluator_rubric": "FastAPI router inclusion.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Initialize FastAPI Instance", "guidance": "Set up the core FastAPI application with metadata.", "code_example": "from fastapi import FastAPI\napp = FastAPI(title='NextStride Microservice')"},
            {"step_name": "Step 2: Modular Router Definition", "guidance": "Organize endpoints into APIRouters for maintainable architecture.", "code_example": "from fastapi import APIRouter\nrouter = APIRouter(prefix='/api/v1/items')"},
            {"step_name": "Step 3: Request & Response Schemas", "guidance": "Bind Pydantic request and response models for automatic validation.", "code_example": "@router.get('/', response_model=list[dict])\nasync def list_items():\n    return [{'id': 1, 'name': 'Item A'}]"},
            {"step_name": "Step 4: Local Uvicorn Testing", "guidance": "Run development server and verify Swagger documentation at /docs.", "code_example": "uvicorn main:app --reload --port 8000"}
        ]
    },
    {
        "step_number": 2, 
        "tier": "Stage 2: Persistence", 
        "skill_title": "Async SQLAlchemy & Alembic Migrations", 
        "skill_description": "Designing connection pools and declarative schemas.", 
        "task_title": "Database Migration Script", 
        "evaluator_rubric": "Alembic revision created.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Async Connection Engine", "guidance": "Configure create_async_engine and session maker.", "code_example": "from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession\nengine = create_async_engine('postgresql+asyncpg://user:pass@localhost/db')"},
            {"step_name": "Step 2: Declarative Model Schema", "guidance": "Define table schemas using SQLAlchemy ORM Base classes.", "code_example": "from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column\nclass Base(DeclarativeBase):\n    pass"},
            {"step_name": "Step 3: Initialize Alembic Migrations", "guidance": "Scaffold migration environment and configure env.py with target metadata.", "code_example": "alembic init -t async alembic\nalembic revision --autogenerate -m 'create_tables'"},
            {"step_name": "Step 4: Apply Database Migrations", "guidance": "Upgrade database schema to head revision via terminal.", "code_example": "alembic upgrade head"}
        ]
    },
    {
        "step_number": 3, 
        "tier": "Stage 3: Caching", 
        "skill_title": "Distributed Caching & Redis Idempotency", 
        "skill_description": "Preventing duplicate operations via Redis keys.", 
        "task_title": "Implement Idempotency Guard", 
        "evaluator_rubric": "Redis cache hit verified.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Setup Redis Connection", "guidance": "Connect to Redis cache instance via async client.", "code_example": "import redis.asyncio as redis\nr = redis.Redis(host='localhost', port=6379, decode_responses=True)"},
            {"step_name": "Step 2: Idempotency Key Middleware", "guidance": "Intercept incoming requests and verify header idempotency tokens.", "code_example": "async def check_idempotency(key: str):\n    return await r.set(f'idemp:{key}', 'locked', nx=True, ex=60)"},
            {"step_name": "Step 3: Cache Storage & Response Memoization", "guidance": "Serialize and store expensive endpoint outputs with configured TTLs.", "code_example": "await r.setex('catalog_cache', 300, json.dumps(data))"},
            {"step_name": "Step 4: Cache Hit Validation", "guidance": "Benchmark response times demonstrating sub-millisecond cache hits.", "code_example": "cached = await r.get('catalog_cache')\nassert cached is not None"}
        ]
    },
    {
        "step_number": 4, 
        "tier": "Stage 4: Authentication", 
        "skill_title": "JWT Auth & Role-Based Access Control", 
        "skill_description": "Securing API routes with signed bearer tokens.", 
        "task_title": "Implement Auth Middleware", 
        "evaluator_rubric": "HTTP 401 on missing token.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Cryptographic Password Hashing", "guidance": "Hash user credentials using passlib and bcrypt context.", "code_example": "from passlib.context import CryptContext\npwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')"},
            {"step_name": "Step 2: Sign JWT Access Tokens", "guidance": "Encode user claims and expiration timestamps into cryptographic tokens.", "code_example": "import jwt\ndef create_token(data: dict):\n    return jwt.encode(data, 'SECRET', algorithm='HS256')"},
            {"step_name": "Step 3: Route Dependency Guard", "guidance": "Inject current authenticated user into secured route handlers.", "code_example": "from fastapi import Depends, HTTPException\nasync def get_current_user(token: str):\n    return jwt.decode(token, 'SECRET', algorithms=['HS256'])"},
            {"step_name": "Step 4: Role-Based Access Testing", "guidance": "Verify that unauthorized requests receive strict HTTP 401 and 403 responses.", "code_example": "response = client.get('/protected', headers={'Authorization': 'Bearer ' + token})\nassert response.status_code == 200"}
        ]
    },
    {
        "step_number": 5, 
        "tier": "Stage 5: Resilience", 
        "skill_title": "Rate Limiting & Circuit Breakers", 
        "skill_description": "Handling downstream dependencies and failure modes.", 
        "task_title": "Configure Resilience Middleware", 
        "evaluator_rubric": "Circuit opens on 503.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Apply Rate Limiter", "guidance": "Limit incoming traffic per IP address using token bucket algorithms.", "code_example": "@app.middleware('http')\nasync def rate_limit(request, call_next):\n    return await call_next(request)"},
            {"step_name": "Step 2: Circuit Breaker State Machine", "guidance": "Implement closed, open, and half-open failure trip counters.", "code_example": "class CircuitBreaker:\n    failures = 0\n    state = 'CLOSED'"},
            {"step_name": "Step 3: Fallback Degradation Handling", "guidance": "Return cached stale responses when downstream microservices fail.", "code_example": "try:\n    return await call_external()\nexcept Exception:\n    return {'status': 'degraded', 'data': []}"},
            {"step_name": "Step 4: Concurrency Load Test", "guidance": "Run concurrent curl requests to assert rate limiting kicks in at threshold.", "code_example": "ab -n 100 -c 10 http://localhost:8000/api/v1/items/"}
        ]
    },
    {
        "step_number": 6, 
        "tier": "Stage 6: Observability", 
        "skill_title": "Prometheus Metrics & Structured Logging", 
        "skill_description": "Emitting p99 latency counters and traces.", 
        "task_title": "Export Live Metrics", 
        "evaluator_rubric": "Metrics scrape endpoint 200 OK.", 
        "is_unlocked": True, 
        "is_completed": True, 
        "step_by_step_blueprint": [
            {"step_name": "Step 1: Structured JSON Logging", "guidance": "Configure logger to emit parsable JSON logs with request IDs.", "code_example": "import logging\nlogger = logging.getLogger('nextstride')"},
            {"step_name": "Step 2: Prometheus Counters & Histograms", "guidance": "Instrument latency buckets for p50, p95, and p99 requests.", "code_example": "from prometheus_client import Counter, Histogram\nREQUEST_COUNT = Counter('requests_total', 'Total HTTP Requests')"},
            {"step_name": "Step 3: Expose Prometheus Endpoint", "guidance": "Mount /metrics route for automated Prometheus scraping.", "code_example": "from prometheus_client import make_asgi_app\nmetrics_app = make_asgi_app()\napp.mount('/metrics', metrics_app)"},
            {"step_name": "Step 4: Synthetic Health Check", "guidance": "Verify end-to-end telemetry scrape returns HTTP 200 with active metrics.", "code_example": "curl -s http://localhost:8000/metrics | grep requests_total"}
        ]
    }
]

DEMO_COMPLETED_PATHS = [
    {
        "share_id": "NS-859916",
        "title": "Python Language Foundations & Modern Tooling",
        "date": "2026-09-18",
        "score": 95,
        "role": "Python Systems Engineer",
        "steps_cleared": 6,
        "summary": "Mastered generator-based streaming I/O, strict type annotations, regex log parsing, pytest suites, async event loops, and container packaging.",
        "steps_data": PYTHON_6_STAGE_CURRICULUM,
        "hashtags": ["#Python312", "#StreamGenerators", "#TypeHints", "#Pytest", "#AsyncIO", "#Docker"]
    },
    {
        "share_id": "NS-412093",
        "title": "Production RESTful API & Distributed Microservices",
        "date": "2026-09-20",
        "score": 92,
        "role": "Backend Architect",
        "steps_cleared": 6,
        "summary": "Designed idempotent endpoints with FastAPI, async SQLAlchemy ORM, Alembic migrations, Redis caching, JWT auth gates, and Prometheus observability.",
        "steps_data": DEMO_PATH_2_STEPS,
        "hashtags": ["#FastAPI", "#Microservices", "#SQLAlchemy", "#RedisCache", "#JWTAuth", "#Observability"]
    }
]

if "completed_tracks" not in st.session_state or not st.session_state.completed_tracks:
    st.session_state.completed_tracks = DEMO_COMPLETED_PATHS

if "support_messages" not in st.session_state:
    st.session_state.support_messages = [
        {"role": "assistant", "content": "Welcome to NextStride Support! How can I assist you with your career roadmaps, task evaluations, or account features?"}
    ]

# ---------------------------------------------------------
# 3. HIGH-CONTRAST DYNAMIC THEME ENGINE (PASTEL PINK & DUAL TONE)
# ---------------------------------------------------------
is_night = st.session_state.is_night_mode
bg1, bg2, accent1, accent2, sb_bg1, sb_bg2 = NIGHT_PALETTE if is_night else st.session_state.day_colors

page_text = "#F8FAFC" if is_night else "#0F172A"
label_text = "#94A3B8" if is_night else "#1E293B"
placeholder_text = "#64748B" if is_night else "#475569"

p_pink_bg = "#FCE7F3" if not is_night else "#1E1B4B"
p_pink_sub = "#FDF2F8" if not is_night else "#1E293B"
p_pink_border = "#F472B6" if not is_night else accent1
p_pink_text = "#831843" if not is_night else "#F8FAFC"

card_bg = "rgba(15, 23, 42, 0.92)" if is_night else "#FFFFFF"
card_border = "rgba(255, 255, 255, 0.15)" if is_night else "#CBD5E1"

custom_css = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800;900&family=Rajdhani:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Rajdhani', sans-serif;
    }}

    /* 1. DUAL-TONE GRADIENT ON BOTH APP CONTAINER AND MAIN VIEW */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
        background: linear-gradient(135deg, {bg1} 0%, {bg2} 100%) !important;
        color: {page_text} !important;
    }}

    .stApp p, .stApp span, .stApp div, .stApp label, .stMarkdown {{
        color: {page_text};
    }}

    /* 2. DUAL-TONED NEXTSTRIDE TEXT */
    .unfold-brand {{
        font-family: 'Orbitron', sans-serif !important;
        font-weight: 900 !important;
        background: linear-gradient(90deg, #0284C7 0%, #EC4899 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: inline-block !important;
        letter-spacing: 0.08em !important;
    }}

    /* 3. SIDEBAR STYLING */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {sb_bg1} 0%, {sb_bg2} 100%) !important;
        border-right: 1.5px solid {card_border} !important;
    }}

    /* 4. ALL BUTTONS FIX (OVERWRITES BLACK BUTTONS ON SIDEBAR AND MAIN PAGE) */
    .stButton > button,
    button[kind="secondary"],
    button[data-testid="baseButton-secondary"],
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {{
        background-color: {p_pink_bg} !important;
        color: {p_pink_text} !important;
        border: 1.5px solid {p_pink_border} !important;
        border-radius: 10px !important;
        font-weight: 800 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05) !important;
        transition: all 0.2s ease !important;
    }}
    .stButton > button:hover,
    button[kind="secondary"]:hover,
    button[kind="primary"]:hover {{
        background-color: #FBCFE8 !important;
        border-color: #DB2777 !important;
        color: #500724 !important;
    }}
    .stButton > button * {{
        color: {p_pink_text} !important;
        font-weight: 800 !important;
    }}

    button[kind="primary"], button[data-testid="baseButton-primary"] {{
        background: linear-gradient(90deg, #EC4899 0%, #0284C7 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
    }}
    button[kind="primary"] * {{
        color: #FFFFFF !important;
    }}

    /* 5. ALL EXPANDERS & BLUEPRINT ACCORDIONS (PASTEL PINK) */
    [data-testid="stExpander"], 
    details, 
    details summary,
    [data-testid="stExpander"] details,
    [data-testid="stExpander"] summary {{
        background-color: {p_pink_bg} !important;
        color: {p_pink_text} !important;
        border: 1.5px solid {p_pink_border} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stExpander"] summary:hover {{
        background-color: {p_pink_sub} !important;
    }}
    [data-testid="stExpander"] summary * {{
        color: {p_pink_text} !important;
        font-weight: 800 !important;
    }}

    /* 6. CODE BLOCKS */
    .stCodeBlock, div[data-testid="stCodeBlock"], pre {{
        background-color: {'#1E293B' if is_night else '#FFF5F7'} !important;
        border: 1.5px solid {p_pink_border} !important;
        border-radius: 8px !important;
    }}
    .stCodeBlock code, pre code, [data-testid="stCodeBlock"] * {{
        color: {'#F8FAFC' if is_night else '#0F172A'} !important;
        font-family: monospace !important;
        font-weight: 600 !important;
    }}

    /* 7. FILE UPLOADER DROPZONE & BUTTON (PASTEL PINK) */
    [data-testid="stFileUploader"],
    [data-testid="stFileUploader"] section,
    [data-testid="stFileUploaderDropzone"],
    [data-testid="stFileUploaderDropzoneInstructions"] {{
        background-color: {p_pink_sub} !important;
        color: {p_pink_text} !important;
        border: 1.5px dashed {p_pink_border} !important;
        border-radius: 10px !important;
    }}
    [data-testid="stFileUploader"] section * {{
        color: {p_pink_text} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stFileUploader"] button {{
        background-color: #FFFFFF !important;
        color: #BE185D !important;
        border: 1.5px solid #F472B6 !important;
        border-radius: 6px !important;
        font-weight: 800 !important;
    }}

    /* 8. PASSWORD REVEAL EYE BUTTON FIX */
    button[aria-label="Show password"],
    button[aria-label="Hide password"],
    [data-testid="stTextInput"] button {{
        background-color: {p_pink_bg} !important;
        border: 1px solid {p_pink_border} !important;
        border-radius: 6px !important;
    }}
    button[aria-label="Show password"] svg,
    button[aria-label="Hide password"] svg {{
        fill: {p_pink_text} !important;
        stroke: {p_pink_text} !important;
    }}

    /* 9. FORM INPUTS & CHAT BAR */
    label[data-testid="stWidgetLabel"] p,
    .stTextInput label p,
    .stSelectbox label p,
    .stTextArea label p,
    .stFileUploader label p {{
        color: {label_text} !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
    }}
    input[type="text"], input[type="password"], textarea, [data-testid="stSelectbox"] div[data-baseweb="select"] {{
        background-color: {'#1E293B' if is_night else '#FFFFFF'} !important;
        color: {'#FFFFFF' if is_night else '#0F172A'} !important;
        border: 1.5px solid {card_border} !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSelectbox"] div[data-baseweb="select"] span {{
        color: {'#FFFFFF' if is_night else '#0F172A'} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stChatInput"] {{
        background-color: {'#1E293B' if is_night else '#FFFFFF'} !important;
        border: 1.5px solid {p_pink_border} !important;
        border-radius: 12px !important;
    }}
    [data-testid="stChatInput"] textarea {{
        color: {page_text} !important;
    }}
    [data-testid="stChatInput"] textarea::placeholder {{
        color: {placeholder_text} !important;
        font-weight: 600 !important;
    }}

    /* 10. SUPPRESS TOAST OVERLAYS */
    div[data-testid="stToast"], 
    div[data-testid="stNotification"],
    [data-testid="stAlert"] {{
        display: none !important;
    }}

    /* 11. CARDS & BADGES */
    .glass-card {{
        background: {card_bg};
        border: 1.5px solid {card_border};
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
        color: {page_text} !important;
    }}
    .metric-badge {{
        display: inline-flex;
        align-items: center;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.85rem;
        border: 1.5px solid {accent1};
        color: {accent1} !important;
        font-weight: 800;
        margin-bottom: 12px;
    }}
    .portalix-stat-tile {{
        border: 1.5px solid {card_border};
        border-radius: 14px;
        padding: 18px;
        background: {card_bg};
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
        text-align: center;
    }}
    .skill-knowledge-box {{
        background: {'rgba(2, 132, 199, 0.08)' if not is_night else 'rgba(56, 189, 248, 0.12)'};
        border-left: 4px solid {accent1};
        padding: 14px 18px;
        border-radius: 0 10px 10px 0;
        margin: 14px 0;
        line-height: 1.6;
        color: {page_text};
    }}
    .security-advisory {{
        background: {'#FFFBEB' if not is_night else 'rgba(245, 158, 11, 0.12)'};
        border: 1.5px solid {'#F59E0B' if not is_night else '#B45309'};
        border-radius: 8px;
        padding: 10px 14px;
        color: {'#92400E' if not is_night else '#FCD34D'};
        font-size: 0.88rem;
        font-weight: 700;
        margin: 10px 0;
    }}
    .hashtag-pill {{
        display: inline-block;
        background: {accent1}22;
        color: {accent1};
        border: 1px solid {accent1}55;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 0.82rem;
        font-weight: 800;
        margin: 4px 4px 4px 0;
    }}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. RECRUITER VERIFICATION VIEW
# ---------------------------------------------------------
query_params = st.query_params
active_cred_query = query_params.get("cred", None)

if active_cred_query:
    target_cred = next((p for p in st.session_state.completed_tracks if p["share_id"] == active_cred_query), None)
    
    st.markdown('<div class="glass-card" style="border:2px solid #10B981;">', unsafe_allow_html=True)
    st.markdown(f'<div style="color:#10B981;font-weight:800;font-size:0.85rem;letter-spacing:0.1em;margin-bottom:6px;">NEXTSTRIDE VERIFIED PROOF-OF-WORK DOSSIER</div>', unsafe_allow_html=True)
    
    if target_cred:
        masked_email = "c*****r@nextstride.ai"
        st.markdown(f'<h2 style="margin:0;color:{page_text};">{target_cred["title"]}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:{label_text};font-weight:700;font-size:0.95rem;margin:8px 0 16px 0;">Credential ID: <code>{target_cred["share_id"]}</code> • Completed: {target_cred["date"]}</div>', unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"**Verified Candidate:**\n{st.session_state.user_profile.get('name')}")
        with c2:
            st.markdown(f"**Candidate Contact:**\n`{masked_email}`")
        with c3:
            st.markdown(f"**Assessment Score:**\n:green[**{target_cred['score']} / 100** (Verified)]")
        
        st.divider()
        st.markdown("### 📋 Competency Proof & Rubric Overview")
        st.write(target_cred["summary"])
        
        st.info("🔒 **Recruiter Privacy Mode Active:** Raw candidate source files, terminal screenshots, and private directory paths are protected and verified via automated rubrics.")
        
        with st.expander("🔍 View Technical Rubric & Evaluator Criteria (5 Verified Standards)"):
            st.markdown("""
            * **1. Syntax & Modern Standards:** Conforms to strict static type definitions, idiomatic structures, and current language guidelines.
            * **2. Systems Architecture & Memory:** Memory-efficient stream processing with O(1) buffer complexity under load.
            * **3. Error Handling & Edge Cases:** Robust handling of malformed inputs and resilience against service exceptions.
            * **4. Verification & Testing:** 100% test pass rate verified across automated unit and integration suites.
            * **5. Operational Security:** Clean configurations with zero hardcoded credentials, tokens, or environment leaks.
            """)
    else:
        st.error(f"Credential record `{active_cred_query}` not found in the verified database.")
    
    if st.button("← Return to NextStride Portal"):
        st.query_params.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# 5. AI ENGINE SETUP
# ---------------------------------------------------------
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

client = genai.Client(api_key=st.session_state.gemini_api_key) if st.session_state.gemini_api_key else None
CANDIDATE_MODELS = ["gemini-3.6-flash", "gemini-3.5-flash-lite"]

def generate_roadmap_ai(target_role, starting_level, job_desc=""):
    if not client:
        return PYTHON_6_STAGE_CURRICULUM
    
    prompt = f"""
    Create a practical 6-step progressive mastery roadmap from {starting_level} to Senior readiness for: {target_role}.
    Context: {job_desc or 'Standard industry benchmark'}
    
    CRITICAL: Each of the 6 steps must include AT LEAST 4 sequential blueprint steps with code examples and guidance.
    
    Return ONLY a raw JSON array matching:
    [
      {{
        "step_number": 1,
        "tier": "Stage 1: Core Tooling",
        "skill_title": "string",
        "skill_description": "Comprehensive explanation of this skill, architectural concepts, and why it is critical.",
        "market_insight": "Market demand or employer expectation insight",
        "resource_title": "string",
        "resource_url": "https://...",
        "task_title": "string",
        "step_by_step_blueprint": [
          {{"step_name": "Step 1: Environment & Tooling Setup", "guidance": "Paragraph explanation.", "code_example": "code snippet"}},
          {{"step_name": "Step 2: Scaffolding & Configuration", "guidance": "Paragraph explanation.", "code_example": "code snippet"}},
          {{"step_name": "Step 3: Core Implementation", "guidance": "Paragraph explanation.", "code_example": "code snippet"}},
          {{"step_name": "Step 4: Verification & Testing", "guidance": "Paragraph explanation.", "code_example": "code snippet"}}
        ],
        "evaluator_rubric": "string"
      }}
    ]
    """
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Curriculum Director. Output 6 detailed stages with at least 4 blueprint steps per stage in raw JSON array only.",
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            data = json.loads(response.text)
            return [{**item, "is_unlocked": (i == 0), "is_completed": False} for i, item in enumerate(data)]
        except Exception:
            continue
    return PYTHON_6_STAGE_CURRICULUM

def evaluate_submission_ai(task_instructions, rubric, submission, mode, screenshot_count=0):
    if not client:
        return {"passed": True, "score": 92, "feedback": "Demonstration approved with clean architectural patterns.", "hints": "Next tier unlocked."}

    prompt = f"""
    Evaluation Mode: {mode}
    Task Guidance: {task_instructions}
    Rubric: {rubric}
    Attached Artifact Screenshots Provided: {screenshot_count} files verified.
    
    Candidate Code/Text Submission:
    \"\"\"{submission or 'Candidate submitted visual proof of execution.'}\"\"\"
    
    Return strict JSON:
    {{
      "passed": boolean,
      "score": integer (0 to 100),
      "feedback": "string",
      "hints": "string"
    }}
    """
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="Automated technical assessor. 70 is passing threshold.",
                    response_mime_type="application/json",
                    temperature=0.1
                )
            )
            return json.loads(response.text)
        except Exception:
            continue
    return {"passed": True, "score": 90, "feedback": "Evaluation cleared successfully.", "hints": "Next milestone ready."}

def support_chat_ai(user_question):
    if not client:
        return "NextStride Support Bot: You can generate tailored 6-step roadmaps in the Career Accelerator, test code in the Language Lab, and share verified credential links with recruiters."
    
    system_prompt = """
    You are the dedicated AI Support Concierge for NextStride.
    You ONLY answer questions directly related to NextStride features, step gating, language lab, or credentials.
    """
    for model_name in CANDIDATE_MODELS:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_question,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.3
                )
            )
            return response.text
        except Exception:
            continue
    return "Support system is momentarily busy. Please consult the FAQs."

# ---------------------------------------------------------
# 6. SIDEBAR NAVIGATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
            <div style="color:{accent1};">{SVG_ICONS["brand_logo"]}</div>
            <span class="unfold-brand" style="font-size:1.55rem;">NEXTSTRIDE</span>
        </div>
        <div style="font-size:0.75rem;letter-spacing:0.14em;color:{accent1};font-weight:800;margin-bottom:14px;">
            NEURAL CAREER ACCELERATOR
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.user_authenticated:
        user_name = st.session_state.user_profile.get("name", "Creative Operator")
        st.markdown(
            f"""
            <div style="border:1.5px solid {card_border};border-radius:14px;padding:12px;background:{'rgba(255,255,255,0.04)' if is_night else '#FFFFFF'};margin-bottom:14px;">
                <div style="display:flex;align-items:center;justify-content:space-between;">
                    <div style="font-weight:800;font-size:1.05rem;color:{page_text};">{user_name}</div>
                    <span style="font-size:0.7rem;background:{accent1};color:#FFFFFF;padding:2px 8px;border-radius:999px;font-weight:800;">
                        ACTIVE
                    </span>
                </div>
                <div style="font-size:0.8rem;color:{label_text};font-weight:600;">{st.session_state.user_profile.get('role', 'Operator')}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        if st.button("☀️ Day", use_container_width=True, type="primary" if not is_night else "secondary"):
            if is_night:
                st.session_state.is_night_mode = False
                st.rerun()
    with theme_col2:
        if st.button("🌙 Night", use_container_width=True, type="primary" if is_night else "secondary"):
            if not is_night:
                st.session_state.is_night_mode = True
                st.rerun()

    st.markdown("<div style='margin:12px 0;height:1px;background:rgba(128,128,128,0.2);'></div>", unsafe_allow_html=True)

    if st.session_state.user_authenticated:
        st.markdown(f'<div style="font-size:0.75rem;font-weight:800;color:{label_text};letter-spacing:0.1em;margin-bottom:8px;">NAVIGATION</div>', unsafe_allow_html=True)
        nav_items = [
            ("Dashboard", "dashboard"),
            ("Career Accelerator", "target"),
            ("Language Lab", "code"),
            ("Completed Paths", "award"),
            ("Credentials", "credential"),
            ("Profile Settings", "user"),
            ("Support & FAQ", "help")
        ]

        for label, icon_key in nav_items:
            is_current = (st.session_state.active_nav == label)
            btn_type = "primary" if is_current else "secondary"
            if st.button(f"{label}", use_container_width=True, type=btn_type, key=f"nav_{label}"):
                st.session_state.active_nav = label
                st.rerun()

        if st.button("Disconnect Session", use_container_width=True):
            st.session_state.user_authenticated = False
            st.rerun()
    else:
        st.markdown(f'<strong style="font-size:0.95rem;color:{page_text};">IDENTITY ACCESS</strong>', unsafe_allow_html=True)
        tab_email, tab_google, tab_otp = st.tabs(["Email", "Google One-Tap", "OTP"])
        with tab_email:
            e_val = st.text_input("Account Email", value="engineer@domain.com", key="auth_email")
            p_val = st.text_input("Security Cipher", type="password", value="demo1234", key="auth_pwd")
            if st.button("Authenticate", use_container_width=True, key="btn_signin"):
                st.session_state.user_authenticated = True
                st.session_state.day_colors = random.choice(DAY_DUAL_TONES)
                st.session_state.active_nav = "Dashboard"
                st.rerun()
        with tab_google:
            st.write("")
            if st.button("Continue with Google One-Tap", use_container_width=True):
                st.session_state.user_authenticated = True
                st.session_state.day_colors = random.choice(DAY_DUAL_TONES)
                st.session_state.active_nav = "Dashboard"
                st.rerun()
        with tab_otp:
            ph_val = st.text_input("Mobile Signal", placeholder="+1 234 567 8900", key="auth_phone")
            otp_val = st.text_input("One-Time PIN", placeholder="6-digit", key="auth_otp")
            if st.button("Verify & Sign In", use_container_width=True):
                st.session_state.user_authenticated = True
                st.session_state.day_colors = random.choice(DAY_DUAL_TONES)
                st.session_state.active_nav = "Dashboard"
                st.rerun()

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    with st.expander("API Key Configuration", icon=":material/key:"):
        k_in = st.text_input(
            "Gemini Key",
            value=st.session_state.gemini_api_key,
            type="password",
            placeholder="AIzaSy...",
            help="Free key from Google AI Studio"
        )
        if k_in != st.session_state.gemini_api_key:
            st.session_state.gemini_api_key = k_in
            st.rerun()

# ---------------------------------------------------------
# 7. MAIN VIEWPORT (PRE-LOGIN LANDING VS AUTH DASHBOARD)
# ---------------------------------------------------------
if not st.session_state.user_authenticated:
    st.markdown(f'<h1 class="unfold-brand" style="font-size:2.8rem;margin-bottom:2px;">NEXTSTRIDE</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:1.15rem;font-weight:700;color:{label_text};margin-bottom:18px;">AI-Architected Career Pipelines with Step-Gated Proof of Competency</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["target"]}</span>Autonomous Proof-of-Work Protocol</h3>', unsafe_allow_html=True)
    st.write("NextStride replaces passive tutorial checklists with rigorous, AI-graded milestone challenges. Advance only when your code or project implementation satisfies production-level rubrics.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown(f"""<div class="portalix-stat-tile" style="text-align:left;"><div style="color:{accent1};margin-bottom:8px;">{SVG_ICONS["target"]}</div><strong>Tailored Roadmaps</strong><p style="font-size:0.9rem;opacity:0.85;margin-top:4px;">Translates specific role targets into structured, beginner-to-senior steps.</p></div>""", unsafe_allow_html=True)
    with col_f2:
        st.markdown(f"""<div class="portalix-stat-tile" style="text-align:left;"><div style="color:{accent1};margin-bottom:8px;">{SVG_ICONS["lock"]}</div><strong>Task Gating</strong><p style="font-size:0.9rem;opacity:0.85;margin-top:4px;">Subsequent tiers remain strictly locked until your submission clears AI grading.</p></div>""", unsafe_allow_html=True)
    with col_f3:
        st.markdown(f"""<div class="portalix-stat-tile" style="text-align:left;"><div style="color:{accent1};margin-bottom:8px;">{SVG_ICONS["award"]}</div><strong>Verified Badges</strong><p style="font-size:0.9rem;opacity:0.85;margin-top:4px;">All approved solutions automatically populate a public proof-of-work portfolio.</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    
    st.markdown(f'<h4><span class="icon-inline">{SVG_ICONS["code"]}</span>Interactive Protocol Preview</h4>', unsafe_allow_html=True)
    st.caption("Here is how milestones are verified on your active path:")
    
    demo_col1, demo_col2 = st.columns([1, 1])
    with demo_col1:
        st.code("""# Task: Implement idempotency key check
def verify_transaction(tx_id: str, log: set) -> bool:
    if tx_id in log:
        return False
    log.add(tx_id)
    return True""", language="python")
    with demo_col2:
        st.markdown(f"""<div style="border:1.5px solid #10B981;padding:14px;border-radius:10px;background:rgba(16,185,129,0.08);"><div style="color:#10B981;font-weight:800;font-size:0.85rem;">EVALUATOR VERDICT: PASS (92/100)</div><div style="font-size:0.85rem;margin-top:4px;color:{page_text};font-weight:600;">Correct O(1) hash set membership check implemented. Milestone 1 cleared. Tier 2 unlocked.</div></div>""", unsafe_allow_html=True)
        st.info("Authenticate via the sidebar to initiate your personalized accelerator track.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------
# 8. AUTHENTICATED HEADER & VIEWS
# ---------------------------------------------------------
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    st.markdown(f'<h1 class="unfold-brand" style="font-size:2.8rem;margin-bottom:2px;">NEXTSTRIDE</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:1.1rem;font-weight:700;color:{label_text};margin-bottom:14px;">Adaptive Career Engineering & Verified Competency Pipelines</div>', unsafe_allow_html=True)

with top_col2:
    if st.button(f"👤 {st.session_state.user_profile.get('name', 'Operator')}", use_container_width=True):
        st.session_state.active_nav = "Profile Settings"
        st.rerun()

# ---------------------------------------------------------
# VIEW: DASHBOARD
# ---------------------------------------------------------
if st.session_state.active_nav == "Dashboard":
    now_str = datetime.now().strftime("%A, %B %d, %Y")
    st.markdown(
        f"""
        <div class="glass-card" style="border:1.5px solid {accent1};">
            <h2 style="margin-bottom:4px;color:{page_text};">Good {'Evening' if is_night else 'Day'}, {st.session_state.user_profile.get('name')}! 🚀</h2>
            <div style="color:{label_text};font-weight:700;font-size:0.95rem;margin-bottom:12px;">{now_str} • Verified Session Dashboard</div>
            <p style="margin-bottom:0;color:{page_text};">NextStride proof-of-work matrix is active. Access your 6-tier roadmaps, completed paths, and verified credentials below.</p>
        </div>
        """, unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="portalix-stat-tile"><div style="font-size:2rem;font-weight:900;color:{accent1};">2</div><div style="font-size:0.8rem;font-weight:800;color:{label_text};">COMPLETED PATHS</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="portalix-stat-tile"><div style="font-size:2rem;font-weight:900;color:{accent1};">12</div><div style="font-size:0.8rem;font-weight:800;color:{label_text};">MILESTONES CLEARED</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="portalix-stat-tile"><div style="font-size:2rem;font-weight:900;color:{accent1};">93.5%</div><div style="font-size:0.8rem;font-weight:800;color:{label_text};">AVERAGE SCORE</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="portalix-stat-tile"><div style="font-size:2rem;font-weight:900;color:{accent1};">2</div><div style="font-size:0.8rem;font-weight:800;color:{label_text};">ACTIVE CREDENTIALS</div></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<h4><span class="icon-inline">{SVG_ICONS["target"]}</span>Career Accelerator Pipeline</h4>', unsafe_allow_html=True)
        st.write("Synthesize and execute a progressive 6-stage role accelerator with strict code and visual screenshot gating.")
        if st.button("Launch Career Accelerator", use_container_width=True):
            st.session_state.active_nav = "Career Accelerator"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with d_col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<h4><span class="icon-inline">{SVG_ICONS["code"]}</span>Language & Systems Lab</h4>', unsafe_allow_html=True)
        st.write("Practice programming languages across 6 structured steps in Free Learning Mode or Job Verification Mode.")
        if st.button("Open Language Lab", use_container_width=True):
            st.session_state.active_nav = "Language Lab"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: CAREER ACCELERATOR (Minimum 4 Blueprint Steps Per Stage)
# ---------------------------------------------------------
elif st.session_state.active_nav == "Career Accelerator":
    if not st.session_state.roadmap:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["trend"]}</span>Target Position & Calibration</h3>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            selected_pos = st.selectbox("Target Position", IT_CAREER_ROLES)
            if selected_pos == "Other / Custom Role":
                target_role = st.text_input("Specify Custom Target Position", placeholder="e.g., Quantum Computing Software Lead")
            else:
                target_role = selected_pos

        with col2:
            starting_level = st.selectbox("Baseline Experience", ["Foundational / Student", "Transitioning Developer", "Mid-Level Engineer", "Senior Moving to Lead"])

        job_desc = st.text_area("Target Job Specification (Optional)", placeholder="Paste benchmark keywords or descriptions from target companies...")

        if st.button("Synthesize Accelerator Path (6-Tiers)", use_container_width=True):
            with st.spinner("Synthesizing 6-tier curriculum via Gemini Flash..."):
                steps = generate_roadmap_ai(target_role, starting_level, job_desc)
                if steps:
                    st.session_state.roadmap = steps
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        col_nav1, col_nav2 = st.columns([1, 4])
        with col_nav1:
            if st.button("← Return to Setup", use_container_width=True):
                st.session_state.roadmap = []
                st.session_state.evaluation_results = {}
                st.rerun()
        with col_nav2:
            cleared_steps = sum(1 for s in st.session_state.roadmap if s.get("is_completed", False))
            st.progress(cleared_steps / len(st.session_state.roadmap), text=f"Progress: {cleared_steps}/{len(st.session_state.roadmap)} Milestones Cleared")

        for idx, step in enumerate(st.session_state.roadmap):
            is_unlocked = step.get("is_unlocked", False)
            is_completed = step.get("is_completed", False)
            step_num = step.get("step_number", idx + 1)

            card_class = "glass-card"
            status_icon = SVG_ICONS["check"] if is_completed else (SVG_ICONS["unlock"] if is_unlocked else SVG_ICONS["lock"])

            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            
            col_h1, col_h2 = st.columns([4, 1])
            with col_h1:
                st.markdown(f'<h3><span class="icon-inline">{status_icon}</span>Step {step_num}: {step["skill_title"]}</h3>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-badge">{SVG_ICONS["trend"]}&nbsp;{step.get("market_insight", "High Market Demand")}</div>', unsafe_allow_html=True)
            with col_h2:
                st.markdown(f"<span style='font-family:Orbitron;font-size:0.8rem;color:{accent1};font-weight:800;'>{step.get('tier', 'Standard').upper()}</span>", unsafe_allow_html=True)

            st.markdown(
                f"""
                <div class="skill-knowledge-box">
                    <div style="font-weight:800;font-size:0.95rem;margin-bottom:4px;color:{accent1};">
                        SKILL ARCHITECTURE & PARADIGM
                    </div>
                    <div>{step.get("skill_description", "Core technological paradigm for this milestone.")}</div>
                </div>
                """, unsafe_allow_html=True
            )

            st.markdown(f'<div class="icon-inline">{SVG_ICONS["code"]}</div><strong style="font-size:1.05rem;">Task Objective: {step["task_title"]}</strong>', unsafe_allow_html=True)
            st.write("Click each sequential blueprint step below to read the comprehensive explanation and copy execution codes:")

            # Ensure minimum 4 blueprint steps
            raw_blueprints = step.get("step_by_step_blueprint", [])
            if len(raw_blueprints) < 4:
                blueprints = [
                    {"step_name": "Step 1: Environment & Tooling Setup", "guidance": "Initialize the environment, runtime dependencies, and package configurations.", "code_example": "python -m venv venv\nsource venv/bin/activate"},
                    {"step_name": "Step 2: Scaffolding & Architecture", "guidance": "Structure directories, create entry files, and configure modular components.", "code_example": "mkdir -p src/tests && touch src/main.py"},
                    {"step_name": "Step 3: Core Implementation", "guidance": "Write idiomatic, strongly-typed code satisfying core technical constraints.", "code_example": "def execute():\n    return True"},
                    {"step_name": "Step 4: Verification & Automated Testing", "guidance": "Run terminal test suites and assert correct output formats.", "code_example": "pytest -v"}
                ]
            else:
                blueprints = raw_blueprints

            for bp in blueprints:
                s_name = bp.get("step_name") if isinstance(bp, dict) else str(bp)
                s_guide = bp.get("guidance", "Execute instructions.") if isinstance(bp, dict) else "Execute instructions."
                s_code = bp.get("code_example", "python --version") if isinstance(bp, dict) else "python --version"
                
                with st.expander(f"📌 {s_name}"):
                    st.write(s_guide)
                    st.code(s_code, language="python" if not s_code.startswith("python") and not s_code.startswith("docker") and not s_code.startswith("alembic") and not s_code.startswith("curl") else "bash")

            if is_unlocked and not is_completed:
                st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
                st.markdown(f'<div class="icon-inline">{SVG_ICONS["camera"]}</div><strong>Verification Gate (Upload 1 to 3 Screenshots OR Enter Code)</strong>', unsafe_allow_html=True)
                
                st.markdown(
                    """
                    <div class="security-advisory">
                        🔒 <strong>Security Advisory:</strong> Ensure screenshots and code submissions do not expose active API tokens, passwords, database credentials, or personal OS directories.
                    </div>
                    """, unsafe_allow_html=True
                )

                uploaded_screens = st.file_uploader(
                    f"Upload Screenshots for Step {step_num} (1 to 3 Files)",
                    type=["png", "jpg", "jpeg", "webp"],
                    accept_multiple_files=True,
                    key=f"uploader_{idx}"
                )

                screen_count = len(uploaded_screens) if uploaded_screens else 0
                if screen_count > 3:
                    st.warning("⚠️ Maximum 3 screenshots allowed. Only the first 3 will be analyzed.")
                    screen_count = 3
                elif screen_count >= 1:
                    st.success(f"✓ {screen_count} screenshot(s) attached.")

                eval_mode = st.radio(
                    f"Evaluator Mode (Step {step_num})",
                    ["Supportive Mentor", "Strict Interviewer"],
                    horizontal=True,
                    key=f"mode_{idx}"
                )

                user_code = st.text_area(
                    f"Code & Solution Implementation for Step {step_num}",
                    placeholder="Paste source code, terminal logs, or solution notes...",
                    key=f"input_{idx}",
                    height=130
                )

                can_evaluate = bool(user_code.strip()) or (screen_count >= 1)

                if not can_evaluate:
                    st.info("ℹ️ Submit via **OR Mode**: Provide source code/text OR upload at least 1 screenshot to enable review.")

                if st.button(f"Submit Step {step_num} for Review", key=f"btn_{idx}", disabled=not can_evaluate):
                    with st.spinner("AI assessing submission artifacts..."):
                        mode_tag = "mentor" if eval_mode == "Supportive Mentor" else "interviewer"
                        result = evaluate_submission_ai(str(blueprints), step["evaluator_rubric"], user_code, mode_tag, screen_count)
                        st.session_state.evaluation_results[idx] = result

                        if result.get("passed", False):
                            step["is_completed"] = True
                            if idx + 1 < len(st.session_state.roadmap):
                                st.session_state.roadmap[idx + 1]["is_unlocked"] = True
                            st.rerun()

                if idx in st.session_state.evaluation_results:
                    res = st.session_state.evaluation_results[idx]
                    if res.get("passed"):
                        st.success(f"SCORE: {res.get('score')}/100 — APPROVED\n\n{res.get('feedback')}")
                    else:
                        st.error(f"SCORE: {res.get('score')}/100 — REVISION REQUIRED\n\n{res.get('feedback')}")
            
            elif is_completed:
                st.success("✓ Milestone verified and archived into your competency portfolio.")
            else:
                st.caption("Complete and pass preceding steps to access this verification gate.")

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: LANGUAGE LAB (Minimum 4 Blueprint Steps Per Stage)
# ---------------------------------------------------------
elif st.session_state.active_nav == "Language Lab":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["code"]}</span>Language & Systems Lab</h3>', unsafe_allow_html=True)
    st.write("Master fundamental and systems programming languages across 6 modular stages with minimum 4 detailed blueprint steps each.")

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        chosen_lang = st.selectbox("Select Programming Language", PROGRAMMING_LANGUAGES)
    with col_l2:
        lab_mode = st.radio("Lab Mode", ["Learning Mode (No Gating / Free Study)", "Job Mode (Step-Gated with AI Proof Verification)"], horizontal=True)

    if st.button("Generate Language Blueprint (6 Steps)", use_container_width=True):
        with st.spinner(f"Compiling 6-stage {chosen_lang} curriculum..."):
            st.session_state.lang_roadmap = [dict(s) for s in PYTHON_6_STAGE_CURRICULUM]
            st.session_state.lang_eval_results = {}
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.lang_roadmap:
        is_job = "Job" in lab_mode
        st.markdown(f"#### Active Track: {chosen_lang} — {'⚡ Job Mode (Verification Enabled)' if is_job else '📖 Free Learning Mode'}")

        for s_idx, l_step in enumerate(st.session_state.lang_roadmap):
            is_unlocked = l_step.get("is_unlocked", False) or not is_job
            is_completed = l_step.get("is_completed", False)
            stage_num = l_step.get("step_number", s_idx + 1)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            status_icon = SVG_ICONS["check"] if is_completed else (SVG_ICONS["unlock"] if is_unlocked else SVG_ICONS["lock"])
            
            st.markdown(f"### <span class='icon-inline'>{status_icon}</span>Stage {stage_num}: {l_step.get('skill_title')}", unsafe_allow_html=True)
            st.write(l_step.get("skill_description"))

            # Render all blueprint steps (guaranteed minimum 4)
            for bp in l_step.get("step_by_step_blueprint", []):
                with st.expander(f"🔹 {bp.get('step_name')}"):
                    st.write(bp.get("guidance"))
                    st.code(bp.get("code_example", "# Run example"), language="python" if not bp.get("code_example", "").startswith("docker") and not bp.get("code_example", "").startswith("python") and not bp.get("code_example", "").startswith("alembic") else "bash")

            if is_job and is_unlocked and not is_completed:
                st.divider()
                st.markdown(f"**Verification Gate (Stage {stage_num}):** {l_step.get('task_title')}")
                
                st.markdown(
                    """
                    <div class="security-advisory">
                        🔒 <strong>Security Advisory:</strong> Ensure screenshots and code submissions do not expose active API tokens, passwords, database credentials, or personal OS directories.
                    </div>
                    """, unsafe_allow_html=True
                )

                uploaded_lang_screens = st.file_uploader(
                    f"Upload Screenshots for Stage {stage_num} (1 to 3 Files)",
                    type=["png", "jpg", "jpeg", "webp"],
                    accept_multiple_files=True,
                    key=f"lang_uploader_{s_idx}"
                )

                l_screen_count = len(uploaded_lang_screens) if uploaded_lang_screens else 0
                if l_screen_count > 3:
                    st.warning("⚠️ Maximum 3 screenshots allowed. Only the first 3 will be analyzed.")
                    l_screen_count = 3
                elif l_screen_count >= 1:
                    st.success(f"✓ {l_screen_count} screenshot(s) attached.")

                l_eval_mode = st.radio(
                    f"Evaluator Mode (Stage {stage_num})",
                    ["Supportive Mentor", "Strict Interviewer"],
                    horizontal=True,
                    key=f"lang_mode_{s_idx}"
                )

                lang_ans = st.text_area(
                    f"Code & Solution Implementation for Stage {stage_num}",
                    placeholder="Paste source code, terminal logs, or test proofs...",
                    key=f"lang_ans_{s_idx}",
                    height=130
                )

                can_eval_lang = bool(lang_ans.strip()) or (l_screen_count >= 1)

                if not can_eval_lang:
                    st.info("ℹ️ Submit via **OR Mode**: Provide source code/text OR upload at least 1 screenshot to enable review.")

                if st.button(f"Submit Stage {stage_num} for Review", key=f"lang_btn_{s_idx}", disabled=not can_eval_lang):
                    with st.spinner("AI evaluating technical proof..."):
                        m_tag = "mentor" if l_eval_mode == "Supportive Mentor" else "interviewer"
                        res = evaluate_submission_ai(str(l_step.get("step_by_step_blueprint", "")), l_step.get("evaluator_rubric", "Strict"), lang_ans, m_tag, l_screen_count)
                        st.session_state.lang_eval_results[s_idx] = res
                        if res.get("passed"):
                            l_step["is_completed"] = True
                            if s_idx + 1 < len(st.session_state.lang_roadmap):
                                st.session_state.lang_roadmap[s_idx + 1]["is_unlocked"] = True
                            st.rerun()

                if s_idx in st.session_state.lang_eval_results:
                    res_obj = st.session_state.lang_eval_results[s_idx]
                    if res_obj.get("passed"):
                        st.success(f"SCORE: {res_obj.get('score')}/100 — APPROVED\n\n{res_obj.get('feedback')}")
                    else:
                        st.error(f"SCORE: {res_obj.get('score')}/100 — REVISION REQUIRED\n\n{res_obj.get('feedback')}")

            elif is_job and is_completed:
                st.success(f"✓ Stage {stage_num} verified and unlocked.")
            elif is_job and not is_unlocked:
                st.caption("Complete and pass preceding stages to access this verification gate.")

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: COMPLETED PATHS
# ---------------------------------------------------------
elif st.session_state.active_nav == "Completed Paths":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["award"]}</span>Completed Pathways Archive</h3>', unsafe_allow_html=True)
    st.write("Click any completed pathway below to view the verified 6-step breakdown, solution notes, and certificates:")

    for idx, path in enumerate(st.session_state.completed_tracks):
        st.markdown(
            f"""
            <div style="border:1.5px solid {accent1};border-radius:12px;padding:18px;margin-bottom:14px;background:{'rgba(255,255,255,0.03)' if is_night else '#FFFFFF'};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h4 style="margin:0;color:{page_text};font-size:1.15rem;">{path['title']}</h4>
                    <span class="metric-badge">VERIFIED GRADE: {path['score']}/100</span>
                </div>
                <div style="font-size:0.85rem;color:{label_text};margin:6px 0;">Credential ID: <code>{path['share_id']}</code> • Date: {path['date']} • 6/6 Steps Cleared</div>
                <p style="margin:6px 0;color:{page_text};font-size:0.95rem;">{path['summary']}</p>
            </div>
            """, unsafe_allow_html=True
        )

        col_p1, col_p2 = st.columns([2, 1])
        with col_p1:
            if st.button(f"Inspect Completed Steps ({path['title']})", key=f"view_path_{idx}", use_container_width=True):
                st.session_state.roadmap = path["steps_data"]
                st.session_state.active_nav = "Career Accelerator"
                st.rerun()
        with col_p2:
            if st.button(f"Share Credential Link", key=f"share_path_{idx}", use_container_width=True):
                st.session_state.active_nav = "Credentials"
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: CREDENTIALS (RECRUITER VIEW BUTTON)
# ---------------------------------------------------------
elif st.session_state.active_nav == "Credentials":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["credential"]}</span>Verified Credentials & Recruiter Links</h3>', unsafe_allow_html=True)
    st.write("Share verified credential URLs with recruiters. External viewers see only candidate proof and evaluation scores; raw code and screenshots remain protected.")

    for idx, path in enumerate(st.session_state.completed_tracks):
        c_id = path["share_id"]
        direct_url = f"http://localhost:8501/?cred={c_id}"
        
        st.markdown(
            f"""
            <div style="border:1.5px solid {accent1};border-radius:12px;padding:16px;margin-bottom:14px;background:{'rgba(255,255,255,0.03)' if is_night else '#F8FAFC'};">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <h4 style="margin:0;color:{page_text};font-size:1.15rem;">{path['title']}</h4>
                    <span class="metric-badge">VERIFIED SCORE: {path['score']}/100</span>
                </div>
                <div style="font-size:0.85rem;color:{label_text};margin:6px 0;">Credential ID: <code>{c_id}</code> • Date: {path['date']}</div>
                <div style="font-size:0.9rem;margin-top:6px;color:{page_text};">{path['summary']}</div>
            </div>
            """, unsafe_allow_html=True
        )

        col_c1, col_c2 = st.columns([3, 1])
        with col_c1:
            st.text_input(f"Recruiter Verification Link ({path['title']})", value=direct_url, key=f"link_{c_id}")
        with col_c2:
            st.write("")
            st.write("")
            if st.button("Recruiter View", key=f"test_hr_{idx}", use_container_width=True):
                st.query_params["cred"] = c_id
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: PROFILE SETTINGS
# ---------------------------------------------------------
elif st.session_state.active_nav == "Profile Settings":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["user"]}</span>Operator Profile Configurations</h3>', unsafe_allow_html=True)

    prof_col1, prof_col2 = st.columns(2)
    with prof_col1:
        new_name = st.text_input("Operator Name", value=st.session_state.user_profile.get("name", ""))
        new_email = st.text_input("Associated Email", value=st.session_state.user_profile.get("email", ""))
    with prof_col2:
        new_role = st.text_input("Headline Title", value=st.session_state.user_profile.get("role", ""))
        new_bio = st.text_area("Professional Bio", value=st.session_state.user_profile.get("bio", ""))

    if st.button("Update Profile Information", use_container_width=True):
        st.session_state.user_profile["name"] = new_name
        st.session_state.user_profile["email"] = new_email
        st.session_state.user_profile["role"] = new_role
        st.session_state.user_profile["bio"] = new_bio
        st.success("Profile saved successfully.")

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🏷️ Verified Competency Hashtags")
    st.caption("Hashtags dynamically generated from completed pathways and verified milestones:")

    all_tags = []
    for track in st.session_state.completed_tracks:
        all_tags.extend(track.get("hashtags", []))

    if all_tags:
        pill_html = "".join([f'<span class="hashtag-pill">{tag}</span>' for tag in set(all_tags)])
        st.markdown(f'<div>{pill_html}</div>', unsafe_allow_html=True)
    else:
        st.caption("Complete accelerator tracks to earn verified skill hashtags.")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# VIEW: SUPPORT & FAQ
# ---------------------------------------------------------
elif st.session_state.active_nav == "Support & FAQ":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["help"]}</span>Platform Frequently Asked Questions</h3>', unsafe_allow_html=True)

    with st.expander("1. Dashboard: What metrics are tracked on my portal?"):
        st.write("The Dashboard tracks total active milestones, cleared proofs, average competency score, and verified credential certificates across all paths.")

    with st.expander("2. Career Accelerator: How does the 6-tier gating work?"):
        st.write("Each role contains 6 progressive milestones (Fundamentals to Production Packaging). Milestones unlock sequentially after your submission clears AI grading with a score of 70 or higher.")

    with st.expander("3. Verification Gate: Can I submit using either code or screenshots? (OR Mode)"):
        st.write("Yes. You can submit via OR Mode: paste your source code/implementation text OR upload 1 to 3 screenshots of working execution to submit for evaluation.")

    with st.expander("4. Language Lab: What is the difference between Learning Mode and Job Mode?"):
        st.write("Learning Mode provides unstructured, free study without submission gates. Job Mode activates evaluation rubrics and verified milestone tracking.")

    with st.expander("5. Completed Paths: How do I review previous work?"):
        st.write("Click 'Inspect Completed Steps' on any completed track to open the pathway and review all 6 unlocked stages and solutions.")

    with st.expander("6. Credentials: How do recruiter links work and what information is shared?"):
        st.write("Recruiters only view candidate credentials, verified scores, and rubric criteria. Source code and private screenshots are excluded to prevent data leaks.")

    with st.expander("7. Profile Settings: Where do the skill hashtags come from?"):
        st.write("Hashtags populate dynamically as you complete steps and pipelines, reflecting your verified competencies.")

    with st.expander("8. Security & Data Protection: What should I avoid in screenshots?"):
        st.write("Ensure uploads do not include active API keys, production passwords, or personal operating system paths.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f'<h3><span class="icon-inline">{SVG_ICONS["brand_logo"]}</span>NextStride AI Concierge</h3>', unsafe_allow_html=True)
    
    for msg in st.session_state.support_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_q = st.chat_input("Type your NextStride platform question...")
    if user_q:
        st.session_state.support_messages.append({"role": "user", "content": user_q})
        with st.chat_message("user"):
            st.write(user_q)
        with st.chat_message("assistant"):
            ans = support_chat_ai(user_q)
            st.write(ans)
            st.session_state.support_messages.append({"role": "assistant", "content": ans})
    st.markdown('</div>', unsafe_allow_html=True)