import type { HardSkills } from "../types/ResumeTypes";

export const Skills = ({
  hard_skills,
  soft_skills,
}: {
  hard_skills: HardSkills;
  soft_skills: Array<
    string | { name: string; score?: number; mandatory?: boolean }
  >;
}) => (
  <section>
    <h2>Compétences techniques</h2>

    <div className="skills-container">
      <div>
        <p>
          <span className="list-name">Principales</span> :{" "}
          {hard_skills.main.map((skill, i) => (
            <span key={i}>
              {typeof skill === "string" ? skill : skill.name}
              {i < hard_skills.main.length - 1 ? ", " : ""}
            </span>
          ))}
        </p>
      </div>

      <div>
        <p>
          <span className="list-name">Secondaires</span> :{" "}
          {hard_skills.secondary.map((skill, i) => (
            <span key={i}>
              {typeof skill === "string" ? skill : skill.name}
              {i < hard_skills.secondary.length - 1 ? ", " : ""}
            </span>
          ))}
        </p>
      </div>

      <div>
        <p>
          <span className="list-name">Environnements et outils</span> :{" "}
          {hard_skills.environment_and_tools.map((skill, i) => (
            <span key={i}>
              {typeof skill === "string" ? skill : skill.name}
              {i < hard_skills.environment_and_tools.length - 1 ? ", " : ""}
            </span>
          ))}
        </p>
      </div>

      <div>
        <h2>Soft Skills</h2>
        <ul>
          {soft_skills.map((skill, i) => (
            <li key={i}>{typeof skill === "string" ? skill : skill.name}</li>
          ))}
        </ul>
      </div>
    </div>
  </section>
);
