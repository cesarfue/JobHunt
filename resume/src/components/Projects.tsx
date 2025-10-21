import type { Project } from "../types/ResumeTypes";

export const Projects = ({ projects }: { projects: Project[] }) => (
  <section>
    <h2>Projets personnels</h2>
    <div>
      {projects.map((project, i) => (
        <div key={i}>
          <p>{project.language}</p>
          <p>{project.description}</p>
        </div>
      ))}
    </div>
  </section>
);
