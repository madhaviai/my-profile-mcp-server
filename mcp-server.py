#!/usr/bin/env python3
"""
MCP Server for Madhavi's Professional Profile
Provides tools to retrieve skills, experience, and professional details.
"""

import json
import asyncio
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Initialize the MCP server
server = Server("madhavi-profile")

# ============================================================================
# PROFILE DATA
# ============================================================================

PROFILE = {
    "name": "Madhavi K",
    "education": {
        "degree": "Masters",
        "university": "Purdue University",
        "field": "Computer Science / Engineering"
    },
    "contact": {
        "linkedin": "https://linkedin.com/in/madhaviai"
        "linkedin_username": "madhaviai"
    },
    "job_titles": [
        "AI Systems Engineer",
        "Applied LLM Engineer", 
        "Software Engineer, Agents",
        "Inference Platform Engineer"
    ],
    "summary": (
        "AI Systems Engineer with a Master's from Purdue University, specializing in "
        "building end-to-end LLM pipelines, agentic workflows, and scalable AI infrastructure. "
        "Expert in MCP development, cloud-native architectures, and production ML systems."
    )
}

SKILLS = {
    "llm_systems_engineering": {
        "name": "LLM Systems Engineering",
        "description": (
            "Builds end-to-end LLM pipelines, agentic workflows, and context-optimized "
            "systems using advanced tokenization, retrieval, and orchestration patterns."
        ),
        "keywords": ["LLM", "pipelines", "agentic workflows", "tokenization", "RAG", "orchestration"]
    },
    "agentic_automation": {
        "name": "Agentic Automation",
        "description": (
            "Designs autonomous, multi-step, self-correcting AI agents with tool-use, "
            "workflow chaining, and intelligent execution loops."
        ),
        "keywords": ["AI agents", "autonomous systems", "tool-use", "workflow chaining", "self-correcting"]
    },
    "mcp_development": {
        "name": "MCP Development",
        "description": (
            "Creates scalable Model Context Protocol servers and automation frameworks "
            "for seamless AI tool integration across product ecosystems."
        ),
        "keywords": ["MCP", "Model Context Protocol", "tool integration", "automation frameworks"]
    },
    "ai_infrastructure": {
        "name": "AI Infrastructure Engineering",
        "description": (
            "Architects cloud-native, high-performance AI systems leveraging Kubernetes, "
            "containers, networking, IaC, and distributed infra patterns."
        ),
        "keywords": ["Kubernetes", "containers", "IaC", "cloud-native", "distributed systems"]
    },
    "machine_learning": {
        "name": "Machine Learning Engineering",
        "description": (
            "Develops robust ML models, anomaly detection systems, and data-driven pipelines "
            "with strong emphasis on model behavior, evaluation, and interpretability."
        ),
        "keywords": ["ML models", "anomaly detection", "model evaluation", "interpretability"]
    },
    "backend_api": {
        "name": "Backend & API Engineering",
        "description": (
            "Builds scalable backend services, microservices, and automation APIs in Python, "
            "Go, Java, and TypeScript with clean, production-ready code."
        ),
        "keywords": ["Python", "Go", "Java", "TypeScript", "microservices", "APIs", "backend"]
    },
    "cloud_platforms": {
        "name": "Cloud Platforms (AWS, Azure, GCP)",
        "description": (
            "Designs, deploys, and optimizes multi-cloud infrastructure with secure "
            "architecture, performance tuning, and cost-efficient scaling."
        ),
        "keywords": ["AWS", "Azure", "GCP", "multi-cloud", "infrastructure", "scaling"]
    },
    "devops_cicd": {
        "name": "DevOps & CI/CD",
        "description": (
            "Implements automated build and deployment systems using Jenkins, GitLab, "
            "Azure DevOps, Spinnaker, and advanced Git workflows."
        ),
        "keywords": ["Jenkins", "GitLab", "Azure DevOps", "Spinnaker", "CI/CD", "automation"]
    },
    "data_streaming": {
        "name": "Data & Streaming Systems",
        "description": (
            "Constructs large-scale data ingestion, ETL, search, and streaming pipelines "
            "using Kafka, Elasticsearch, Redis, PostgreSQL, and modern storage stacks."
        ),
        "keywords": ["Kafka", "Elasticsearch", "Redis", "PostgreSQL", "ETL", "streaming"]
    },
    "security_threat_intel": {
        "name": "Security & Threat Intelligence",
        "description": (
            "Builds ML-powered threat detection, SIEM automation, and risk scoring systems "
            "with secure, enterprise-grade cloud architectures."
        ),
        "keywords": ["threat detection", "SIEM", "risk scoring", "security", "ML-powered"]
    },
    "monitoring_observability": {
        "name": "Monitoring & Observability",
        "description": (
            "Implements full-stack monitoring, logging, and alerting using Prometheus, "
            "Grafana, Kibana, and Dynatrace for system reliability and traceability."
        ),
        "keywords": ["Prometheus", "Grafana", "Kibana", "Dynatrace", "monitoring", "observability"]
    },
    "open_source": {
        "name": "Open-Source Engineering",
        "description": (
            "Contributes to developer tooling, Kubernetes ecosystems, and AI frameworks "
            "with high-quality code, documentation, and community-driven innovation."
        ),
        "keywords": ["open-source", "developer tooling", "Kubernetes", "AI frameworks"]
    },
    "research_optimization": {
        "name": "Research & Model Optimization",
        "description": (
            "Performs research on tokenization, representation learning, model robustness, "
            "and data efficiency to enhance LLM interpretability and performance."
        ),
        "keywords": ["research", "tokenization", "representation learning", "model optimization"]
    }
}

