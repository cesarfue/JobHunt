import { useResumeData } from "./hooks/useResumeData";
import { Header } from "./components/Header";
import { Summary } from "./components/Summary";
import { Skills } from "./components/Skills";
import { Experience } from "./components/Experience";
import { Education } from "./components/Education";
import { Projects } from "./components/Projects";
import { LanguagesAndInterests } from "./components/LanguagesAndInterests";
import Pic from "./assets/photo.jpeg";

export default function App() {
  const { resumeData, error } = useResumeData();

  if (error || !resumeData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-xl text-red-600">
          Erreur: {error || "Données non disponibles"}
        </div>
      </div>
    );
  }

  return (
    <div className="a4-page grid grid-cols-[35%_65%]">
      <div className="left-column space-y-4">
        <img src={Pic} alt="César Fuentes" className="photo" />
        <Summary summary={resumeData.summary} />
        <Skills
          hard_skills={resumeData.hard_skills}
          soft_skills={resumeData.soft_skills}
        />
        <LanguagesAndInterests
          languages={resumeData.languages}
          interests={resumeData.interests}
        />
      </div>

      <div className="right-column space-y-4">
        <Header basics={resumeData.basics} />
        <Projects projects={resumeData.projects} />
        <Experience work_experience={resumeData.work_experience} />
        <Education education={resumeData.education} />
      </div>
    </div>
  );
}
