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
import tensorflow as tf
import warnings
from ..utils.logging_config import configure_logging
from typing import Dict, Any

configure_logging()

logger = logging.getLogger(__name__)

# Initialize empty model storage
_LOADED_MODELS = {}

# Model configurations
GENRE_MODELS = {
    "discogs400": {
        "embedding": "discogs-effnet-bs64-1.pb",
        "genre": "genre_discogs400-discogs-effnet-1.pb",
        "metadata": "genre_discogs400-discogs-effnet-1.json",
        "input": "serving_default_model_Placeholder",
        "output": "PartitionedCall",
    }
}

TAG_MODELS = {
    "mtg_jamendo_track": {
        "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
        "tag": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.pb",
        "metadata": "mtg_jamendo_top50tags-discogs_track_embeddings-effnet-1.json",
        "input": "model/Placeholder",
        "output": "model/Sigmoid",
    }
}

MOOD_THEME_MODELS = {
    "track_level": {
        "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
        "mood_theme": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.pb",
        "metadata": "mtg_jamendo_moodtheme-discogs_track_embeddings-effnet-1.json",
        "input": "model/Placeholder",
        "output": "model/Sigmoid",
    }
}


def initialize_models(model_dir: str) -> None:
    """Initialize ML models at startup."""
    global _LOADED_MODELS
    logger.info(f"Initializing ML models from directory: {model_dir}")

    try:
        if not os.path.exists(model_dir):
            raise FileNotFoundError(f"Model directory not found: {model_dir}")

        # Initialize all model types using the configurations
        for model_type, models in [
            ("genre", GENRE_MODELS),
            ("tag", TAG_MODELS),
            ("mood_theme", MOOD_THEME_MODELS),
        ]:
            _LOADED_MODELS[model_type] = {}
            for model_name, model_config in models.items():
                _LOADED_MODELS[model_type][model_name] = {
                    "is_hierarchical": False,
                    "batch_size": 64,
                    "embedding_size": 512,
                }
                # Verify all required files exist
                for key in ["embedding", model_type, "metadata"]:
                    file_path = os.path.join(model_dir, model_config[key])
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(
                            f"Missing {key} file for {model_type} model {model_name}: {file_path}"
                        )

                try:
                    embedding_path = os.path.join(model_dir, model_config["embedding"])
                    prediction_path = os.path.join(model_dir, model_config[model_type])
                    metadata_path = os.path.join(model_dir, model_config["metadata"])

                    logger.info(f"Loading {model_type} model {model_name}")
                    _LOADED_MODELS[model_type][model_name] = {
                        "embedding": TensorflowPredictEffnetDiscogs(
                            graphFilename=embedding_path
                        ),
                        "prediction": TensorflowPredict2D(
                            graphFilename=prediction_path,
                            input=model_config["input"],
                            output=model_config["output"],
                        ),
                        "metadata": load_json_metadata(metadata_path),
                        "classes": load_json_metadata(metadata_path)["classes"],
                    }
                    logger.info(f"Successfully loaded {model_type} model {model_name}")

                except Exception as e:
                    logger.error(
                        f"Error loading {model_type} model {model_name}: {str(e)}"
                    )
                    raise

        logger.info("All models loaded successfully")

    except Exception as e:
        logger.error(f"Error initializing models: {str(e)}")
        raise


def normalize_audio(segment):
    max_val = np.max(np.abs(segment))
    if max_val > 0:
        return segment / max_val
    return segment


