import type { WorkExperience } from "../types/ResumeTypes";

export const Experience = ({
  work_experience,
}: {
  work_experience: WorkExperience[];
}) => (
  <section>
    <h2>Expériences professionnelles</h2>
    <div>
      {work_experience.map((exp, i) => (
        <div key={i} className="entry">
          <p className="entry-title">{exp.title}</p>
          <p className="entry-meta">
            {exp.location} • {exp.time_period}
          </p>
          <p className="entry-description">{exp.description}</p>
        </div>
      ))}
    </div>
  </section>
);
