import { useEffect, useState } from "react";
import type { ResumeData } from "../types/ResumeTypes";

export function useResumeData() {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // List of possible override files to check
    const overrideFiles = [
      "hard_skills",
      "soft_skills",
      "summary",
      "projects",
      "education",
      "work_experience",
      "languages",
      "interests",
      "basics",
    ];

    // First, fetch the base resume.json
    fetch("/resume.json")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load resume data");
        return res.json();
      })
      .then(async (data: ResumeData) => {
        // Try to fetch each override file
        const overridePromises = overrideFiles.map(async (fileName) => {
          try {
            const res = await fetch(`/resume_overrides/${fileName}.json`);
            if (res.ok) {
              const overrideData = await res.json();
              console.log(`✅ Loaded override: ${fileName}.json`);
              return { fileName, data: overrideData };
            }
          } catch (err) {
            // File doesn't exist, that's okay
            return null;
          }
          return null;
        });

        // Wait for all override fetches to complete
        const overrides = await Promise.all(overridePromises);

        // Merge overrides into the base data
        overrides.forEach((override) => {
          if (override) {
            const { fileName, data: overrideData } = override;
            // Replace the field in resumeData with the override data
            (data as any)[fileName] = overrideData;
            console.log(`✅ Merged ${fileName} from override`);
          }
        });

        setResumeData(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { resumeData, loading, error };
}
