import os
import logging
import requests
import tempfile
from urllib.parse import urlparse
import yt_dlp
import numpy as np
from collections import defaultdict
import essentia.standard as es
from essentia.standard import (
    MonoLoader,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredictMusiCNN,
    TensorflowPredict2D,
)

# Genre and Tag Constants
JAMENDO_TAGS = ['electronic', 'rock', 'ambient', 'pop', 'experimental', 'metal', 'classical', 
        'folk', 'jazz', 'instrumental', 'alternative', 'punk', 'indie', 'hip hop', 
        'techno', 'house', 'dance', 'dark', 'drum and bass', 'industrial', 'chillout', 
        'beat', 'black metal', 'core', 'contemporary', 'trance', 'heavy', 'progressive', 
        'hardcore', 'atmospheric', 'soundtrack', 'fusion', 'psychedelic', 'vocal', 
        'synthpop', 'noise', 'minimal', 'disco', 'blues', 'chill', 'electro', 'orchestral',
        'garage', 'deep', 'melodic', 'acoustic', 'house deep', 'funk', 'modern', 'piano']

JAMENDO_GENRES = [
    '60s', '70s', '80s', '90s', 'acidjazz', 'alternative', 'alternativerock', 'ambient',
    'atmospheric', 'blues', 'bluesrock', 'bossanova', 'breakbeat', 'celtic', 'chanson',
    'chillout', 'choir', 'classical', 'classicrock', 'club', 'contemporary', 'country',
    'dance', 'darkambient', 'darkwave', 'deephouse', 'disco', 'downtempo', 'drumnbass',
    'dub', 'dubstep', 'easylistening', 'edm', 'electronic', 'electronica', 'electropop',
    'ethno', 'eurodance', 'experimental', 'folk', 'funk', 'fusion', 'groove', 'grunge',
    'hard', 'hardrock', 'hiphop', 'house', 'idm', 'improvisation', 'indie', 'industrial',
    'instrumentalpop', 'instrumentalrock', 'jazz', 'jazzfusion', 'latin', 'lounge',
    'medieval', 'metal', 'minimal', 'newage', 'newwave', 'orchestral', 'pop', 'popfolk',
    'poprock', 'postrock', 'progressive', 'psychedelic', 'punkrock', 'rap', 'reggae',
    'rock', 'rockabilly', 'rocknroll', 'singersongwriter', 'ska', 'slow', 'smooth',
    'soul', 'soundscape', 'space', 'swing', 'symphonic', 'synthpop', 'techno', 'trance',
    'triphop', 'vocal', 'world'
]

DISCOGS_GENRES = [
    'african', 'blues', 'brass & military', 'children\'s', 'classical', 'electronic',
    'folk, world, & country', 'funk / soul', 'hip hop', 'jazz', 'latin', 'non-music',
    'pop', 'reggae', 'rock', 'stage & screen'
]

