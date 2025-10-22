import type { HardSkills } from "../types/ResumeTypes";

export const Skills = ({
  hard_skills,
  soft_skills,
}: {
  hard_skills: HardSkills;
  soft_skills: string[];
}) => (
  <section>
    <h2>Compétences</h2>

    <div className="skill-list">
      <h3>Principales</h3>
      <div>
        {hard_skills.main.map((skill, i) => (
          <span key={i} className="skill-badge">
            {skill}
          </span>
        ))}
      </div>
    </div>

    <div className="skill-list">
      <h3>Secondaires</h3>
      <div>
        {hard_skills.secondary.map((skill, i) => (
          <span key={i} className="skill-badge">
            {skill}
          </span>
        ))}
      </div>
    </div>

    <div className="skill-list">
      <h3>Outils</h3>
      <div>
        {hard_skills.environmnent_and_tools.map((skill, i) => (
          <span key={i} className="skill-badge">
            {skill}
          </span>
        ))}
      </div>
    </div>

    <div>
      <h3>Soft Skills</h3>
      <ul>
        {soft_skills.map((skill, i) => (
          <li key={i}>{skill}</li>
        ))}
      </ul>
    </div>
  </section>
);
