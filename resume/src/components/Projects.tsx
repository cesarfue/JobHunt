import type { Project } from "../types/ResumeTypes";

export const Projects = ({ projects }: { projects: Project[] }) => (
  <section>
    <h2>Projets personnels</h2>
    <div>
      {projects.map((project, i) => (
        <div key={i} className="project-entry">
          <p className="project-language">{project.language}</p>
          <p className="project-description">{project.description}</p>
        </div>
      ))}
    </div>
  </section>
);
