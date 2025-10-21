import type * as ResumeTypes from "../types/ResumeTypes";

export const Education = ({
  education,
}: {
  education: ResumeTypes.Education[];
}) => (
  <section>
    <h2>Formation</h2>
    <div>
      {education.map((edu, i) => (
        <div key={i}>
          <p>{edu.title}</p>
          <p>
            {edu.location} • {edu.time_period}
          </p>
          <p>{edu.description}</p>
        </div>
      ))}
    </div>
  </section>
);
