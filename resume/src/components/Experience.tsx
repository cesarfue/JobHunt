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
        <div key={i}>
          <h3>{exp.title}</h3>
          <div>
            <span>{exp.location}</span> • {exp.time_period}
          </div>
          <p>{exp.description}</p>
        </div>
      ))}
    </div>
  </section>
);