SKILL_CATEGORIES = {
    "ai_ml": ["llm_systems_engineering", "agentic_automation", "mcp_development", "machine_learning", "research_optimization"],
    "infrastructure": ["ai_infrastructure", "cloud_platforms", "devops_cicd"],
    "backend": ["backend_api", "data_streaming"],
    "security_ops": ["security_threat_intel", "monitoring_observability"],
    "community": ["open_source"]
}

# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List all available profile tools."""
    tools = [
        Tool(
            name="get_profile",
            description="Get Madhavi's complete professional profile including education and job titles",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_contact",
            description="Get contact information including LinkedIn profile",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_education",
            description="Get education details including degree and university",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_job_titles",
            description="Get suitable job titles for Madhavi's skillset",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_all_skills",
            description="Get a complete list of all technical skills with descriptions",
            inputSchema={
                "type": "object",
                "properties": {
                    "include_keywords": {
                        "type": "boolean",
                        "description": "Whether to include keywords for each skill",
                        "default": False
                    }
                }
            }
        ),
        Tool(
            name="get_skill",
            description="Get details about a specific skill",
            inputSchema={
                "type": "object",
                "properties": {
                    "skill_id": {
                        "type": "string",
                        "description": "The skill identifier (e.g., 'llm_systems_engineering', 'mcp_development')",
                        "enum": list(SKILLS.keys())
                    }
                },
                "required": ["skill_id"]
            }
        ),
        Tool(
            name="get_skills_by_category",
            description="Get skills filtered by category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "The category to filter by",
                        "enum": ["ai_ml", "infrastructure", "backend", "security_ops", "community"]
                    }
                },
                "required": ["category"]
            }
        ),
        Tool(
            name="search_skills",
            description="Search skills by keyword or technology",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (e.g., 'Python', 'Kubernetes', 'LLM')"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="get_summary",
            description="Get a brief professional summary",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="get_technologies",
            description="Get a list of all technologies and tools",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        )
    ]
    
    return ListToolsResult(tools=tools)

# ============================================================================
# TOOL HANDLERS
# ============================================================================

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    
    try:
        if name == "get_profile":
            return await get_profile()
        elif name == "get_contact":
            return await get_contact()
        elif name == "get_education":
            return await get_education()
        elif name == "get_job_titles":
            return await get_job_titles()
        elif name == "get_all_skills":
            return await get_all_skills(arguments.get("include_keywords", False))
        elif name == "get_skill":
            return await get_skill(arguments["skill_id"])
        elif name == "get_skills_by_category":
            return await get_skills_by_category(arguments["category"])
        elif name == "search_skills":
            return await search_skills(arguments["query"])
        elif name == "get_summary":
            return await get_summary()
        elif name == "get_technologies":
            return await get_technologies()
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")]
            )
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error executing {name}: {str(e)}")]
        )