# DISCOGS_GENRES_FLAT = [
#     'Blues', 'Boogie Woogie', 'Chicago Blues', 'Country Blues', 'Delta Blues', 
#     'Electric Blues', 'Harmonica Blues', 'Jump Blues', 'Louisiana Blues', 
#     'Modern Electric Blues', 'Piano Blues', 'Rhythm & Blues', 'Texas Blues',
#     'Brass & Military', 'Brass Band', 'Marches', 'Military',
#     'Children\'s', 'Educational', 'Nursery Rhymes', 'Story',
#     'Classical', 'Baroque', 'Choral', 'Classical', 'Contemporary', 'Impressionist', 
#     'Medieval', 'Modern', 'Neo-Classical', 'Neo-Romantic', 'Opera', 'Post-Modern', 
#     'Renaissance', 'Romantic',
#     'Electronic', 'Abstract', 'Acid', 'Acid House', 'Acid Jazz', 'Ambient', 'Bassline', 
#     'Beatdown', 'Berlin-School', 'Big Beat', 'Bleep', 'Breakbeat', 'Breakcore', 'Breaks', 
#     'Broken Beat', 'Chillwave', 'Chiptune', 'Dance-pop', 'Dark Ambient', 'Darkwave', 
#     'Deep House', 'Deep Techno', 'Disco', 'Disco Polo', 'Donk', 'Downtempo', 'Drone', 
#     'Drum n Bass', 'Dub', 'Dub Techno', 'Dubstep', 'Dungeon Synth', 'EBM', 'Electro', 
#     'Electro House', 'Electroclash', 'Euro House', 'Euro-Disco', 'Eurobeat', 'Eurodance', 
#     'Experimental', 'Freestyle', 'Future Jazz', 'Gabber', 'Garage House', 'Ghetto', 
#     'Ghetto House', 'Glitch', 'Goa Trance', 'Grime', 'Halftime', 'Hands Up', 
#     'Happy Hardcore', 'Hard House', 'Hard Techno', 'Hard Trance', 'Hardcore', 'Hardstyle', 
#     'Hi NRG', 'Hip Hop', 'Hip-House', 'House', 'IDM', 'Illbient', 'Industrial', 
#     'Italo House', 'Italo-Disco', 'Italodance', 'Jazzdance', 'Juke', 'Jumpstyle', 
#     'Jungle', 'Latin', 'Leftfield', 'Makina', 'Minimal', 'Minimal Techno', 
#     'Modern Classical', 'Musique Concrète', 'Neofolk', 'New Age', 'New Beat', 
#     'New Wave', 'Noise', 'Nu-Disco', 'Power Electronics', 'Progressive Breaks', 
#     'Progressive House', 'Progressive Trance', 'Psy-Trance', 'Rhythmic Noise', 
#     'Schranz', 'Sound Collage', 'Speed Garage', 'Speedcore', 'Synth-pop', 'Synthwave', 
#     'Tech House', 'Tech Trance', 'Techno', 'Trance', 'Tribal', 'Tribal House', 
#     'Trip Hop', 'Tropical House', 'UK Garage', 'Vaporwave',
#     'Folk, World, & Country', 'African', 'Bluegrass', 'Cajun', 'Canzone Napoletana', 
#     'Catalan Music', 'Celtic', 'Country', 'Fado', 'Flamenco', 'Folk', 
#     'Gospel', 'Highlife', 'Hillbilly', 'Hindustani', 'Honky Tonk', 
#     'Indian Classical', 'Laïkó', 'Nordic', 'Pacific', 'Polka', 'Raï', 
#     'Romani', 'Soukous', 'Séga', 'Volksmusik', 'Zouk', 'Éntekhno',
#     'Funk / Soul', 'Afrobeat', 'Boogie', 'Contemporary R&B', 'Disco', 'Free Funk', 'Funk', 
#     'Gospel', 'Neo Soul', 'New Jack Swing', 'P.Funk', 'Psychedelic', 
#     'Rhythm & Blues', 'Soul', 'Swingbeat', 'UK Street Soul',
#     'Hip Hop', 'Bass Music', 'Boom Bap', 'Bounce', 'Britcore', 'Cloud Rap', 'Conscious', 
#     'Crunk', 'Cut-up/DJ', 'DJ Battle Tool', 'Electro', 'G-Funk', 'Gangsta', 
#     'Grime', 'Hardcore Hip-Hop', 'Horrorcore', 'Instrumental', 'Jazzy Hip-Hop', 
#     'Miami Bass', 'Pop Rap', 'Ragga HipHop', 'RnB/Swing', 'Screw', 'Thug Rap', 
#     'Trap', 'Trip Hop', 'Turntablism',
#     'Jazz', 'Afro-Cuban Jazz', 'Afrobeat', 'Avant-garde Jazz', 'Big Band', 'Bop', 
#     'Bossa Nova', 'Contemporary Jazz', 'Cool Jazz', 'Dixieland', 'Easy Listening', 
#     'Free Improvisation', 'Free Jazz', 'Fusion', 'Gypsy Jazz', 'Hard Bop', 
#     'Jazz-Funk', 'Jazz-Rock', 'Latin Jazz', 'Modal', 'Post Bop', 'Ragtime', 
#     'Smooth Jazz', 'Soul-Jazz', 'Space-Age', 'Swing',
#     'Latin', 'Afro-Cuban', 'Baião', 'Batucada', 'Beguine', 'Bolero', 'Boogaloo', 
#     'Bossanova', 'Cha-Cha', 'Charanga', 'Compas', 'Cubano', 'Cumbia', 'Descarga', 
#     'Forró', 'Guaguancó', 'Guajira', 'Guaracha', 'MPB', 'Mambo', 'Mariachi', 
#     'Merengue', 'Norteño', 'Nueva Cancion', 'Pachanga', 'Porro', 'Ranchera', 
#     'Reggaeton', 'Rumba', 'Salsa', 'Samba', 'Son', 'Son Montuno', 'Tango', 
#     'Tejano', 'Vallenato',
#     'Non-Music', 'Audiobook', 'Comedy', 'Dialogue', 'Education', 'Field Recording', 
#     'Interview', 'Monolog', 'Poetry', 'Political', 'Promotional', 'Radioplay', 
#     'Religious', 'Spoken Word',
#     'Pop', 'Ballad', 'Bollywood', 'Bubblegum', 'Chanson', 'City Pop', 'Europop', 
#     'Indie Pop', 'J-pop', 'K-pop', 'Kayōkyoku', 'Light Music', 'Music Hall', 
#     'Novelty', 'Parody', 'Schlager', 'Vocal',
#     'Reggae', 'Calypso', 'Dancehall', 'Dub', 'Lovers Rock', 'Ragga', 'Reggae', 
#     'Reggae-Pop', 'Rocksteady', 'Roots Reggae', 'Ska', 'Soca',
#     'Rock', 'AOR', 'Acid Rock', 'Acoustic', 'Alternative Rock', 'Arena Rock', 'Art Rock', 
#     'Atmospheric Black Metal', 'Avantgarde', 'Beat', 'Black Metal', 'Blues Rock', 
#     'Brit Pop', 'Classic Rock', 'Coldwave', 'Country Rock', 'Crust', 'Death Metal', 
#     'Deathcore', 'Deathrock', 'Depressive Black Metal', 'Doo Wop', 'Doom Metal', 
#     'Dream Pop', 'Emo', 'Ethereal', 'Experimental', 'Folk Metal', 'Folk Rock', 
#     'Funeral Doom Metal', 'Funk Metal', 'Garage Rock', 'Glam', 'Goregrind', 
#     'Goth Rock', 'Gothic Metal', 'Grindcore', 'Grunge', 'Hard Rock', 'Hardcore', 
#     'Heavy Metal', 'Indie Rock', 'Industrial', 'Krautrock', 'Lo-Fi', 'Lounge', 
#     'Math Rock', 'Melodic Death Metal', 'Melodic Hardcore', 'Metalcore', 'Mod', 
#     'Neofolk', 'New Wave', 'No Wave', 'Noise', 'Noisecore', 'Nu Metal', 'Oi', 
#     'Parody', 'Pop Punk', 'Pop Rock', 'Pornogrind', 'Post Rock', 'Post-Hardcore', 
#     'Post-Metal', 'Post-Punk', 'Power Metal', 'Power Pop', 'Power Violence', 
#     'Prog Rock', 'Progressive Metal', 'Psychedelic Rock', 'Psychobilly', 'Pub Rock', 
#     'Punk', 'Rock & Roll', 'Rockabilly', 'Shoegaze', 'Ska', 'Sludge Metal', 
#     'Soft Rock', 'Southern Rock', 'Space Rock', 'Speed Metal', 'Stoner Rock', 
#     'Surf', 'Symphonic Rock', 'Technical Death Metal', 'Thrash', 'Twist', 
#     'Viking Metal', 'Yé-Yé',
#     'Stage & Screen', 'Musical', 'Score', 'Soundtrack', 'Theme'
# ]

