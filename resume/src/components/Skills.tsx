import type { HardSkills } from "../types/ResumeTypes";

export const Skills = ({
  hard_skills,
  soft_skills,
}: {
  hard_skills: HardSkills;
  soft_skills: string[];
}) => (
  <section>
    <h2>Compétences techniques</h2>

    <div>
      {hard_skills.main.map((skill, i) => (
        <p key={i}>
          <span className="list-name">Principales</span> : {skill}
        </p>
      ))}
    </div>

    <div>
      {hard_skills.secondary.map((skill, i) => (
        <p key={i}>
          <span className="list-name">Secondaires</span> : {skill}
        </p>
      ))}
    </div>

    <div>
      {hard_skills.environmnent_and_tools.map((skill, i) => (
        <p key={i}>
          <span className="list-name">Environnements et Outils</span> : {skill}
        </p>
      ))}
    </div>

    <div>
      <h2>Soft Skills</h2>
      <ul>
        {soft_skills.map((skill, i) => (
          <li key={i}>{skill}</li>
        ))}
      </ul>
    </div>
  </section>
);
