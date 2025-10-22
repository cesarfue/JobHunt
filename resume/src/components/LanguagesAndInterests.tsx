import type { Language } from "../types/ResumeTypes";

export const LanguagesAndInterests = ({
  languages,
  interests,
}: {
  languages: Language[];
  interests: string[];
}) => (
  <section>
    <h2>Langues & Intérêts</h2>
    <div>
      <div>
        <h3>Langues</h3>
        <ul>
          {languages.map((lang, i) => (
            <li key={i} className="language-item">
              <span className="language-name">{lang.language}</span>:{" "}
              {lang.fluency}
            </li>
          ))}
        </ul>
      </div>
      <div>
        <h3>Centres d'intérêt</h3>
        <ul>
          {interests.map((interest, i) => (
            <li key={i}>{interest}</li>
          ))}
        </ul>
      </div>
    </div>
  </section>
);