MSD_TAGS = [
    "rock",
    "pop",
    "alternative",
    "indie",
    "electronic",
    "female vocalists",
    "dance",
    "metal",
    "alternative rock",
    "jazz",
    "beautiful",
    "experimental",
    "guitar",
    "classic rock",
    "ambient",
    "indie rock",
    "folk",
    "soul",
    "punk",
    "instrumental",
    "pop rock",
    "chillout",
    "male vocalists",
    "hip-hop",
    "hard rock",
    "80s",
    "progressive rock",
    "heavy metal",
    "hardcore",
    "black metal",
    "blues",
    "electronica",
    "rap",
    "acoustic",
    "psychedelic",
    "piano",
    "funk",
    "alternative metal",
    "death metal",
    "classical",
    "industrial",
    "sexy",
    "thrash metal",
    "progressive metal",
    "90s",
    "oldies",
    "country",
    "cool",
    "heavy",
    "progressive",
    "british",
    "favorite",
    "amazing",
    "trance",
    "live",
    "loved",
    "rnb",
    "punk rock",
    "mellow",
    "epic",
    "new wave",
    "disco",
    "favorites",
    "american",
    "idm",
    "electro",
    "indie pop",
    "techno",
    "german",
    "house",
    "awesome",
    "jazz fusion",
    "dark",
    "psytrance",
    "rock n roll",
    "instrumental rock",
    "singer-songwriter",
    "japanese",
    "classic",
    "ambient electronic",
    "drum and bass",
    "experimental rock",
    "female vocalist",
    "alternative punk",
    "soft rock",
    "industrial metal",
    "reggae",
    "post-rock",
    "trip-hop",
    "bass",
    "punk metal",
    "smooth jazz",
    "dub",
    "avant-garde",
    "70s",
    "downtempo",
    "post punk",
    "novelty",
    "symphonic metal",
    "contemporary classical",
]

