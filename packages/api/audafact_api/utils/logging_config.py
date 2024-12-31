import logging
import warnings
import os
import tensorflow as tf

def configure_logging():
    # 1. Suppress TensorFlow warnings - multiple approaches
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress all TF logging
    tf.get_logger().setLevel(logging.ERROR)  # Set TF logger to error only
    logging.getLogger("tensorflow").setLevel(logging.ERROR)  # Another way to suppress TF

    # 2. Suppress Python warnings
    warnings.filterwarnings('ignore')
    
    # 3. Configure basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 4. Set Essentia logging level (using property instead of method)
    from essentia import log as essentia_logger
    essentia_logger.warningLevel = 0

    # 5. Disable Autograph logging
    os.environ['AUTOGRAPH_VERBOSITY'] = '0'

    # 6. Additional TF specific suppressions
    try:
        # For TF 2.x
        tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
    except:
        pass
