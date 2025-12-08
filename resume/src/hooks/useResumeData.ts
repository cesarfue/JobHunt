import { useEffect, useState } from "react";
import type { ResumeData } from "../types/ResumeTypes";

// Deep merge function that merges custom data into base data
function deepMerge<T>(base: T, custom: Partial<T>): T {
  const result = { ...base };

  for (const key in custom) {
    const customValue = custom[key];
    const baseValue = result[key];

    if (customValue === undefined) {
      continue;
    }

    // If both are objects (but not arrays), merge recursively
    if (
      customValue &&
      typeof customValue === "object" &&
      !Array.isArray(customValue) &&
      baseValue &&
      typeof baseValue === "object" &&
      !Array.isArray(baseValue)
    ) {
      result[key] = deepMerge(baseValue, customValue) as T[Extract<keyof T, string>];
    } else {
      // Otherwise, custom value takes priority
      result[key] = customValue as T[Extract<keyof T, string>];
    }
  }

  return result;
}

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
      .then(async (baseData: ResumeData) => {
        try {
          // Try to load custom.json
          const customRes = await fetch("/custom.json");
          if (customRes.ok) {
            const customData = await customRes.json();
            console.log("Loaded custom.json, merging with resume.json");
            const mergedData = deepMerge(baseData, customData);
            setResumeData(mergedData);
          } else {
            console.log("No custom.json found, using resume.json");
            setResumeData(baseData);
          }
        } catch (err) {
          console.log("No custom.json available, using resume.json");
          setResumeData(baseData);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  return { resumeData, loading, error };
}