# Mood and Context Labels
MIREX_MOODS = [
    'passionate/rousing/confident/boisterous/rowdy',
    'rollicking/cheerful/fun/sweet/amiable',
    'literate/poignant/wistful/bittersweet/brooding',
    'humorous/silly/campy/quirky/whimsical',
    'aggressive/fiery/tense/anxious/intense'
]

JAMENDO_MOODS = [
    'action', 'adventure', 'advertising', 'background', 'ballad', 'calm', 
    'children', 'christmas', 'commercial', 'cool', 'corporate', 'dark', 'deep',
    'documentary', 'drama', 'dramatic', 'dream', 'emotional', 'energetic', 
    'epic', 'fast', 'film', 'fun', 'funny', 'game', 'groovy', 'happy', 'heavy',
    'holiday', 'hopeful', 'inspiring', 'love', 'meditative', 'melancholic', 
    'melodic', 'motivational', 'movie', 'nature', 'party', 'positive',
    'powerful', 'relaxing', 'retro', 'romantic', 'sad', 'sexy', 'slow', 'soft', 
    'soundscape', 'space', 'sport', 'summer', 'trailer', 'travel', 'upbeat',
    'uplifting'
]

# Create a ModelLoader class to load all models once
class ModelLoader:
    def __init__(self):
        try:
            # Original embedding models
            self.discogs_effnet = TensorflowPredictEffnetDiscogs(
                graphFilename="lab/essentia/models/discogs-effnet-bs64-1.pb",
                output="PartitionedCall:1"
            )
            self.musicnn = TensorflowPredictMusiCNN(
                graphFilename="lab/essentia/models/msd-musicnn-1.pb",
                output="model/dense/BiasAdd"
            )

            # Jamendo Tags model
            self.jamendo_tags_model = TensorflowPredict2D(
                graphFilename="lab/essentia/models/mtg_jamendo_top50tags-discogs-effnet-1.pb",
                input="model/Placeholder",
                output="model/Sigmoid"
            )

            # Discogs Genres model
            self.discogs_genres_model = TensorflowPredict2D(
                graphFilename="lab/essentia/models/genre_discogs400-discogs-effnet-1.pb",
                input="model/Placeholder",
                output="model/Softmax"
            )

            # Jamendo Genres model
            self.jamendo_genres_model = TensorflowPredict2D(
                graphFilename="lab/essentia/models/mtg_jamendo_genre-discogs-effnet-1.pb",
                input="model/Placeholder",
                output="model/Sigmoid"
            )

            # MSD Tags model
            self.msd_tags_model = TensorflowPredict2D(
                graphFilename="lab/essentia/models/msd-msd-musicnn-1.pb",
                input="model/Placeholder",
                output="model/Softmax"
            )

            # VGGish-based models need different input/output nodes
            def create_vggish_model(filename):
                return TensorflowPredict2D(
                    graphFilename=filename,
                    input="model/Placeholder",
                    output="model/dense_1/BiasAdd"
                )

            # Danceability models
            self.danceability_models = {
                'effnet': create_vggish_model("lab/essentia/models/danceability-audioset-vggish-1.pb")
            }

            # Mood models
            self.mood_aggressive_models = {
                'effnet': create_vggish_model("lab/essentia/models/mood_aggressive-audioset-vggish-1.pb")
            }
            self.mood_happy_models = {
                'effnet': create_vggish_model("lab/essentia/models/mood_happy-audioset-vggish-1.pb")
            }
            self.mood_party_models = {
                'effnet': create_vggish_model("lab/essentia/models/mood_party-audioset-vggish-1.pb")
            }
            self.mood_relaxed_models = {
                'effnet': create_vggish_model("lab/essentia/models/mood_relaxed-audioset-vggish-1.pb")
            }
            self.mood_sad_models = {
                'effnet': create_vggish_model("lab/essentia/models/mood_sad-audioset-vggish-1.pb")
            }

            # Approachability models
            self.approachability_models = {
                '2c': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/approachability_2c-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Softmax"
                ),
                '3c': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/approachability_3c-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Softmax"
                ),
                'regression': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/approachability_regression-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Identity"
                )
            }

            # Engagement models
            self.engagement_models = {
                '2c': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/engagement_2c-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Softmax"
                ),
                '3c': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/engagement_3c-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Softmax"
                ),
                'regression': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/engagement_regression-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Identity"
                )
            }

            # Jamendo mood/theme models
            self.jamendo_moodtheme_models = {
                'effnet': TensorflowPredict2D(
                    graphFilename="lab/essentia/models/mtg_jamendo_moodtheme-discogs-effnet-1.pb",
                    input="model/Placeholder",
                    output="model/Sigmoid"
                )
            }

            logging.info("All models loaded successfully.")
        except Exception as e:
            logging.error(f"Error loading models: {e}")
            # Reset all attributes to None
            self.discogs_effnet = None
            self.musicnn = None
            self.jamendo_tags_model = None
            self.discogs_genres_model = None
            self.jamendo_genres_model = None
            self.msd_tags_model = None
            self.approachability_models = {}
            self.engagement_models = {}
            self.jamendo_moodtheme_models = {}
            self.danceability_models = {}
            self.mood_aggressive_models = {}
            self.mood_happy_models = {}
            self.mood_party_models = {}
            self.mood_relaxed_models = {}
            self.mood_sad_models = {}
            raise

