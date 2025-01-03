import type { Genre, MoodTheme, Tag, AnalysisResponse } from "../types/api";

export const transformGenre = (data: any): Genre => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || "",
  confidence: Number(data.confidence) || 0,
});

export const transformMoodTheme = (data: any): MoodTheme => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || "",
  confidence: Number(data.confidence) || 0,
  category: data.category?.toLowerCase() === "mood" ? "mood" : "theme",
});

export const transformTag = (data: any): Tag => ({
  id: data.id || String(Math.random()),
  name: data.name?.toLowerCase() || "",
  confidence: Number(data.confidence) || 0,
  category: data.category?.toLowerCase() || "general",
});

export const transformAnalysisResponse = (data: any): AnalysisResponse => {
  // Transform genres from nested structure
  const genres = data.genres?.discogs400
    ? Object.entries(data.genres.discogs400).flatMap(
        ([category, subGenres]) => {
          if (typeof subGenres === "object") {
            return Object.entries(subGenres).map(([name, confidence]) => ({
              id: String(Math.random()),
              name,
              confidence: confidence as number,
            }));
          }
          return [];
        }
      )
    : [];

  // Transform mood themes from nested structure
  const moodThemes = data.moodThemes
    ? [
        ...Object.entries(data.moodThemes.general || {}).map(
          ([name, confidence]) => ({
            id: String(Math.random()),
            name,
            confidence: confidence as number,
            category: "mood" as "mood",
          })
        ),
        ...Object.entries(data.moodThemes.track_level || {}).map(
          ([name, confidence]) => ({
            id: String(Math.random()),
            name,
            confidence: confidence as number,
            category: "theme" as "theme",
          })
        ),
      ]
    : [];

  // Transform tags from nested structure
  const tags = [
    ...Object.entries(data.tags?.mtg_jamendo_general || {}).map(
      ([name, confidence]) => ({
        id: String(Math.random()),
        name,
        confidence: confidence as number,
        category: "general",
      })
    ),
    ...Object.entries(data.tags?.mtg_jamendo_track || {}).map(
      ([name, confidence]) => ({
        id: String(Math.random()),
        name,
        confidence: confidence as number,
        category: "track",
      })
    ),
  ];

  console.log("Mood themes data:", data.moodThemes);
  console.log("Transformed mood themes:", moodThemes);

  return {
    success: Boolean(data.success),
    genres,
    moodThemes,
    tags,
  };
};
