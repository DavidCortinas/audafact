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

logger = logging.getLogger(__name__)


def normalize_audio(segment):
    max_val = np.max(np.abs(segment))
    if max_val > 0:
        return segment / max_val
    return segment


def load_json_metadata(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def predict_genre_from_segments(audio_file_path, model_dir, segment_length=45):
    model_dir = os.path.abspath(model_dir)
    print(f"Loading audio file from: {audio_file_path}")

    # Define model configurations
    models = {
        "discogs400": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "genre": "genre_discogs400-discogs-effnet-1.pb",
            "metadata": "genre_discogs400-discogs-effnet-1.json",
            "input": "serving_default_model_Placeholder",
            "output": "PartitionedCall:0",
            "is_hierarchical": True,  # Uses umbrella/sub-genre format
        },
        "mtg_general": {
            "embedding": "discogs-effnet-bs64-1.pb",
            "genre": "mtg_jamendo_genre-discogs-effnet-1.pb",
            "metadata": "mtg_jamendo_genre-discogs-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "is_hierarchical": False,
        },
        "mtg_track": {
            "embedding": "discogs_track_embeddings-effnet-bs64-1.pb",
            "genre": "mtg_jamendo_genre-discogs_track_embeddings-effnet-1.pb",
            "metadata": "mtg_jamendo_genre-discogs_track_embeddings-effnet-1.json",
            "input": "model/Placeholder",
            "output": "model/Sigmoid",
            "is_hierarchical": False,
        },
    }

    # Load audio once
    audio = MonoLoader(filename=audio_file_path, sampleRate=16000, resampleQuality=4)()
    frame_size = int(16000 * segment_length)
    segment_frames = list(
        FrameGenerator(
            audio, frameSize=frame_size, hopSize=frame_size // 2, startFromZero=True
        )
    )

    all_results = {}

    for model_name, model_config in models.items():
        try:
            print(f"\nProcessing with {model_name} model...")

            # Initialize models
            embedding_model = None
            genre_model = None

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

            # Process segments
            for i, segment in enumerate(segment_frames):
                print(
                    f"Generating embeddings for segment {i+1}/{len(segment_frames)}..."
                )
                normalized_segment = normalize_audio(segment)

                # Load embedding model if needed
                if embedding_model is None:
                    embedding_model_path = os.path.join(
                        model_dir, model_config["embedding"]
                    )
                    print(f"Loading embedding model from: {embedding_model_path}")
                    embedding_model = TensorflowPredictEffnetDiscogs(
                        graphFilename=embedding_model_path, output="PartitionedCall:1"
                    )

                embeddings = embedding_model(normalized_segment)

                # Load genre model if needed
                if genre_model is None:
                    genre_model_path = os.path.join(model_dir, model_config["genre"])
                    print(f"Loading genre model from: {genre_model_path}")
                    genre_model = TensorflowPredict2D(
                        graphFilename=genre_model_path,
                        input=model_config["input"],
                        output=model_config["output"],
                    )

                predictions = genre_model(embeddings)[0]
                weight = np.max(predictions)
                weighted_sum += predictions * weight
                total_weight += weight
                genre_counts += predictions > 0.07
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
            threshold = 0.07
            top_indices = np.argsort(refined_predictions)[-15:][::-1]
            top_genres = [
                (genre_labels[i], float(refined_predictions[i]))
                for i in top_indices
                if refined_predictions[i] > threshold
            ]

            # Format results based on model type
            if model_config["is_hierarchical"]:
                # Format for Discogs400 (hierarchical)
                formatted_results = {}
                for genre_label, confidence in top_genres:
                    umbrella_genre, sub_genre = genre_label.split("---")
                    if umbrella_genre not in formatted_results:
                        formatted_results[umbrella_genre] = {}
                    formatted_results[umbrella_genre][sub_genre] = round(confidence, 2)
            else:
                # Format for MTG models (flat)
                formatted_results = {
                    genre_label: round(confidence, 2)
                    for genre_label, confidence in top_genres
                }

            all_results[model_name] = formatted_results

        except Exception as e:
            print(f"Error processing {model_name}: {str(e)}")
            all_results[model_name] = {"error": str(e)}

    return all_results


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
