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

    <div>
      <h3>Compétences techniques principales</h3>
      <div>
        {hard_skills.main.map((skill, i) => (
          <span key={i}>{skill}</span>
        ))}
      </div>
    </div>

    <div>
      <h3>Compétences secondaires</h3>
      <div>
        {hard_skills.secondary.map((skill, i) => (
          <span key={i}>{skill}</span>
        ))}
      </div>
    </div>

    <div>
      <h3>Environnement et outils</h3>
      <div>
        {hard_skills.environmnent_and_tools.map((skill, i) => (
          <span key={i}>{skill}</span>
        ))}
      </div>
    </div>

    <div>
      <h3>Compétences transversales</h3>
      <ul>
        {soft_skills.map((skill, i) => (
          <li key={i}>{skill}</li>
        ))}
      </ul>
    </div>
  </section>
);
