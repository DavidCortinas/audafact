import numpy as np
from essentia.standard import (
    MonoLoader,
    FrameGenerator,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredictMusiCNN,
    TensorflowPredict2D,
)
import logging
import os
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# At module level, add these configurations
GENRE_MODELS = {
    "discogs400": {
        "embedding": "discogs-effnet-bs64-1.pb",
        "genre": "genre_discogs400-discogs-effnet-1.pb",
        "metadata": "genre_discogs400-discogs-effnet-1.json",
        "input": "serving_default_model_Placeholder",
        "output": "PartitionedCall:0",
        "is_hierarchical": True,
    }
}

MOOD_THEME_MODELS = {
    "general": {
        "embedding": "discogs-effnet-bs64-1.pb",
        "mood_theme": "mtg_jamendo_moodtheme-discogs-effnet-1.pb",
        "metadata": "mtg_jamendo_moodtheme-discogs-effnet-1.json",
    },
    "track_level": {
        "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
        "mood_theme": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.pb",
        "metadata": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.json",
    },
}

TAG_MODELS = {
    "mtg_jamendo_general": {
        "embedding": "discogs-effnet-bs64-1.pb",
        "tag": "mtg_jamendo_top50tags-discogs-effnet-1.pb",
        "metadata": "mtg_jamendo_top50tags-discogs-effnet-1.json",
        "input": "model/Placeholder",
        "output": "model/Sigmoid",
        "embedding_type": "effnet",
    },
    # ... other tag models ...
}

# Add global model storage
_LOADED_MODELS = {"genre": {}, "mood_theme": {}, "tags": {}}


def normalize_audio(segment):
    max_val = np.max(np.abs(segment))
    if max_val > 0:
        return segment / max_val
    return segment


