import { SpotifySearchResult } from "./spotify";

export interface StepContentProps {
  step: number;
  onNext: () => void;
  onBack: () => void;
  onSearchComplete: (results: SpotifySearchResult[]) => void;
  results: SpotifySearchResult[];
}

export interface GenreSelectionStepProps {
  onNext: (results: SpotifySearchResult[]) => void;
  onBack: () => void;
}

export interface ReportStepProps {
  onBack: () => void;
  results: SpotifySearchResult[];
}
