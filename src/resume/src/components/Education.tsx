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
        <div key={i} className="entry">
          <p className="entry-title">{edu.title}</p>
          <p className="entry-meta">
            {edu.location} • {edu.time_period}
          </p>
          <p className="entry-description">{edu.description}</p>
        </div>
      ))}
    </div>
  </section>
);
