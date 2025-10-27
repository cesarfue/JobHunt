import { useEffect, useState } from "react";
import type { ResumeData } from "../types/ResumeTypes";

export function useResumeData() {
  const [resumeData, setResumeData] = useState<ResumeData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/resume.json")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load resume data");
        return res.json();
      })
      .then(async (data: any) => {
        try {
          const overridesRes = await fetch("/overrides.json");
          if (overridesRes.ok) {
            const overrides = await overridesRes.json();

            Object.keys(overrides).forEach((key) => {
              if (data.resume && data.resume[key]) {
                data.resume[key] = overrides[key];
                console.log(`Merged ${key} from override`);
              }
            });
          } else {
            console.log("No overrides.json found, using default resume.json");
          }
        } catch (err) {
          console.log("No overrides.json available, using default resume.json");
        }

        console.log("Final resume data:", data.resume);
        setResumeData(data.resume);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { resumeData, loading, error };
}
