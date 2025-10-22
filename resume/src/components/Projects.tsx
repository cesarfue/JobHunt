import type { Project } from "../types/ResumeTypes";

export const Projects = ({ projects }: { projects: Project[] }) => (
  <section>
    <h2>Projets personnels</h2>
    <ul>
      {projects.map((project, i) => (
        <li key={i} className="project-entry">
          <span className="list-name">{project.language}</span> :{" "}
          {project.description}
        </li>
      ))}
    </ul>
  </section>
);
