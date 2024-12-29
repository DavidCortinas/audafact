from packages.api.audafact_api.api.routes.spotify import search_spotify


async def generate_full_report(analysis_results, user_email):
    # Get genres from analysis
    genres = analysis_results["genres"]
    
    # Search Spotify for similar artists and playlists
    spotify_results = await search_spotify(
        genres=genres,
        year_range="2020-2023",  # Recent music
        limit=50  # Get more results for better matching
    )
    
    # Filter and rank results based on relevance
    ranked_artists = rank_results(spotify_results["artists"], analysis_results)
    ranked_playlists = rank_results(spotify_results["playlists"], analysis_results)
    
    # Compile report
    report = {
        "analysis": analysis_results,
        "recommendations": {
            "artists_to_target": ranked_artists[:20],
            "playlists_to_pitch": ranked_playlists[:20],
            "marketing_suggestions": generate_marketing_suggestions(analysis_results)
        },
        "detailed_insights": generate_detailed_insights(analysis_results)
    }
    
    # Save report to database and send email
    report_id = await save_report(report, user_email)
    await send_report_email(user_email, report_id)
    
    return report_id