def download_audio(url):
    """Download audio file from URL to a temporary file."""
    try:
        # Configure yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(id)s.%(ext)s',
            'ffmpeg_location': '/usr/local/bin/ffmpeg',  # Update as needed
            'quiet': True,  # Suppress yt-dlp output
            'no_warnings': True
        }

        # For SoundCloud and YouTube links, use yt-dlp
        if 'soundcloud.com' in url or 'youtube.com' in url or 'youtu.be' in url:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                logging.info(f"Downloaded audio: {info['id']}.mp3")
                return f"{info['id']}.mp3"
        else:
            # Original direct download logic for direct audio file URLs
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Get the filename from the URL or use a default
            filename = os.path.basename(urlparse(url).path) or 'audio_file'
            
            # Create temporary file with the correct extension
            suffix = os.path.splitext(filename)[1] or '.mp3'  # default to .mp3 if no extension
            temp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            
            # Write the audio file
            with temp as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logging.info(f"Downloaded audio to temporary file: {temp.name}")
            return temp.name
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return None

def load_audio(audio_path, sample_rate=16000):
    """Load and preprocess audio file."""
    try:
        # Use MonoLoader to load audio directly as mono
        loader = es.MonoLoader(
            filename=audio_path, sampleRate=sample_rate, resampleQuality=4
        )
        audio = loader()
        # Normalize audio
        audio = es.EqualLoudness()(audio)
        return audio
    except Exception as e:
        logging.error(f"Error loading audio: {e}")
        return None

