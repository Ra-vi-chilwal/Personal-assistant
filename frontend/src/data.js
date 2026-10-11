export const profile = {
  name: "Ravindar Singh Chilwal",
  role: "Full Stack AI Engineer",
  location: "Gurugram, India",
  email: "work.ravindarchilwal@gmail.com",
  linkedin: "https://www.linkedin.com/in/ravindar-singh-chilwal30",
  github: "https://github.com/Ra-vi-chilwal",
  resume: "/Ravindar_Singh_Chilwal_Resume.pdf",
  tagline:
    "I build scalable web platforms and ship Generative AI into production: RAG chatbots, LLM automation and agentic workflows.",
  about: [
    "Full Stack AI Engineer with 5+ years of professional experience building scalable web applications with React, Node.js, MongoDB, PostgreSQL and AWS, and integrating Generative AI into real products.",
    "Hands-on with Python and FastAPI services, vector search (pgvector, Pinecone), n8n workflow automation, queues (Bull/Redis, Kafka) and Dockerized deployments on AWS. I have also led small teams and delivered business-driven results.",
  ],
};

export const stats = [
  { value: "5+", label: "Years of experience" },
  { value: "40%", label: "Faster app load time" },
  { value: "2", label: "ISO 27001 compliant solutions" },
  { value: "5+", label: "Client sites & dashboards" },
];

export const skills = [
  { group: "Generative AI & ML", items: ["LLM Integration", "RAG", "LangChain", "Agentic Workflows", "Prompt Engineering", "Fine-tuning", "NLP", "Sentiment Analysis", "pgvector", "Pinecone"] },
  { group: "Full Stack", items: ["React.js", "Node.js", "Express.js", "FastAPI", "REST APIs", "Microservices", "HTML", "CSS", "JavaScript", "Python"] },
  { group: "Data & Messaging", items: ["MongoDB", "PostgreSQL", "Redis", "DynamoDB", "Kafka", "RabbitMQ", "Bull Queue", "SQL"] },
  { group: "Cloud & Automation", items: ["AWS EC2", "ECR", "S3", "CloudFront", "Glue", "Athena", "EMR", "Docker", "Nginx", "n8n", "GitHub"] },
  { group: "Also", items: ["Salesforce Apex", "jsforce", "System Design", "DSA", "Jira"] },
];

export const experience = [
  {
    title: "Senior Full Stack Developer",
    company: "360degreeCloud",
    place: "Noida, UP",
    period: "Aug 2026 – Present",
    points: [
      "Building a Salesforce data backup, restoration and archival platform that moves Salesforce data to AWS using Apex, jsforce/Node.js middleware, Glue, Athena, EMR and DynamoDB.",
      "Designed microservices, containerized them with Docker, managed images in ECR and deployed on EC2.",
      "Building agentic AI workflows to automate project processes, using Claude, Cursor and Grok to accelerate delivery.",
    ],
  },
  {
    title: "Full Stack Developer (AI)",
    company: "Adglobal360",
    place: "Gurugram, Haryana",
    period: "Apr 2024 – Aug 2026",
    points: [
      "Built a GenAI Business Insights Chatbot (RAG) with LangChain, FastAPI and PostgreSQL/pgvector for real-time, client-wise analytics.",
      "Built an NLP sentiment-analysis and auto-reply pipeline for Google Business reviews, cutting manual response effort across locations.",
      "Shipped a multi-location Google Business automation platform and two ISO 27001-compliant solutions; improved load speed by 40%.",
      "Re-architected post creation to an atomic design (unique compound index + Bull/Redis queue, 202 Accepted), eliminating duplicate posts.",
    ],
  },
  {
    title: "Software Engineer, Team Lead",
    company: "Solis Technologies",
    place: "Gurugram, Haryana",
    period: "Apr 2023 – Mar 2024",
    points: [
      "Led a small team: task delegation and code reviews for on-time delivery across client projects.",
      "Designed and built 5 professional websites and client dashboards with Node.js and PHP; worked directly with international clients.",
    ],
  },
  {
    title: "Full Stack Developer",
    company: "DDReg Pharma",
    place: "Gurugram, Haryana",
    period: "Mar 2022 – Apr 2023",
    points: [
      "Built an HRMS (Node.js, React, MongoDB) covering onboarding, attendance, payroll, leave and performance.",
      "Built REST APIs integrating HRMS modules with internal reporting tools.",
    ],
  },
  {
    title: "Front-end Developer Intern",
    company: "Verts Pvt. Ltd.",
    place: "Noida, UP",
    period: "Feb 2021 – Jan 2022",
    points: ["Converted designs into responsive, cross-browser pages, contributing to a 30% increase in user engagement."],
  },
];

export const projects = [
  {
    title: "Business Insights RAG Chatbot",
    desc: "Natural-language Q&A and real-time, client-wise analytics over multi-location business data.",
    tags: ["LangChain", "FastAPI", "pgvector", "PostgreSQL"],
  },
  {
    title: "Review Sentiment & Auto-Reply",
    desc: "Classifies Google Business reviews and uses an LLM to write and post context-aware replies.",
    tags: ["NLP", "LLM", "Node.js", "Automation"],
  },
  {
    title: "Salesforce → AWS Backup Platform",
    desc: "Backup, restore and archival of Salesforce data on AWS, queryable through Athena.",
    tags: ["Apex", "jsforce", "Glue", "Athena", "EMR"],
  },
  {
    title: "Idempotent Post Workflow",
    desc: "Race-condition-free publishing using a compound unique index and a Bull/Redis queue.",
    tags: ["MongoDB", "Redis", "Bull", "System Design"],
  },
  {
    title: "HRMS Platform",
    desc: "Onboarding, attendance, payroll, leave tracking and performance evaluation in one system.",
    tags: ["React", "Node.js", "MongoDB"],
  },
  {
    title: "AI Knowledge Assistant",
    desc: "OpenAI-powered assistant with a React frontend and prompt-engineered, context-aware answers.",
    tags: ["OpenAI", "React", "RAG", "Pinecone"],
  },
];

export const education = {
  school: "Uttarakhand Technical University",
  degree: "B.Tech, Computer Science",
  period: "2016 – 2020",
  note: "GPA 7.8 / 10",
};

export const suggestions = [
  "What does Ravindar do?",
  "Tell me about his AI & RAG experience",
  "What is his tech stack?",
  "Where has he worked?",
];