def load_json_metadata(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def initialize_models(model_dir: str) -> None:
    """Initialize ML models at startup."""
    global _LOADED_MODELS
    model_dir = os.path.abspath(model_dir)
    logger.info("Initializing ML models...")

    # Start with just genre models as a test
    for model_name, config in GENRE_MODELS.items():
        try:
            # Load embedding model
            embedding_path = os.path.join(model_dir, config["embedding"])
            logger.info(f"Loading {model_name} embedding model from: {embedding_path}")

            embedding_model = TensorflowPredictEffnetDiscogs(
                graphFilename=embedding_path, output="PartitionedCall:1"
            )

            # Load genre model
            genre_path = os.path.join(model_dir, config["genre"])
            logger.info(f"Loading {model_name} genre model from: {genre_path}")

            genre_model = TensorflowPredict2D(
                graphFilename=genre_path, input=config["input"], output=config["output"]
            )

            # Load metadata
            metadata_path = os.path.join(model_dir, config["metadata"])
            metadata = load_json_metadata(metadata_path)

            # Store everything
            _LOADED_MODELS["genre"][model_name] = {
                "embedding": embedding_model,
                "prediction": genre_model,
                "metadata": metadata,
                "is_hierarchical": config["is_hierarchical"],
            }

            logger.info(f"Successfully loaded {model_name} models")

        except Exception as e:
            logger.error(f"Failed to load {model_name} models: {str(e)}")
            _LOADED_MODELS["genre"][model_name] = {"error": str(e)}


async def predict_genre_from_segments(audio_file_path: str, segment_length: int = 45):
    try:
        # Load audio with balanced quality/speed
        audio = MonoLoader(
            filename=audio_file_path, sampleRate=16000, resampleQuality=4
        )()
        frame_size = int(16000 * segment_length)

        # Generate segments
        segments = np.array(
            list(
                FrameGenerator(
                    audio,
                    frameSize=frame_size,
                    hopSize=frame_size // 2,
                    startFromZero=True,
                )
            )
        )

        all_results = {}

        # Use a smaller thread pool
        executor = ThreadPoolExecutor(max_workers=4)

        for model_name, model_data in _LOADED_MODELS["genre"].items():
            if "error" in model_data:
                all_results[model_name] = model_data
                continue

            try:
                num_classes = len(model_data["metadata"]["classes"])
                weighted_sum = np.zeros(num_classes, dtype=np.float32)
                total_weight = 0.0
                genre_counts = np.zeros(num_classes, dtype=np.float32)

                # Process segments sequentially but use the thread pool for each segment
                async def process_segment(segment):
                    def _process():
                        normalized = normalize_audio(segment)
                        embeddings = model_data["embedding"](normalized)
                        return model_data["prediction"](embeddings)[0]

                    return await asyncio.get_event_loop().run_in_executor(
                        executor, _process
                    )

                # Process segments with minimal overhead
                for segment in segments:
                    predictions = await process_segment(segment)
                    weight = float(np.max(predictions))
                    weighted_sum += predictions * weight
                    total_weight += weight
                    genre_counts += predictions > 0.07

                # Calculate final predictions
                averaged = (
                    weighted_sum / total_weight if total_weight > 0 else weighted_sum
                )
                refined_predictions = averaged + 0.2 * (genre_counts / len(segments))

                # Get top genres
                top_indices = np.argsort(refined_predictions)[-15:][::-1]
                top_genres = [
                    (
                        model_data["metadata"]["classes"][i],
                        float(refined_predictions[i]),
                    )
                    for i in top_indices
                    if refined_predictions[i] > 0.07
                ]

                # Format results
                if model_data["is_hierarchical"]:
                    formatted_results = {}
                    for genre_label, confidence in top_genres:
                        umbrella_genre, sub_genre = genre_label.split("---")
                        if umbrella_genre not in formatted_results:
                            formatted_results[umbrella_genre] = {"subgenres": {}}
                        formatted_results[umbrella_genre]["subgenres"][sub_genre] = (
                            round(confidence, 2)
                        )
                else:
                    formatted_results = {
                        genre_label: round(confidence, 2)
                        for genre_label, confidence in top_genres
                    }

                all_results[model_name] = formatted_results

            except Exception as e:
                logger.error(f"Error processing {model_name}: {str(e)}")
                all_results[model_name] = {"error": str(e)}

        return all_results

    except Exception as e:
        logger.error(f"Error in predict_genre_from_segments: {str(e)}")
        raise


def predict_mood_theme_from_audio(
    audio_file_path: str, model_dir: str, segment_length=45
):
    """Predict mood and theme from audio file with segmentation."""
    try:
        logger.info(f"Loading audio from: {audio_file_path}")
        logger.info(f"Using model directory: {model_dir}")

        # Define model configurations
        models = {
            "general": {
                "embedding": "discogs-effnet-bs64-1.pb",
                "mood_theme": "mtg_jamendo_moodtheme-discogs-effnet-1.pb",
                "metadata": "mtg_jamendo_moodtheme-discogs-effnet-1.json",
            },
            "track_level": {
                "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
                "mood_theme": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.pb",
                "metadata": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.json",
            },
        }

        # Load audio once
        logger.info("Loading audio file...")
        audio = MonoLoader(
            filename=audio_file_path, sampleRate=16000, resampleQuality=4
        )()
        logger.info(f"Audio loaded successfully. Length: {len(audio)} samples")

        all_results = {}

        # Process with each model
        for model_name, model_files in models.items():
            try:
                logger.info(f"\nProcessing with {model_name} model...")

                # Construct paths
                embedding_model_path = os.path.join(model_dir, model_files["embedding"])
                mood_theme_model_path = os.path.join(
                    model_dir, model_files["mood_theme"]
                )
                metadata_path = os.path.join(model_dir, model_files["metadata"])

                # Verify files exist
                for path in [
                    embedding_model_path,
                    mood_theme_model_path,
                    metadata_path,
                ]:
                    if not os.path.exists(path):
                        logger.warning(f"Model file not found: {path}")
                        continue

                # Generate embeddings
                logger.info(f"Loading embedding model for {model_name}...")
                embedding_model = TensorflowPredictEffnetDiscogs(
                    graphFilename=embedding_model_path, output="PartitionedCall:1"
                )

                embeddings = embedding_model(audio)
                logger.info(f"Embeddings shape: {embeddings.shape}")

                # Make predictions
                logger.info(f"Loading mood/theme model for {model_name}...")
                model = TensorflowPredict2D(
                    graphFilename=mood_theme_model_path,
                    input="model/Placeholder",
                    output="model/Sigmoid",
                )

                predictions = model(embeddings)
                max_predictions = np.max(predictions, axis=0)

                # Load metadata
                with open(metadata_path) as f:
                    metadata = json.load(f)

                # Process predictions
                min_threshold = 0.2
                min_predictions = 10
                threshold_indices = np.where(max_predictions > min_threshold)[0]
                top_k_indices = np.argsort(max_predictions)[-min_predictions:][::-1]
                selected_indices = np.unique(
                    np.concatenate([threshold_indices, top_k_indices])
                )

                # Create results
                results = {
                    metadata["classes"][i]: round(float(max_predictions[i]), 3)
                    for i in selected_indices
                }

                # Sort by confidence
                results = dict(
                    sorted(results.items(), key=lambda x: x[1], reverse=True)
                )

                logger.info(f"{model_name} model predictions: {len(results)} items")
                all_results[model_name] = results

            except Exception as e:
                logger.error(f"Error processing {model_name} model: {str(e)}")
                all_results[model_name] = {"error": str(e)}

        return all_results

    except Exception as e:
        logger.error(f"Error in predict_mood_theme_from_audio: {str(e)}", exc_info=True)
        raise


def predict_tags_from_segments(audio_file_path, model_dir, segment_length=45):
    """Predict tags using multiple models with segmentation."""
    model_dir = os.path.abspath(model_dir)
    print(f"Loading audio file from: {audio_file_path}")

    # Define model configurations
    models = {
        "mtg_jamendo_general": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "tag": "mtg_jamendo_top50tags-discogs-effnet-1.pb",
            "metadata": "mtg_jamendo_top50tags-discogs-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtg_jamendo_track": {
            "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
            "tag": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.pb",
            "metadata": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtt_general": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "tag": "mtt-discogs-effnet-1.pb",
            "metadata": "mtt-discogs-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtt_track": {
            "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
            "tag": "mtt-discogs_track_embeddings-effnet-1.pb",
            "metadata": "mtt-discogs_track_embeddings-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "msd": {
            "embedding": "msd-musicnn-1.pb",
            "tag": "msd-msd-musicnn-1.pb",
            "metadata": "msd-msd-musicnn-1.json",
            "input": "serving_default_model_Placeholder",
            "output": "PartitionedCall",
            "embedding_type": "musicnn",
            "embedding_output": "model/dense/BiasAdd",
        },
    }

    # Load audio once
    audio = MonoLoader(filename=audio_file_path, sampleRate=16000, resampleQuality=4)()

    all_results = {}

    for model_name, model_config in models.items():
        try:
            print(f"\nProcessing with {model_name} model...")

            if model_config["embedding_type"] == "musicnn":
                # Special handling for MSD MusiCNN model
                embedding_model_path = os.path.join(
                    model_dir, model_config["embedding"]
                )
                tag_model_path = os.path.join(model_dir, model_config["tag"])

                print(f"Loading MusiCNN embedding model from: {embedding_model_path}")
                embedding_model = TensorflowPredictMusiCNN(
                    graphFilename=embedding_model_path, output="model/dense/BiasAdd"
                )

                print("Generating MusiCNN embeddings...")
                embeddings = embedding_model(audio)

                print(f"Loading MSD tag model from: {tag_model_path}")
                tag_model = TensorflowPredict2D(
                    graphFilename=tag_model_path,
                    input="serving_default_model_Placeholder",
                    output="PartitionedCall",
                )

                predictions = tag_model(embeddings)
                predictions = predictions[0]  # Get first prediction

            else:
                # Original handling for EffNet models
                frame_size = int(16000 * segment_length)
                segment_frames = list(
                    FrameGenerator(
                        audio,
                        frameSize=frame_size,
                        hopSize=frame_size // 2,
                        startFromZero=True,
                    )
                )

                # Initialize models
                embedding_model = None
                tag_model = None

                # Initialize prediction arrays
                metadata_path = os.path.join(model_dir, model_config["metadata"])
                metadata = load_json_metadata(metadata_path)
                tag_labels = metadata["classes"]
                num_classes = len(tag_labels)
                weighted_sum = np.zeros(num_classes)
                total_weight = 0.0
                tag_counts = np.zeros(num_classes)

                # Process segments
                for i, segment in enumerate(segment_frames):
                    print(
                        f"Generating embeddings for segment {i+1}/{len(segment_frames)}..."
                    )
                    normalized_segment = normalize_audio(segment)

                    if embedding_model is None:
                        embedding_model_path = os.path.join(
                            model_dir, model_config["embedding"]
                        )
                        print(f"Loading embedding model from: {embedding_model_path}")
                        embedding_model = TensorflowPredictEffnetDiscogs(
                            graphFilename=embedding_model_path,
                            output="PartitionedCall:1",
                        )

                    embeddings = embedding_model(normalized_segment)

                    if tag_model is None:
                        tag_model_path = os.path.join(model_dir, model_config["tag"])
                        print(f"Loading tag model from: {tag_model_path}")
                        tag_model = TensorflowPredict2D(
                            graphFilename=tag_model_path,
                            input=model_config["input"],
                            output=model_config["output"],
                        )

                    segment_predictions = tag_model(embeddings)[0]
                    weight = np.max(segment_predictions)
                    weighted_sum += segment_predictions * weight
                    total_weight += weight
                    tag_counts += segment_predictions > 0.07

                # Calculate final predictions
                if total_weight > 0:
                    averaged_predictions = weighted_sum / total_weight
                else:
                    averaged_predictions = weighted_sum

                frequency_weight = 0.2
                predictions = averaged_predictions + frequency_weight * (
                    tag_counts / len(segment_frames)
                )

            # Load metadata for formatting results
            metadata_path = os.path.join(model_dir, model_config["metadata"])
            metadata = load_json_metadata(metadata_path)
            tag_labels = metadata["classes"]

            # Get top predictions
            threshold = 0.07
            top_indices = np.argsort(predictions)[-15:][::-1]
            top_tags = [
                (tag_labels[i], float(predictions[i]))
                for i in top_indices
                if predictions[i] > threshold
            ]

            # Format results
            formatted_results = {
                tag: round(confidence, 2) for tag, confidence in top_tags
            }

            all_results[model_name] = formatted_results

        except Exception as e:
            print(f"Error processing {model_name}: {str(e)}")
            all_results[model_name] = {"error": str(e)}

    return all_results


def predict_tags_from_file(audio_file_path, model_dir):
    """Predict tags using multiple models on entire file (no segmentation)."""
    model_dir = os.path.abspath(model_dir)
    print(f"Loading audio file from: {audio_file_path}")

    # Define model configurations
    models = {
        "mtg_jamendo_general": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "tag": "mtg_jamendo_top50tags-discogs-effnet-1.pb",
            "metadata": "mtg_jamendo_top50tags-discogs-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtg_jamendo_track": {
            "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
            "tag": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.pb",
            "metadata": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtt_general": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "tag": "mtt-discogs-effnet-1.pb",
            "metadata": "mtt-discogs-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "mtt_track": {
            "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
            "tag": "mtt-discogs_track_embeddings-effnet-1.pb",
            "metadata": "mtt-discogs_track_embeddings-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "embedding_type": "effnet",
        },
        "msd": {
            "embedding": "msd-musicnn-1.pb",
            "tag": "msd-msd-musicnn-1.pb",
            "metadata": "msd-msd-musicnn-1.json",
            "input": "serving_default_model_Placeholder",
            "output": "PartitionedCall",
            "embedding_type": "musicnn",
        },
    }

    # Load audio once
    audio = MonoLoader(filename=audio_file_path, sampleRate=16000, resampleQuality=4)()

    all_results = {}

    for model_name, model_config in models.items():
        try:
            print(f"\nProcessing with {model_name} model...")

            if model_config["embedding_type"] == "musicnn":
                # MSD MusiCNN model - using exact example code structure
                embedding_model_path = os.path.join(
                    model_dir, model_config["embedding"]
                )
                tag_model_path = os.path.join(model_dir, model_config["tag"])

                print(f"Loading MusiCNN embedding model from: {embedding_model_path}")
                embedding_model = TensorflowPredictMusiCNN(
                    graphFilename=embedding_model_path, output="model/dense/BiasAdd"
                )

                print("Generating MusiCNN embeddings...")
                embeddings = embedding_model(audio)

            else:
                # EffNet models
                embedding_model_path = os.path.join(
                    model_dir, model_config["embedding"]
                )
                print(f"Loading embedding model from: {embedding_model_path}")
                embedding_model = TensorflowPredictEffnetDiscogs(
                    graphFilename=embedding_model_path, output="PartitionedCall:1"
                )

                print("Generating embeddings...")
                embeddings = embedding_model(audio)

            # Load tag model and make predictions
            tag_model_path = os.path.join(model_dir, model_config["tag"])
            print(f"Loading tag model from: {tag_model_path}")
            tag_model = TensorflowPredict2D(
                graphFilename=tag_model_path,
                input=model_config["input"],
                output=model_config["output"],
            )

            predictions = tag_model(embeddings)
            predictions = predictions[0]  # Get first prediction

            # Load metadata for formatting results
            metadata_path = os.path.join(model_dir, model_config["metadata"])
            metadata = load_json_metadata(metadata_path)
            tag_labels = metadata["classes"]

            # Get top predictions
            threshold = 0.07
            top_indices = np.argsort(predictions)[-15:][::-1]
            top_tags = [
                (tag_labels[i], float(predictions[i]))
                for i in top_indices
                if predictions[i] > threshold
            ]

            # Format results
            formatted_results = {
                tag: round(confidence, 2) for tag, confidence in top_tags
            }

            all_results[model_name] = formatted_results

        except Exception as e:
            print(f"Error processing {model_name}: {str(e)}")
            all_results[model_name] = {"error": str(e)}

    return all_results