async def get_profile() -> CallToolResult:
    """Get complete professional profile."""
    result = {
        "name": PROFILE["name"],
        "education": PROFILE["education"],
        "contact": PROFILE["contact"],
        "job_titles": PROFILE["job_titles"],
        "summary": PROFILE["summary"],
        "total_skills": len(SKILLS),
        "skill_categories": list(SKILL_CATEGORIES.keys())
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_contact() -> CallToolResult:
    """Get contact information."""
    result = {
        "name": PROFILE["name"],
        "linkedin": PROFILE["contact"]["linkedin"],
        "linkedin_username": PROFILE["contact"]["linkedin_username"],
        "connect_message": "Feel free to connect on LinkedIn to discuss AI, LLMs, and engineering!"
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_education() -> CallToolResult:
    """Get education details."""
    result = {
        "education": PROFILE["education"],
        "highlights": [
            f"Master's degree from {PROFILE['education']['university']}",
            "Strong foundation in computer science and engineering principles",
            "Research experience in ML and AI systems"
        ]
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_job_titles() -> CallToolResult:
    """Get suitable job titles."""
    result = {
        "primary_titles": PROFILE["job_titles"],
        "alternative_titles": [
            "ML Platform Engineer",
            "AI/ML Infrastructure Engineer",
            "Senior Software Engineer - AI",
            "LLM Operations Engineer",
            "AI Tooling Engineer"
        ]
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_all_skills(include_keywords: bool = False) -> CallToolResult:
    """Get all skills."""
    skills_list = []
    for skill_id, skill_data in SKILLS.items():
        skill_info = {
            "id": skill_id,
            "name": skill_data["name"],
            "description": skill_data["description"]
        }
        if include_keywords:
            skill_info["keywords"] = skill_data["keywords"]
        skills_list.append(skill_info)
    
    result = {
        "total": len(skills_list),
        "skills": skills_list
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_skill(skill_id: str) -> CallToolResult:
    """Get a specific skill."""
    if skill_id not in SKILLS:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Skill '{skill_id}' not found. Available skills: {list(SKILLS.keys())}")]
        )
    
    skill = SKILLS[skill_id]
    result = {
        "id": skill_id,
        "name": skill["name"],
        "description": skill["description"],
        "keywords": skill["keywords"]
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_skills_by_category(category: str) -> CallToolResult:
    """Get skills by category."""
    if category not in SKILL_CATEGORIES:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Category '{category}' not found. Available: {list(SKILL_CATEGORIES.keys())}")]
        )
    
    category_names = {
        "ai_ml": "AI & Machine Learning",
        "infrastructure": "Infrastructure & Cloud",
        "backend": "Backend & Data Systems",
        "security_ops": "Security & Operations",
        "community": "Community & Open Source"
    }
    
    skill_ids = SKILL_CATEGORIES[category]
    skills_list = []
    for skill_id in skill_ids:
        skill = SKILLS[skill_id]
        skills_list.append({
            "id": skill_id,
            "name": skill["name"],
            "description": skill["description"]
        })
    
    result = {
        "category": category,
        "category_name": category_names.get(category, category),
        "count": len(skills_list),
        "skills": skills_list
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def search_skills(query: str) -> CallToolResult:
    """Search skills by keyword."""
    query_lower = query.lower()
    matches = []
    
    for skill_id, skill_data in SKILLS.items():
        # Search in name, description, and keywords
        searchable = (
            skill_data["name"].lower() + " " +
            skill_data["description"].lower() + " " +
            " ".join(skill_data["keywords"]).lower()
        )
        
        if query_lower in searchable:
            matches.append({
                "id": skill_id,
                "name": skill_data["name"],
                "description": skill_data["description"],
                "matching_keywords": [k for k in skill_data["keywords"] if query_lower in k.lower()]
            })
    
    result = {
        "query": query,
        "matches": len(matches),
        "skills": matches
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_summary() -> CallToolResult:
    """Get professional summary."""
    result = {
        "summary": PROFILE["summary"],
        "key_strengths": [
            "End-to-end LLM pipeline development",
            "Agentic AI system design",
            "MCP server development",
            "Cloud-native AI infrastructure",
            "Production ML systems"
        ],
        "education": f"Master's from {PROFILE['education']['university']}"
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


async def get_technologies() -> CallToolResult:
    """Get all technologies and tools."""
    all_keywords = set()
    for skill_data in SKILLS.values():
        all_keywords.update(skill_data["keywords"])
    
    # Categorize technologies
    languages = ["Python", "Go", "Java", "TypeScript"]
    cloud = ["AWS", "Azure", "GCP", "Kubernetes", "containers"]
    data = ["Kafka", "Elasticsearch", "Redis", "PostgreSQL", "ETL", "streaming"]
    ai_ml = ["LLM", "ML models", "RAG", "tokenization", "AI agents"]
    devops = ["Jenkins", "GitLab", "Azure DevOps", "Spinnaker", "CI/CD"]
    monitoring = ["Prometheus", "Grafana", "Kibana", "Dynatrace"]
    
    result = {
        "languages": languages,
        "cloud_platforms": cloud,
        "data_technologies": data,
        "ai_ml_technologies": ai_ml,
        "devops_tools": devops,
        "monitoring_tools": monitoring,
        "all_keywords": sorted(list(all_keywords))
    }
    return CallToolResult(
        content=[TextContent(type="text", text=json.dumps(result, indent=2))]
    )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """Main entry point for the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="madhavi-profile",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )


if __name__ == "__main__":
    asyncio.run(main())

