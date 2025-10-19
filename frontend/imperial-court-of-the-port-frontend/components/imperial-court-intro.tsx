"use client";
import React, { useState } from "react";

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
}

interface DeploymentCardProps {
  title: string;
  description: string;
  features: string[];
}

interface ArchitectureItemProps {
  title: string;
  description: string;
}

interface TechBadgeProps {
  text: string;
}

interface CapabilityCardProps {
  icon: string;
  title: string;
  points: string[];
}

export default function ImperialCourtIntro(): JSX.Element {
  const [isImageModalOpen, setIsImageModalOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-12 md:py-20 max-w-7xl">
        {/* Hero Section */}
        <header className="bg-white rounded-2xl shadow-sm p-8 md:p-16 mb-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
              Imperial Court
            </h1>
            <p className="text-xl md:text-2xl text-purple-600 font-semibold mb-6">
              AI-Powered Port Operations Intelligence System
            </p>
            <p className="text-base md:text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
              Revolutionary multi-agent AI platform leveraging CrewAI for
              intelligent incident management, real-time operational analysis,
              and automated decision support in port and maritime operations.
            </p>
          </div>
          <div className="container mx-auto px-4 py-12 md:py-20 max-w-7xl">
            <h1 className="text-3xl sm:text-3xl md:text-3xl font-extrabold text-gray-900 mb-6 sm:mb-8 text-center tracking-tight">
              What Our Agents Are{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-purple-500">
                Orchestrating
              </span>{" "}
              Behind the Scenes
            </h1>

            <p className="text-center text-gray-600 mb-10 text-lg max-w-3xl mx-auto">
              The Imperial Court of the Port utilizes multiple specialized
              agents, each executing a crucial role in our incident management
              protocol—achieving unprecedented speed and precision.
            </p>

            <div className="w-full flex justify-center">
              <iframe
                src="https://drive.google.com/file/d/1OM2g1TBI4ZltZKz0G4gCGcGhwIPXvhom/preview"
                width="640"
                height="480"
                allow="autoplay"
              ></iframe>
            </div>
          </div>
          {/* Key Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon="🤖"
              title="Multi-Agent Intelligence"
              description="8 specialized AI agents working in concert: Intelligence gathering, technical analysis, business impact assessment, and escalation management."
            />
            <FeatureCard
              icon="⚡"
              title="Real-Time Processing"
              description="Celery-powered background job processing with Redis for instant incident analysis and response coordination."
            />
            <FeatureCard
              icon="📊"
              title="Database Intelligence"
              description="Comprehensive operational data access across vessels, containers, EDI messages, and API events for evidence-based decisions."
            />
            <FeatureCard
              icon="🎯"
              title="RAG-Enhanced Analysis"
              description="Qdrant vector search with OpenAI embeddings for historical case retrieval and knowledge base integration."
            />
            <FeatureCard
              icon="📞"
              title="Smart Escalation"
              description="Automated contact selection and escalation paths based on incident classification, severity, and system health metrics."
            />
            <FeatureCard
              icon="🔐"
              title="Enterprise Security"
              description="Azure DDoS protection, Microsoft Defender integration, and comprehensive monitoring with Azure Sentinel."
            />
          </div>
        </header>

        {/* Deployment Flexibility */}
        <section className="bg-white rounded-2xl shadow-sm p-8 md:p-16 mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 text-center mb-4">
            Flexible Deployment Options
          </h2>
          <p className="text-center text-gray-600 mb-10 max-w-3xl mx-auto">
            Our codebase can be containerised to enable seamless deployment
            across multiple environments. Choose the infrastructure that best
            fits your organization's needs. We are recommending a hybrid
            solution.
          </p>
         
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
            <DeploymentCard
              title="On-Premises"
              description="Full control and data sovereignty. Deploy within your own infrastructure for maximum security and compliance."
              features={[
                "Complete data control",
                "Customizable security",
                "No cloud dependencies",
              ]}
            />
            <DeploymentCard
              title="Cloud (Azure)"
              description="Scalable cloud deployment leveraging Azure services for high availability and global reach."
              features={[
                "Auto-scaling",
                "Global distribution",
                "Managed services",
              ]}
            />
            <DeploymentCard
              title="Hybrid Solution"
              description="Best of both worlds - critical data on-premises with cloud burst capability for peak loads."
              features={["Cost optimization", "Resilience", "Flexibility"]}
            />
          </div>

          <div className="bg-purple-50 rounded-xl p-6 border border-purple-100">
            <h4 className="font-semibold text-gray-900 mb-3 text-center text-lg">
              Multi-Cloud Ready
            </h4>
            <p className="text-sm text-gray-600 text-center mb-4">
              Our containerized architecture supports deployment across multiple
              cloud providers for enhanced resilience and cost optimization.
            </p>
            <div className="flex flex-wrap justify-center gap-3">
              <span className="bg-white px-4 py-2 rounded-lg text-sm font-medium text-gray-700 shadow-sm border border-gray-200">
                Microsoft Azure
              </span>
              <span className="bg-white px-4 py-2 rounded-lg text-sm font-medium text-gray-700 shadow-sm border border-gray-200">
                AWS
              </span>
              <span className="bg-white px-4 py-2 rounded-lg text-sm font-medium text-gray-700 shadow-sm border border-gray-200">
                Google Cloud
              </span>
              <span className="bg-white px-4 py-2 rounded-lg text-sm font-medium text-gray-700 shadow-sm border border-gray-200">
                Private Data Centers
              </span>
            </div>
            <h4 className="font-semibold text-gray-900 mb-3 text-center text-lg p-4">
              Example Architecture on Azure
            </h4>
            <img src="/psacodesprint.drawio.png" alt="Azure Architecture overview" className="w-full h-auto mb-10 rounded-lg shadow-md"/>
            <p className="text-slate-800">
              Imperial Court operates on a robust, Azure-native architecture
              designed for enterprise-grade reliability, security, and
              scalability through intelligent orchestration of various Azure
              services. The process begins with Incident Submission & Security,
              where reports enter via a containerized Eureka Client App hosted
              on Azure Functions, secured by Azure DDoS Protection and Azure WAF
              for initial screening. Next, in Intelligent Job Orchestration,
              Azure Functions create database job entries that trigger Azure
              Machine Learning to host the Imperial Court Agentic Framework. AI
              agents analyze the incidents using CrewAI, utilizing RAG
              capabilities by accessing operational data stored in Cosmos DB and
              PostgreSQL. This leads to Multi-Agent Analysis, where specialized
              AI agents execute comprehensive analysis—covering evidence,
              technical investigation, business impact, and communication
              strategy—with results stored in Blob Storage and job status synced
              to Cosmos DB. Subsequently, Automated Escalation & Notification is
              handled as Azure Functions trigger timely notifications via Event
              Grid, and Azure Communication Services push information to
              stakeholders via email or other formats. Finally, External
              Integration & Monitoring is achieved through Webhooks for
              application integration, while Azure Logs, Azure Sentinel, and
              Microsoft Defender provide comprehensive monitoring and logging
              for full traceability and accountability.
            </p>
          </div>
        </section>
        {/* Architecture Highlights */}
        <section className="bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl shadow-sm p-8 md:p-16 mb-8 text-white">
          <h2 className="text-3xl md:text-4xl font-bold text-center mb-8">
            Enterprise-Grade Architecture
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <ArchitectureItem
              title="Scalability"
              description="Backend powered by Celery for workload distribution. Cloud scaling and load balancing for on-demand capacity."
            />
            <ArchitectureItem
              title="High Availability"
              description="Support for high-volume workloads with automatic failover and redundancy across multiple availability zones."
            />
            <ArchitectureItem
              title="Security"
              description="Minimized disruption to operations with Azure DDoS protection, Microsoft Defender, and comprehensive logging."
            />
            <ArchitectureItem
              title="Cost Resilience"
              description="Hybrid deployment ensures high availability while optimizing costs through intelligent resource allocation."
            />
          </div>

          <div className="mt-10 bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20">
            <h4 className="font-semibold text-xl mb-4 text-center">
              Core Technologies
            </h4>
            <div className="flex flex-wrap justify-center gap-3">
              <TechBadge text="Python / FastAPI" />
              <TechBadge text="CrewAI Agents" />
              <TechBadge text="PostgreSQL (Supabase)" />
              <TechBadge text="Redis Cloud" />
              <TechBadge text="Celery" />
              <TechBadge text="Qdrant Vector DB" />
              <TechBadge text="OpenAI Embeddings" />
              <TechBadge text="Azure Services" />
              <TechBadge text="Docker" />
              <TechBadge text="Next.js Frontend" />
            </div>
          </div>
        </section>

        {/* System Architecture & Tech Stack */}
        <section className="bg-white rounded-2xl shadow-sm p-8 md:p-16 mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 text-center mb-4">
            System Architecture & Tech Stack
          </h2>
          <p className="text-center text-gray-600 mb-6 max-w-3xl mx-auto">
            The diagram below illustrates the high-level system architecture and
            the major components used by Imperial Court. It highlights the
            interaction between the frontend, backend services, databases,
            vector store, message transport, and background worker cluster.
          </p>

          <div className="flex flex-col lg:flex-row items-center gap-8">
            <div className="w-full lg:w-2/3">
              <img
                src="/eureka_arch.png"
                alt="Deployment Architecture overview"
                className="w-full h-auto rounded-lg shadow-md cursor-pointer hover:shadow-lg transition-shadow duration-300"
                onClick={() => setIsImageModalOpen(true)}
                title="Click to view larger image"
              />
            </div>

            <div className="w-full lg:w-1/3">
              <h3 className="text-xl font-semibold text-gray-900 mb-3">
                Components
              </h3>
              <ul className="list-none space-y-3 text-sm text-gray-700">
                <li>
                  <strong>Next.js (Frontend):</strong> User interface for
                  incident submission, job tracking, and results visualization.
                </li>
                <li>
                  <strong>FastAPI (Backend):</strong> Primary API layer that
                  accepts submissions, orchestrates jobs, and exposes agent
                  tools.
                </li>
                <li>
                  <strong>Supabase / PostgreSQL:</strong> Relational datastore
                  for job records, case logs, and operational data.
                </li>
                <li>
                  <strong>Qdrant (Vector DB):</strong> Vector store used for RAG
                  and similarity search of past incidents and knowledge base
                  content.
                </li>
                <li>
                  <strong>Redis:</strong> Message transport for Celery and
                  ephemeral caching needs.
                </li>
                <li>
                  <strong>Celery & Worker Cluster:</strong> Background job
                  workers that execute multi-agent analysis at scale.
                </li>
                <li>
                  <strong>OpenAI / Embeddings:</strong> Embedding model used to
                  index knowledge base and inform RAG searches.
                </li>
                <li>
                  <strong>CrewAI Agents:</strong> Multi-agent orchestration
                  layer responsible for staged analysis, evidence collection,
                  and escalation generation.
                </li>
                <li>
                  <strong>Qdrant ↔ Supabase Integration:</strong> Hybrid
                  retrieval pattern where structured evidence is stored in
                  Postgres while semantic vectors live in Qdrant.
                </li>
                <li>
                  <strong>Observability:</strong> Centralized logs and
                  monitoring (e.g., Cloud / Azure logs, alerts) for traceability
                  and incident analysis.
                </li>
              </ul>

              <h4 className="mt-6 font-semibold text-gray-900">
                Why this design?
              </h4>
              <p className="text-sm text-gray-700">
                The architecture separates concerns: fast API responses and job
                orchestration are handled by FastAPI, long-running analysis
                lives in Celery workers, and RAG searches use a vector index for
                speed and relevance. This enables horizontally scalable analysis
                workloads while keeping the primary API responsive.
              </p>
            </div>
          </div>
        </section>

        {/* Key Capabilities */}
        <section className="bg-white rounded-2xl shadow-sm p-8 md:p-16 mb-8">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 text-center mb-8">
            Intelligent Capabilities
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <CapabilityCard
              icon="🔍"
              title="Comprehensive Investigation"
              points={[
                "Evidence-based analysis using real operational data",
                "Pattern recognition across historical incidents",
                "Multi-domain validation (technical, business, communication)",
                "Root cause analysis with database correlation",
              ]}
            />
            <CapabilityCard
              icon="⚙️"
              title="Automated Escalation"
              points={[
                "Intelligent contact selection based on incident type",
                "Priority-based ticket generation (P1/P2/P3)",
                "Timeline-driven escalation pathways",
                "Stakeholder notification management",
              ]}
            />
            <CapabilityCard
              icon="📈"
              title="Operational Intelligence"
              points={[
                "Real-time system health monitoring",
                "Container and vessel tracking",
                "EDI/API performance analysis",
                "Business impact quantification",
              ]}
            />
            <CapabilityCard
              icon="🎓"
              title="Learning System"
              points={[
                "Historical case pattern analysis",
                "Proven solution recommendations",
                "Knowledge base integration",
                "Continuous improvement from past incidents",
              ]}
            />
          </div>
        </section>
        <section className='bg-gradient-to-br from-purple-600 to-indigo-600 rounded-2xl shadow-sm p-8 md:p-16 mb-8 text-white flex items-center flex-col '>
          <h2 className="text-xl md:text-xl font-bold text-center mb-8">Our Solution Design Philosophy:</h2>
          <p className="text-xl md:text-xl text-center mb-8 italic">
            Build with performance, scalability and user needs in mind. <br/> Think long-term and consider the infrastructure as well as the AI solution. An AI solution on a shaky infrastructure crumbles on heavy loads and while cloud can help to improve scalability, we must avert the risk of a single-point of failure by using a hybrid solution.
          </p>
        </section>
      </div>

      {/* Image Modal */}
      {isImageModalOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
          onClick={() => setIsImageModalOpen(false)}
        >
          <div className="relative max-w-7xl max-h-full">
            <button
              onClick={() => setIsImageModalOpen(false)}
              className="absolute top-4 right-4 text-white bg-black bg-opacity-50 rounded-full p-2 hover:bg-opacity-75 transition-all duration-200 z-10"
              aria-label="Close modal"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
            <img
              src="/eureka_arch.png"
              alt="Deployment Architecture overview - Expanded view"
              className="max-w-full max-h-full object-contain rounded-lg"
              onClick={(e) => e.stopPropagation()}
            />
          </div>
        </div>
      )}
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: FeatureCardProps): JSX.Element {
  return (
    <div className="bg-gray-50 rounded-xl p-6 border border-gray-200 hover:border-purple-200 hover:shadow-md transition-all duration-300">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-xl font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-gray-600 text-sm leading-relaxed">{description}</p>
    </div>
  );
}

function DeploymentCard({
  title,
  description,
  features,
}: DeploymentCardProps): JSX.Element {
  return (
    <div className="bg-gradient-to-br from-purple-600 to-indigo-600 rounded-xl p-6 text-white hover:shadow-lg transition-all duration-300">
      <h3 className="text-2xl font-bold mb-3">{title}</h3>
      <p className="text-sm mb-4 text-white/90">{description}</p>
      <ul className="space-y-2">
        {features.map((feature: string, idx: number) => (
          <li key={idx} className="flex items-start text-sm">
            <span className="mr-2">✓</span>
            <span>{feature}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function ArchitectureItem({
  title,
  description,
}: ArchitectureItemProps): JSX.Element {
  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 border border-white/20 hover:bg-white/15 transition-all duration-300">
      <h4 className="text-xl font-bold mb-3">{title}</h4>
      <p className="text-sm text-white/90 leading-relaxed">{description}</p>
    </div>
  );
}

function TechBadge({ text }: TechBadgeProps): JSX.Element {
  return (
    <span className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-sm font-medium border border-white/30">
      {text}
    </span>
  );
}

function CapabilityCard({
  icon,
  title,
  points,
}: CapabilityCardProps): JSX.Element {
  return (
    <div className="bg-gray-50 rounded-xl p-6 border border-gray-200 hover:border-purple-200 transition-all duration-300">
      <div className="flex items-center mb-4">
        <span className="text-3xl mr-3">{icon}</span>
        <h3 className="text-xl font-bold text-gray-900">{title}</h3>
      </div>
      <ul className="space-y-2">
        {points.map((point: string, idx: number) => (
          <li key={idx} className="flex items-start text-sm text-gray-700">
            <span className="text-purple-600 mr-2 font-bold">•</span>
            <span>{point}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
