from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from essentia.standard import (
    MonoLoader,
    TensorflowPredictEffnetDiscogs,
    TensorflowPredict2D,
    FrameGenerator,
)
import numpy as np
import json
import os
import tempfile
import yt_dlp
from urllib.parse import quote

app = FastAPI(
    title="Audio Genre API",
    description="API for audio genre classification and analysis",
    docs_url=None,
    redoc_url=None,
)


def load_json_metadata(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


def normalize_audio(segment):
    max_val = np.max(np.abs(segment))
    if max_val > 0:
        return segment / max_val
    return segment


def download_audio_from_url(url):
    try:
        temp_dir = tempfile.gettempdir()
        temp_audio_path = os.path.join(temp_dir, "downloaded_audio.wav")
        print(f"Temporary file path: {temp_audio_path}")

        ydl_opts = {
            "format":
            "bestaudio[ext=m4a]/best",
            "outtmpl":
            temp_audio_path,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                    "preferredquality": "192",
                },
            ],
            "verbose":
            True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
            if result != 0:
                raise Exception("yt-dlp failed to download audio")

        final_audio_path = f"{temp_audio_path}.wav"
        if not os.path.exists(final_audio_path):
            raise Exception("Failed to save downloaded audio")

        return final_audio_path

    except Exception as e:
        print(f"Error during audio download: {str(e)}")
        raise HTTPException(status_code=500,
                            detail="Failed to download audio from URL")


def predict_genre_from_segments(audio_file_path, model_dir, segment_length=45):
    model_dir = os.path.abspath(model_dir)
    print(f"Loading audio file from: {audio_file_path}")
    audio = MonoLoader(filename=audio_file_path,
                       sampleRate=16000,
                       resampleQuality=4)()
    frame_size = int(16000 * segment_length)
    segment_frames = list(
        FrameGenerator(audio,
                       frameSize=frame_size,
                       hopSize=frame_size // 2,
                       startFromZero=True))

    embedding_model_path = os.path.join(model_dir, "discogs-effnet-bs64-1.pb")
    embedding_model = None

    genre_model_path = os.path.join(model_dir,
                                    "genre_discogs400-discogs-effnet-1.pb")
    genre_model = None

    genre_metadata_path = os.path.join(
        model_dir, "genre_discogs400-discogs-effnet-1.json")
    genre_metadata = load_json_metadata(genre_metadata_path)
    genre_labels = genre_metadata["classes"]

    all_predictions = []
    weighted_sum = np.zeros(400)
    total_weight = 0.0
    genre_counts = np.zeros(400)

    for i, segment in enumerate(segment_frames):
        print(
            f"Generating embeddings for segment {i+1}/{len(segment_frames)}..."
        )
        normalized_segment = normalize_audio(segment)

        if embedding_model is None:
            print(f"Loading embedding model from: {embedding_model_path}")
            embedding_model = TensorflowPredictEffnetDiscogs(
                graphFilename=embedding_model_path, output="PartitionedCall:1")

        embeddings = embedding_model(normalized_segment)

        if genre_model is None:
            print(f"Loading genre prediction model from: {genre_model_path}")
            genre_model = TensorflowPredict2D(
                graphFilename=genre_model_path,
                input="serving_default_model_Placeholder",
                output="PartitionedCall:0",
            )

        predictions = genre_model(embeddings)[0]
        weight = np.max(predictions)
        weighted_sum += predictions * weight
        total_weight += weight
        genre_counts += predictions > 0.07
        all_predictions.append(predictions)

    if total_weight > 0:
        averaged_predictions = weighted_sum / total_weight
    else:
        averaged_predictions = weighted_sum

    frequency_weight = 0.2
    refined_predictions = averaged_predictions + frequency_weight * (
        genre_counts / len(segment_frames))

    threshold = 0.07
    top_indices = np.argsort(refined_predictions)[-15:][::-1]
    top_genres = [(genre_labels[i], float(refined_predictions[i]))
                  for i in top_indices if refined_predictions[i] > threshold]

    formatted_genres = {}
    for genre_label, confidence in top_genres:
        umbrella_genre, sub_genre = genre_label.split("---")
        if umbrella_genre not in formatted_genres:
            formatted_genres[umbrella_genre] = {}
        formatted_genres[umbrella_genre][sub_genre] = round(confidence, 2)

    return formatted_genres


class URLInput(BaseModel):
    url: str


@app.get("/genres/{url:path}")
async def get_genres_by_url(url: str):
    try:
        print(f"Processing URL: {url}")
        audio_file_path = download_audio_from_url(url)

        model_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "models")
        genre_predictions = predict_genre_from_segments(
            audio_file_path, model_directory)
        return JSONResponse(content={"genres": genre_predictions})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'audio_file_path' in locals(
        ) and audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
            except Exception as e:
                print(f"Error removing temporary file: {str(e)}")


@app.post("/genres")
async def get_genres_by_file(file: UploadFile = File(...)):
    try:
        print("Processing uploaded file")
        with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
            temp_audio.write(await file.read())
            audio_file_path = temp_audio.name
        model_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "models")
        genre_predictions = predict_genre_from_segments(
            audio_file_path, model_directory)
        return JSONResponse(content={"genres": genre_predictions})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'audio_file_path' in locals(
        ) and audio_file_path and os.path.exists(audio_file_path):
            try:
                os.remove(audio_file_path)
            except Exception as e:
                print(f"Error removing temporary file: {str(e)}")
