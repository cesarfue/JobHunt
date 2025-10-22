export interface Contact {
  phone: string;
  email: string;
  github: string;
  city: string;
}

export interface Basics {
  name: string;
  image: string;
  contact: Contact;
}

export interface Language {
  language: string;
  fluency: string;
}

export interface Project {
  language: string;
  description: string;
}

export interface Education {
  title: string;
  location: string;
  time_period: string;
  description: string;
}

export interface WorkExperience {
  title: string;
  location: string;
  time_period: string;
  description: string;
}

export interface HardSkills {
  main: string[];
  secondary: string[];
  environmnent_and_tools: string[];
}

export interface ResumeData {
  basics: Basics;
  summary: string;
  hard_skills: HardSkills;
  soft_skills: string[];
  languages: Language[];
  interests: string[];
  projects: Project[];
  education: Education[];
  work_experience: WorkExperience[];
}
