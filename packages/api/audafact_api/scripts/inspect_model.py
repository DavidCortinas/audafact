import tensorflow as tf
import os
from ..core.config import settings


def inspect_model():
    # Get the model path from your settings
    model_dir = settings.MODEL_PATH
    mood_theme_model_path = os.path.join(
        model_dir, "mtg_jamendo_moodtheme-discogs-effnet-1.pb"
    )

    print(f"Loading model from: {mood_theme_model_path}")

    # Load and inspect the model
    model = tf.saved_model.load(mood_theme_model_path)
    print("\nModel Structure:")
    print("Model inputs:", model.signatures["serving_default"].inputs)
    print("Model outputs:", model.signatures["serving_default"].outputs)


if __name__ == "__main__":
    inspect_model()