def load_json_metadata(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


async def predict_genre_from_segments(
    audio_file_path: str, model_dir: str, segment_length: int = 45
):
    """Predict genres from audio segments."""
    model_dir = os.path.abspath(model_dir)
    logger.info(f"Debug - Using model directory: {model_dir}")
    logger.info(f"Loading audio file from: {audio_file_path}")

    # Define model configurations
    models = {
        "discogs400": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "genre": "genre_discogs400-discogs-effnet-1.pb",
            "metadata": "genre_discogs400-discogs-effnet-1.json",
            "input": "serving_default_model_Placeholder",
            "output": "PartitionedCall:0",
            "is_hierarchical": True,
        }
    }

    # Load audio
    audio = MonoLoader(filename=audio_file_path, sampleRate=16000, resampleQuality=4)()
    frame_size = int(16000 * segment_length)
    segment_frames = list(
        FrameGenerator(
            audio, frameSize=frame_size, hopSize=frame_size // 2, startFromZero=True
        )
    )

    all_results = {}

    # Use ThreadPoolExecutor for concurrent processing
    executor = ThreadPoolExecutor(max_workers=4)

    for model_name, model_config in models.items():
        try:
            logger.info(f"\nProcessing with {model_name} model...")

            # Load metadata
            genre_metadata_path = os.path.join(model_dir, model_config["metadata"])
            genre_metadata = load_json_metadata(genre_metadata_path)
            genre_labels = genre_metadata["classes"]

            # Initialize prediction arrays
            num_classes = len(genre_labels)
            weighted_sum = np.zeros(num_classes)
            total_weight = 0.0
            genre_counts = np.zeros(num_classes)
            all_predictions = []

            # Process segments concurrently
            async def process_segment(segment, embedding_model, genre_model):
                def _process():
                    normalized_segment = normalize_audio(segment)
                    embeddings = embedding_model(normalized_segment)
                    predictions = genre_model(embeddings)[0]
                    return predictions

                return await asyncio.get_event_loop().run_in_executor(
                    executor, _process
                )

            # Load models once outside the segment loop
            embedding_model_path = os.path.join(model_dir, model_config["embedding"])
            genre_model_path = os.path.join(model_dir, model_config["genre"])

            embedding_model = TensorflowPredictEffnetDiscogs(
                graphFilename=embedding_model_path, output="PartitionedCall:1"
            )
            genre_model = TensorflowPredict2D(
                graphFilename=genre_model_path,
                input=model_config["input"],
                output=model_config["output"],
            )

            # Process all segments concurrently
            segment_tasks = [
                process_segment(segment, embedding_model, genre_model)
                for segment in segment_frames
            ]
            predictions_list = await asyncio.gather(*segment_tasks)

            # Process predictions
            for predictions in predictions_list:
                weight = np.max(predictions)
                weighted_sum += predictions * weight
                total_weight += weight
                genre_counts += predictions > 0.05
                all_predictions.append(predictions)

            # Calculate final predictions
            if total_weight > 0:
                averaged_predictions = weighted_sum / total_weight
            else:
                averaged_predictions = weighted_sum

            frequency_weight = 0.2
            refined_predictions = averaged_predictions + frequency_weight * (
                genre_counts / len(segment_frames)
            )

            # Get top predictions
            threshold = 0.05
            top_indices = np.argsort(refined_predictions)[-15:][::-1]
            top_genres = [
                (genre_labels[i], float(refined_predictions[i]))
                for i in top_indices
                if refined_predictions[i] > threshold
            ]

            # Format results based on model type
            if model_config["is_hierarchical"]:
                formatted_results = {}
                for genre_label, confidence in top_genres:
                    umbrella_genre, sub_genre = genre_label.split("---")
                    if umbrella_genre not in formatted_results:
                        formatted_results[umbrella_genre] = {}
                    formatted_results[umbrella_genre][sub_genre] = round(confidence, 2)
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