def analyze_mood_category(audio, model_loader, category_models, embeddings=None):
    """Analyze audio file for a specific mood category using multiple models."""
    results = {}
    try:
        # Only use effnet models for now since we have effnet embeddings
        for model_name, model in category_models.items():
            if 'effnet' in model_name.lower():  # Only process effnet models
                try:
                    if embeddings is None:
                        embeddings = model_loader.discogs_effnet(audio)
                    predictions = model(embeddings)
                    results[model_name] = predictions
                except Exception as e:
                    logging.error(f"Error analyzing {model_name} model: {e}")
    except Exception as e:
        logging.error(f"Error generating embeddings: {e}")
    return results

def analyze_jamendo_music_tags(audio, model_loader):
    """Analyze Jamendo music tags."""
    try:
        embeddings = model_loader.discogs_effnet(audio)
        return model_loader.jamendo_tags_model(embeddings)
    except Exception as e:
        logging.error(f"Error analyzing Jamendo tags: {e}")
        return None

def analyze_discogs_genres(audio, model_loader):
    """Analyze Discogs genres."""
    try:
        embeddings = model_loader.discogs_effnet(audio)
        logging.debug("Generated embeddings for Discogs genres")
        predictions = model_loader.discogs_genres_model(embeddings)
        logging.debug(f"Discogs genres predictions: {predictions}")
        return predictions
    except Exception as e:
        logging.error(f"Error analyzing Discogs genres: {e}")
        return None

def analyze_jamendo_genres(audio, model_loader):
    """Analyze Jamendo genres."""
    try:
        embeddings = model_loader.discogs_effnet(audio)
        return model_loader.jamendo_genres_model(embeddings)
    except Exception as e:
        logging.error(f"Error analyzing Jamendo genres: {e}")
        return None

def analyze_msd_tags(audio, model_loader):
    """Analyze MSD tags."""
    try:
        embeddings = model_loader.musicnn(audio)
        logging.debug("Generated embeddings for MSD tags")
        predictions = model_loader.msd_tags_model(embeddings)
        logging.debug(f"MSD tags predictions: {predictions}")
        return predictions
    except Exception as e:
        logging.error(f"Error analyzing MSD tags: {e}")
        return None

def process_binary_results(results, positive_label, negative_label, threshold=0.5):
    """Process and print binary classification results from multiple models."""
    print(f"\n=== {positive_label} vs {negative_label} ===")
    for model_name, predictions in results.items():
        try:
            prob = float(predictions[0][0])
            label = positive_label if prob >= threshold else negative_label
            print(f"{model_name}: {label} ({prob:.3f})")
        except Exception as e:
            logging.error(f"Error processing {model_name} results: {e}")

def process_approachability_results(results):
    """Process approachability results from different models."""
    print("\n=== Approachability Analysis ===")
    try:
        # Binary classification (2c)
        if '2c' in results and results['2c'] is not None:
            prob = float(results['2c'][0][0])
            print(f"Binary: {'Approachable' if prob >= 0.5 else 'Not Approachable'} ({prob:.3f})")
        
        # Three-class classification (3c)
        if '3c' in results and results['3c'] is not None:
            probs = results['3c'][0]
            classes = ['Low', 'Medium', 'High']
            max_idx = max(range(len(probs)), key=lambda i: probs[i])
            print(f"Three-class: {classes[max_idx]} ({probs[max_idx]:.3f})")
        
        # Regression
        if 'regression' in results and results['regression'] is not None:
            value = float(results['regression'][0][0])
            print(f"Regression value: {value:.3f}")
    except Exception as e:
        logging.error(f"Error processing approachability results: {e}")

