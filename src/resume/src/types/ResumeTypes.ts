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
  score?: number;
  mandatory?: boolean;
}

export interface Language {
  language: string;
  fluency: string;
  score?: number;
  mandatory?: boolean;
}

export interface Project {
  language: string;
  description: string;
  score?: number;
  mandatory?: boolean;
}

export interface Education {
  title: string;
  location: string;
  time_period: string;
  description: string;
  score?: number;
  mandatory?: boolean;
}

export interface WorkExperience {
  title: string;
  location: string;
  time_period: string;
  description: string;
  score?: number;
  mandatory?: boolean;
}

export interface HardSkills {
  main: Array<string | { name: string; score?: number; mandatory?: boolean }>;
  secondary: Array<
    string | { name: string; score?: number; mandatory?: boolean }
  >;
  environment_and_tools: Array<
    string | { name: string; score?: number; mandatory?: boolean }
  >;
}

export interface ResumeData {
  basics: Basics;
  summary: string | { text: string; score?: number; mandatory?: boolean };
  hard_skills: HardSkills;
  soft_skills: Array<
    string | { name: string; score?: number; mandatory?: boolean }
  >;
  languages: Language[];
  interests: Array<
    string | { name: string; score?: number; mandatory?: boolean }
  >;
  projects: Project[];
  education: Education[];
  work_experience: WorkExperience[];
}