async def predict_mood_theme_from_audio(
    audio_file_path: str, model_dir: str, segment_length: int = 45
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
        executor = ThreadPoolExecutor(max_workers=4)

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

                async def process_audio():
                    def _process():
                        # Generate embeddings
                        logger.info(f"Loading embedding model for {model_name}...")
                        embedding_model = TensorflowPredictEffnetDiscogs(
                            graphFilename=embedding_model_path,
                            output="PartitionedCall:1",
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

                        return model(embeddings)

                    return await asyncio.get_event_loop().run_in_executor(
                        executor, _process
                    )

                # Get predictions
                predictions = await process_audio()
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


async def predict_tags_from_segments(
    audio_file_path: str, model_dir: str, segment_length: int = 45
):
    """Predict tags using multiple models with segmentation."""
    model_dir = os.path.abspath(model_dir)
    logger.info(f"Loading audio file from: {audio_file_path}")

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
        # "mtt_general": {
        #     "embedding": "discogs-effnet-bs64-1.pb",
        #     "tag": "mtt-discogs-effnet-1.pb",
        #     "metadata": "mtt-discogs-effnet-1.json",
        #     "input": "model/Placeholder",
        #     "output": "model/Sigmoid",
        #     "embedding_type": "effnet",
        # },
        # "mtt_track": {
        #     "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
        #     "tag": "mtt-discogs_track_embeddings-effnet-1.pb",
        #     "metadata": "mtt-discogs_track_embeddings-effnet-1.json",
        #     "input": "model/Placeholder",
        #     "output": "model/Sigmoid",
        #     "embedding_type": "effnet",
        # },
        # "msd": {
        #     "embedding": "msd-musicnn-1.pb",
        #     "tag": "msd-msd-musicnn-1.pb",
        #     "metadata": "msd-msd-musicnn-1.json",
        #     "input": "serving_default_model_Placeholder",
        #     "output": "PartitionedCall",
        #     "embedding_type": "musicnn",
        #     "embedding_output": "model/dense/BiasAdd",
        # },
    }

    # Load audio once
    audio = MonoLoader(filename=audio_file_path, sampleRate=16000, resampleQuality=4)()
    all_results = {}
    executor = ThreadPoolExecutor(max_workers=4)

    for model_name, model_config in models.items():
        try:
            logger.info(f"\nProcessing with {model_name} model...")

            if model_config["embedding_type"] == "musicnn":

                async def process_musicnn():
                    def _process():
                        # Special handling for MSD MusiCNN model
                        embedding_model_path = os.path.join(
                            model_dir, model_config["embedding"]
                        )
                        tag_model_path = os.path.join(model_dir, model_config["tag"])

                        logger.info(
                            f"Loading MusiCNN embedding model from: {embedding_model_path}"
                        )
                        embedding_model = TensorflowPredictMusiCNN(
                            graphFilename=embedding_model_path,
                            output="model/dense/BiasAdd",
                        )

                        logger.info("Generating MusiCNN embeddings...")
                        embeddings = embedding_model(audio)

                        logger.info(f"Loading MSD tag model from: {tag_model_path}")
                        tag_model = TensorflowPredict2D(
                            graphFilename=tag_model_path,
                            input="serving_default_model_Placeholder",
                            output="PartitionedCall",
                        )

                        predictions = tag_model(embeddings)
                        return predictions[0]  # Get first prediction

                    return await asyncio.get_event_loop().run_in_executor(
                        executor, _process
                    )

                predictions = await process_musicnn()

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

                # Load models once outside the segment loop
                embedding_model_path = os.path.join(
                    model_dir, model_config["embedding"]
                )
                tag_model_path = os.path.join(model_dir, model_config["tag"])

                embedding_model = TensorflowPredictEffnetDiscogs(
                    graphFilename=embedding_model_path,
                    output="PartitionedCall:1",
                )
                tag_model = TensorflowPredict2D(
                    graphFilename=tag_model_path,
                    input=model_config["input"],
                    output=model_config["output"],
                )

                # Process segments concurrently
                async def process_segment(segment):
                    def _process():
                        normalized_segment = normalize_audio(segment)
                        embeddings = embedding_model(normalized_segment)
                        return tag_model(embeddings)[0]

                    return await asyncio.get_event_loop().run_in_executor(
                        executor, _process
                    )

                # Initialize prediction arrays
                metadata_path = os.path.join(model_dir, model_config["metadata"])
                metadata = load_json_metadata(metadata_path)
                tag_labels = metadata["classes"]
                num_classes = len(tag_labels)
                weighted_sum = np.zeros(num_classes)
                total_weight = 0.0
                tag_counts = np.zeros(num_classes)

                # Process all segments concurrently
                segment_tasks = [process_segment(segment) for segment in segment_frames]
                segment_predictions_list = await asyncio.gather(*segment_tasks)

                # Process predictions
                for segment_predictions in segment_predictions_list:
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
            logger.error(f"Error processing {model_name}: {str(e)}")
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
        # "mtt_general": {
        #     "embedding": "discogs-effnet-bs64-1.pb",
        #     "tag": "mtt-discogs-effnet-1.pb",
        #     "metadata": "mtt-discogs-effnet-1.json",
        #     "input": "model/Placeholder",
        #     "output": "model/Sigmoid",
        #     "embedding_type": "effnet",
        # },
        # "mtt_track": {
        #     "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
        #     "tag": "mtt-discogs_track_embeddings-effnet-1.pb",
        #     "metadata": "mtt-discogs_track_embeddings-effnet-1.json",
        #     "input": "model/Placeholder",
        #     "output": "model/Sigmoid",
        #     "embedding_type": "effnet",
        # },
        # "msd": {
        #     "embedding": "msd-musicnn-1.pb",
        #     "tag": "msd-msd-musicnn-1.pb",
        #     "metadata": "msd-msd-musicnn-1.json",
        #     "input": "serving_default_model_Placeholder",
        #     "output": "PartitionedCall",
        #     "embedding_type": "musicnn",
        # },
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


async def predict_genre_from_qtrs(audio_file_path: str):
    """Predict genres from 4 equal segments of the audio file."""
    try:
        # Load audio
        audio = MonoLoader(
            filename=audio_file_path, sampleRate=16000, resampleQuality=4
        )()

        # Split into 4 equal segments
        total_samples = len(audio)
        segment_size = total_samples // 4
        segments = [audio[i * segment_size : (i + 1) * segment_size] for i in range(4)]

        all_results = {}
        executor = ThreadPoolExecutor(max_workers=4)

        for model_name, model_data in _LOADED_MODELS["genre"].items():
            if "error" in model_data:
                all_results[model_name] = model_data
                continue

            try:
                num_classes = len(model_data["metadata"]["classes"])
                segment_predictions = []

                # Process each quarter segment
                async def process_segment(segment):
                    def _process():
                        normalized = normalize_audio(segment)
                        embeddings = model_data["embedding"](normalized)
                        return model_data["prediction"](embeddings)[0]

                    return await asyncio.get_event_loop().run_in_executor(
                        executor, _process
                    )

                # Process segments
                for segment in segments:
                    predictions = await process_segment(segment)
                    segment_predictions.append(predictions)

                # Average predictions across segments
                averaged = np.mean(segment_predictions, axis=0)

                # Get top genres
                top_indices = np.argsort(averaged)[-15:][::-1]
                top_genres = [
                    (
                        model_data["metadata"]["classes"][i],
                        float(averaged[i]),
                    )
                    for i in top_indices
                    if averaged[i] > 0.07
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
        logger.error(f"Error in predict_genre_from_qtrs: {str(e)}")
        raise


async def predict_tags_from_qtrs(audio_file_path: str):
    """Predict tags from 4 equal segments of the audio file."""
    try:
        # Load audio
        audio = MonoLoader(
            filename=audio_file_path, sampleRate=16000, resampleQuality=4
        )()

        # Split into 4 equal segments
        total_samples = len(audio)
        segment_size = total_samples // 4
        segments = [audio[i * segment_size : (i + 1) * segment_size] for i in range(4)]

        all_results = {}
        executor = ThreadPoolExecutor(max_workers=4)

        for model_name, model_data in _LOADED_MODELS["tag"].items():
            try:
                batch_size = model_data.get("batch_size", 64)
                embedding_size = model_data.get("embedding_size", 512)

                def process_segment(segment):
                    normalized = normalize_audio(segment)
                    embeddings = model_data["embedding"](normalized)

                    # Reshape embeddings to match expected dimensions
                    if embeddings.shape[0] != batch_size:
                        pad_size = batch_size - embeddings.shape[0]
                        if pad_size > 0:
                            # Pad with zeros if needed
                            embeddings = np.pad(
                                embeddings, ((0, pad_size), (0, 0)), mode="constant"
                            )
                        else:
                            # Truncate if too large
                            embeddings = embeddings[:batch_size]

                    return model_data["prediction"](embeddings)[0]

                # Process segments concurrently
                segment_tasks = [
                    asyncio.get_event_loop().run_in_executor(
                        executor, process_segment, segment
                    )
                    for segment in segments
                ]
                segment_predictions = await asyncio.gather(*segment_tasks)

                # Average predictions across segments
                averaged = np.mean(segment_predictions, axis=0)

                # Format results
                threshold = 0.07
                top_indices = np.argsort(averaged)[-15:][::-1]
                top_tags = [
                    (model_data["classes"][i], float(averaged[i]))
                    for i in top_indices
                    if averaged[i] > threshold
                ]

                all_results[model_name] = {
                    tag: round(confidence, 2) for tag, confidence in top_tags
                }

            except Exception as e:
                logger.error(f"Error processing {model_name}: {str(e)}")
                all_results[model_name] = {"error": str(e)}

        return all_results

    except Exception as e:
        logger.error(f"Error in predict_tags_from_qtrs: {str(e)}")
        raise


def reshape_embeddings(embeddings, target_shape=(1280, 512)):
    """Reshape embeddings to match expected input size."""
    if embeddings.shape != target_shape:
        padded = np.zeros(target_shape)
        # Copy as much of the original data as possible
        min_rows = min(embeddings.shape[0], target_shape[0])
        min_cols = min(embeddings.shape[1], target_shape[1])
        padded[:min_rows, :min_cols] = embeddings[:min_rows, :min_cols]
        return padded
    return embeddings


def reshape_embeddings_for_prediction(embeddings, batch_size=64, embedding_size=512):
    """Reshape embeddings to match the model's expected input shape."""
    if embeddings.shape[1] != embedding_size:
        raise ValueError(
            f"Embedding size mismatch. Expected {embedding_size}, got {embeddings.shape[1]}"
        )

    # If we have more than batch_size embeddings, average them in groups
    if embeddings.shape[0] > batch_size:
        # Reshape to handle the excess embeddings
        n_chunks = embeddings.shape[0] // batch_size + (
            1 if embeddings.shape[0] % batch_size else 0
        )
        chunks = np.array_split(embeddings, n_chunks)
        # Average each chunk
        embeddings = np.stack(
            [chunk.mean(axis=0) if len(chunk) > 1 else chunk[0] for chunk in chunks]
        )

    # If we still have too many, take the first batch_size
    if embeddings.shape[0] > batch_size:
        embeddings = embeddings[:batch_size]
    # If we have too few, pad with zeros
    elif embeddings.shape[0] < batch_size:
        padding = np.zeros((batch_size - embeddings.shape[0], embedding_size))
        embeddings = np.vstack([embeddings, padding])

    return embeddings


def predict_tags_from_qtrs_internal(segments):
    """Internal function to get raw tag predictions from segments."""
    try:
        if "tag" not in _LOADED_MODELS:
            logger.error("Tag models not loaded")
            raise KeyError("Tag models not loaded")

        model_data = _LOADED_MODELS["tag"]["mtg_jamendo_track"]

        # Initialize prediction arrays
        tag_labels = model_data["classes"]
        num_classes = len(tag_labels)
        weighted_sum = np.zeros(num_classes)
        total_weight = 0.0
        tag_counts = np.zeros(num_classes)

        # Process each segment
        for segment in segments:
            try:
                normalized = normalize_audio(segment)
                embeddings = model_data["embedding"](normalized)

                # Reshape embeddings to match expected dimensions
                embeddings = reshape_embeddings_for_prediction(
                    embeddings,
                    batch_size=model_data.get("batch_size", 64),
                    embedding_size=model_data.get("embedding_size", 512),
                )

                predictions = model_data["prediction"](embeddings)[0]
                weight = np.max(predictions)
                weighted_sum += predictions * weight
                total_weight += weight
                tag_counts += predictions > 0.07

            except Exception as e:
                logger.warning(f"Error processing segment: {str(e)}")
                continue

        # Calculate final predictions
        if total_weight > 0:
            averaged_predictions = weighted_sum / total_weight
        else:
            averaged_predictions = weighted_sum

        frequency_weight = 0.2
        predictions = averaged_predictions + frequency_weight * (
            tag_counts / len(segments)
        )

        # Get top predictions
        threshold = 0.07
        top_indices = np.argsort(predictions)[-15:][::-1]
        top_tags = [
            (tag_labels[i], float(predictions[i]))
            for i in top_indices
            if predictions[i] > threshold
        ]

        # Format results
        formatted_results = {tag: round(confidence, 2) for tag, confidence in top_tags}
        return formatted_results

    except Exception as e:
        logger.error(f"Error in predict_tags_from_qtrs_internal: {str(e)}")
        raise


def predict_genres_from_qtrs_internal(segments):
    """Internal function to get raw genre predictions from segments."""
    try:
        if "genre" not in _LOADED_MODELS:
            logger.error("Genre models not loaded")
            return {}

        model_data = _LOADED_MODELS["genre"]["discogs400"]
        genre_labels = model_data["classes"]

        # Initialize arrays for predictions
        all_predictions = []

        for segment in segments:
            try:
                # Normalize audio segment
                normalized = normalize_audio(segment)

                # Get embeddings
                embeddings = model_data["embedding"](normalized)
                logger.info(f"Original embeddings shape: {embeddings.shape}")

                # If embeddings are (400, 512), reshape to (64, 512)
                if embeddings.shape[1] == 512:
                    # Reshape to handle the size mismatch
                    if embeddings.shape[0] > 64:
                        # Average the embeddings to get 64 vectors
                        embeddings = embeddings.reshape(
                            -1, embeddings.shape[0] // 64, 512
                        ).mean(axis=1)
                    elif embeddings.shape[0] < 64:
                        # Pad with zeros
                        padding = np.zeros((64 - embeddings.shape[0], 512))
                        embeddings = np.vstack([embeddings, padding])

                logger.info(f"Reshaped embeddings shape: {embeddings.shape}")

                # Get predictions
                predictions = model_data["prediction"](embeddings)[0]
                all_predictions.append(predictions)

            except Exception as e:
                logger.warning(
                    f"Error processing segment for genre prediction: {str(e)}"
                )
                continue

        if not all_predictions:
            logger.error("No valid predictions generated")
            return {}

        # Average predictions across segments
        averaged_predictions = np.mean(all_predictions, axis=0)

        # Get top predictions
        threshold = 0.07
        top_indices = np.argsort(averaged_predictions)[-15:][::-1]
        top_genres = [
            (genre_labels[i], float(averaged_predictions[i]))
            for i in top_indices
            if averaged_predictions[i] > threshold
        ]

        # Format results
        return {genre: round(confidence, 2) for genre, confidence in top_genres}

    except Exception as e:
        logger.error(f"Error in predict_genres_from_qtrs_internal: {str(e)}")
        return {}


def predict_mood_themes_from_qtrs_internal(segments):
    """Internal function to get raw mood predictions from segments."""
    try:
        if "mood_theme" not in _LOADED_MODELS:
            logger.error("Mood theme models not loaded")
            raise KeyError("Mood theme models not loaded")

        model_data = _LOADED_MODELS["mood_theme"]["track_level"]

        # Initialize prediction arrays
        mood_labels = model_data["classes"]
        num_classes = len(mood_labels)
        weighted_sum = np.zeros(num_classes)
        total_weight = 0.0
        mood_counts = np.zeros(num_classes)

        # Process each segment
        for segment in segments:
            normalized = normalize_audio(segment)
            embeddings = model_data["embedding"](normalized)

            # Debug logging
            logger.info(f"Embeddings shape: {embeddings.shape}")

            # Reshape embeddings if needed
            if embeddings.shape[0] != 1280:
                padded_embeddings = np.zeros((1280, embeddings.shape[1]))
                padded_embeddings[: embeddings.shape[0], :] = embeddings
                embeddings = padded_embeddings

            predictions = model_data["prediction"](embeddings)[0]
            weight = np.max(predictions)
            weighted_sum += predictions * weight
            total_weight += weight
            mood_counts += predictions > 0.07

        # Calculate final predictions
        if total_weight > 0:
            averaged_predictions = weighted_sum / total_weight
        else:
            averaged_predictions = weighted_sum

        frequency_weight = 0.2
        predictions = averaged_predictions + frequency_weight * (
            mood_counts / len(segments)
        )

        # Get top predictions
        threshold = 0.07
        top_indices = np.argsort(predictions)[-15:][::-1]
        top_moods = [
            (mood_labels[i], float(predictions[i]))
            for i in top_indices
            if predictions[i] > threshold
        ]

        # Format results
        formatted_results = {
            mood: round(confidence, 2) for mood, confidence in top_moods
        }

        return formatted_results

    except Exception as e:
        logger.error(f"Error in predict_mood_themes_from_qtrs_internal: {str(e)}")
        raise


async def analyze_audio_quick(audio_file_path: str) -> Dict[str, Any]:
    """Quick analysis of audio file."""
    try:
        # Load audio
        audio = MonoLoader(
            filename=audio_file_path, sampleRate=16000, resampleQuality=4
        )()

        # Split into 4 equal segments
        total_samples = len(audio)
        segment_size = total_samples // 4
        segments = [audio[i * segment_size : (i + 1) * segment_size] for i in range(4)]

        # For now, only process genre predictions
        executor = ThreadPoolExecutor(max_workers=4)

        # Run genre prediction only (no more asyncio.gather)
        raw_genre_results = await asyncio.get_event_loop().run_in_executor(
            executor, lambda: predict_genres_from_qtrs_internal(segments)
        )

        # Return results
        return {
            "source": "soundcloud",  # or whatever the source is
            "status": "success",
            "analysis_type": "quick",
            "results": {
                "genres": raw_genre_results if raw_genre_results else {},
                "tags": {},  # Empty for now
                "mood_themes": {},  # Empty for now
            },
        }

    except Exception as e:
        logger.error(f"Error in analyze_audio_quick: {str(e)}")
        raise RuntimeError(str(e))
