export interface SpotifySearchResult {
  genre: string;
  artists: {
    href: string;
    items: any[];
    limit: number;
    next: string | null;
    offset: number;
    previous: string | null;
    total: number;
  };
  playlists: {
    href: string;
    items: any[];
    limit: number;
    next: string | null;
    offset: number;
    previous: string | null;
    total: number;
  };
}
