import logging
import sys
import os
import time
import asyncio
import json
from typing import Dict, Any

# Add the parent directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

from core.config import settings
from services.audio import predict_tags_from_segments

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def format_predictions(predictions: Dict[str, Any]) -> str:
    """Format predictions for pretty printing"""
    return json.dumps(predictions, indent=2)


async def test_tags_predictions(audio_path: str):
    """Test tags prediction on an audio file."""
    try:
        print(f"\nTesting file: {audio_path}")
        print("\nTesting predict_tags_from_segments...")
        start_time = time.time()

        # Call predict_tags_from_segments with model_dir
        results = await predict_tags_from_segments(
            audio_path, settings.MODEL_PATH, segment_length=45  # explicitly set default
        )

        execution_time = time.time() - start_time
        print(f"Time taken: {execution_time:.2f}s")
        print("Results:")
        print(format_predictions(results))

    except Exception as e:
        logger.error(f"Error in test: {str(e)}", exc_info=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_tags_prediction.py <path_to_audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]
    if not os.path.exists(audio_path):
        print(f"Error: File {audio_path} does not exist")
        sys.exit(1)

    print("Starting test script...")
    asyncio.run(test_tags_predictions(audio_path))
