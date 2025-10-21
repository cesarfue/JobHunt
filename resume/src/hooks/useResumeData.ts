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
      .then((data) => {
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
