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
          <h3>{edu.title}</h3>
          <div>
            <span>{edu.location}</span> • {edu.time_period}
          </div>
          <p>{edu.description}</p>
        </div>
      ))}
    </div>
  </section>
);
