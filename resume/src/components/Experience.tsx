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
          <p>{exp.title}</p>
          <p>
            {exp.location} • {exp.time_period}
          </p>
          <p>{exp.description}</p>
        </div>
      ))}
    </div>
  </section>
);