def process_engagement_results(results):
    """Process engagement results from different models."""
    print("\n=== Engagement Analysis ===")
    try:
        # Binary classification (2c)
        if '2c' in results and results['2c'] is not None:
            prob = float(results['2c'][0][0])
            print(f"Binary: {'High Engagement' if prob >= 0.5 else 'Low Engagement'} ({prob:.3f})")
        
        # Three-class classification (3c)
        if '3c' in results and results['3c'] is not None:
            probs = results['3c'][0]
            classes = ['Low', 'Medium', 'High']
            max_idx = max(range(len(probs)), key=lambda i: probs[i])
            print(f"Three-class: {classes[max_idx]} ({probs[max_idx]:.3f})")
        
        # Regression
        if 'regression' in results and results['regression'] is not None:
            value = float(results['regression'][0][0])
            print(f"Regression value: {value:.3f}")
    except Exception as e:
        logging.error(f"Error processing engagement results: {e}")

def process_jamendo_moodtheme_results(results, threshold=0.2):
    """Process Jamendo mood/theme results from different models."""
    print("\n=== Jamendo Mood/Theme Analysis ===")
    try:
        for model_name, predictions in results.items():
            if predictions is not None and len(predictions) > 0:
                print(f"\nModel: {model_name}")
                mood_predictions = list(zip(JAMENDO_MOODS, predictions[0]))
                relevant_moods = [(mood, float(prob)) for mood, prob in mood_predictions if prob > threshold]
                relevant_moods.sort(key=lambda x: x[1], reverse=True)
                
                if relevant_moods:
                    for mood, probability in relevant_moods:
                        print(f"{mood}: {probability:.3f}")
    except Exception as e:
        logging.error(f"Error processing Jamendo mood/theme results: {e}")

def process_audio(source, model_loader):
    """Process audio from either a URL or local file path."""
    if source.startswith(('http://', 'https://', 'www.')):
        # Handle as URL
        temp_path = download_audio(source)
        should_cleanup = True
    else:
        # Handle as local file
        if not os.path.exists(source):
            logging.error(f"File not found: {source}")
            return
        temp_path = source
        should_cleanup = False

    if not temp_path:
        logging.error("Failed to obtain audio path.")
        return

    try:
        audio = load_audio(temp_path)
        if audio is None:
            logging.error("Audio loading failed.")
            return

        # Generate embeddings once for efficiency
        embeddings = model_loader.discogs_effnet(audio)

        # Run all analyses
        logging.info(f"\nAnalyzing audio {'from URL' if should_cleanup else 'file'}: {source}")

        # Original analyses
        jamendo_tags = analyze_jamendo_music_tags(audio, model_loader)
        discogs_genres = analyze_discogs_genres(audio, model_loader)
        jamendo_genres = analyze_jamendo_genres(audio, model_loader)
        msd_tags = analyze_msd_tags(audio, model_loader)

        # Mood and context analyses
        danceability_results = analyze_mood_category(audio, model_loader, 
            model_loader.danceability_models, embeddings)
        mood_aggressive_results = analyze_mood_category(audio, model_loader, 
            model_loader.mood_aggressive_models, embeddings)
        mood_happy_results = analyze_mood_category(audio, model_loader, 
            model_loader.mood_happy_models, embeddings)
        mood_party_results = analyze_mood_category(audio, model_loader, 
            model_loader.mood_party_models, embeddings)
        mood_relaxed_results = analyze_mood_category(audio, model_loader, 
            model_loader.mood_relaxed_models, embeddings)
        mood_sad_results = analyze_mood_category(audio, model_loader, 
            model_loader.mood_sad_models, embeddings)
        approachability_results = analyze_mood_category(audio, model_loader, 
            model_loader.approachability_models, embeddings)
        engagement_results = analyze_mood_category(audio, model_loader, 
            model_loader.engagement_models, embeddings)
        jamendo_moodtheme_results = analyze_mood_category(audio, model_loader, 
            model_loader.jamendo_moodtheme_models, embeddings)

        # Process and print results
        # Original results processing
        print("\n=== Jamendo Tags ===")
        if jamendo_tags is not None:
            process_jamendo_tags(jamendo_tags[0])
        
        print("\n=== Discogs Genres ===")
        if discogs_genres is not None:
            process_discogs_genres_results(discogs_genres[0])
        
        print("\n=== Jamendo Genres ===")
        if jamendo_genres is not None:
            process_jamendo_genres(jamendo_genres[0])
        
        print("\n=== Million Song Dataset Tags ===")
        if msd_tags is not None:
            process_msd_tags(msd_tags[0])

        # Mood and context results processing
        process_binary_results(danceability_results, "Danceable", "Not Danceable")
        process_binary_results(mood_aggressive_results, "Aggressive", "Not Aggressive")
        process_binary_results(mood_happy_results, "Happy", "Not Happy")
        process_binary_results(mood_party_results, "Party", "Not Party")
        process_binary_results(mood_relaxed_results, "Relaxed", "Not Relaxed")
        process_binary_results(mood_sad_results, "Sad", "Not Sad")
        process_approachability_results(approachability_results)
        process_engagement_results(engagement_results)
        process_jamendo_moodtheme_results(jamendo_moodtheme_results)

    finally:
        if should_cleanup and temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)
            logging.info(f"Cleaned up temporary file: {temp_path}")

