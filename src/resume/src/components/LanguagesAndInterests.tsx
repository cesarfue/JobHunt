import type { Language } from "../types/ResumeTypes";

export const LanguagesAndInterests = ({
  languages,
  interests,
}: {
  languages: Language[];
  interests: string[];
}) => (
  <section>
    <h2>Langues</h2>
    <div>
      {languages.map((lang, i) => (
        <p key={i}>
          <span className="list-name">{lang.language}</span> : {lang.fluency}
        </p>
      ))}
    </div>
    <div>
      <h2>Intérêts</h2>
      <ul>
        {interests.map((interest, i) => (
          <li key={i}>{interest}</li>
        ))}
      </ul>
    </div>
  </section>
);