def process_jamendo_tags(predictions, threshold=0.2):
    """Process Jamendo tag predictions."""
    tag_predictions = list(zip(JAMENDO_TAGS, predictions))
    relevant_tags = [(tag, float(prob)) for tag, prob in tag_predictions if prob > threshold]
    relevant_tags.sort(key=lambda x: x[1], reverse=True)
    
    for tag, probability in relevant_tags:
        print(f"{tag}: {probability:.3f}")

def process_discogs_genres_results(predictions, threshold=0.2):
    """Process Discogs genres results."""
    print("\n=== Discogs Genres ===")
    if predictions is not None and len(predictions) > 0:
        genre_predictions = list(zip(DISCOGS_GENRES, predictions[0]))
        relevant_genres = [(genre, float(prob)) for genre, prob in genre_predictions if prob > threshold]
        relevant_genres.sort(key=lambda x: x[1], reverse=True)
        
        for genre, probability in relevant_genres:
            print(f"{genre}: {probability:.3f}")

def process_jamendo_genres(predictions, threshold=0.2):
    """Process Jamendo genre predictions."""
    genre_predictions = list(zip(JAMENDO_GENRES, predictions))
    relevant_genres = [(genre, float(prob)) for genre, prob in genre_predictions if prob > threshold]
    relevant_genres.sort(key=lambda x: x[1], reverse=True)
    
    for genre, probability in relevant_genres:
        print(f"{genre}: {probability:.3f}")

def process_msd_tags(predictions, threshold=0.2):
    """Process MSD tag predictions."""
    tag_predictions = list(zip(MSD_TAGS, predictions))
    relevant_tags = [(tag, float(prob)) for tag, prob in tag_predictions if prob > threshold]
    relevant_tags.sort(key=lambda x: x[1], reverse=True)
    
    for tag, probability in relevant_tags:
        print(f"{tag}: {probability:.3f}")

def run_tensorflow_session(model, input_data):
    try:
        # Feed a default value for 'saver_filename'
        feed_dict = {
            model.input_tensor: input_data,
            'saver_filename:0': ''  # Provide an empty string or a valid path
        }
        return model.session.run(model.output_tensor, feed_dict=feed_dict)
    except Exception as e:
        logging.error(f"Error running TensorFlow session: {e}")
        return None

# Initialize model loader
model_loader = ModelLoader()
if not all([
    model_loader.discogs_effnet,
    model_loader.musicnn,
    model_loader.jamendo_tags_model,
    model_loader.discogs_genres_model,
    model_loader.jamendo_genres_model,
    model_loader.msd_tags_model,
    model_loader.danceability_models,
    model_loader.mood_aggressive_models,
    model_loader.mood_happy_models,
    model_loader.mood_party_models,
    model_loader.mood_relaxed_models,
    model_loader.mood_sad_models,
    model_loader.approachability_models,
    model_loader.engagement_models,
    model_loader.jamendo_moodtheme_models
]):
    logging.error("Failed to load all models. Exiting.")
    exit(1)

if __name__ == "__main__":
    # Get input from user
    source = input("Enter audio file path or URL: ").strip()
    process_audio(source, model_loader)
