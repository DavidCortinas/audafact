# Music Genre Prediction API

This API allows you to analyze and predict music genres using audio files or YouTube URLs. It integrates several open-source tools and machine learning models to provide genre predictions based on your input.

## Key Features

- **Upload an audio file** or **provide a YouTube URL** to get genre predictions.
- Utilizes **TensorFlow** models for genre classification.
- Built with **FastAPI** for a scalable and user-friendly interface.

## Installation and Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/music-genre-api.git
    ```
2. Navigate to the project directory:
    ```bash
    cd music-genre-api
    ```
3. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5. Ensure **FFmpeg** is installed and available in your system path:
    - For macOS: `brew install ffmpeg`
    - For Linux: Install via your package manager, e.g., `apt install ffmpeg`
    - For Windows: Download FFmpeg from the [official site](https://ffmpeg.org/download.html) and add it to your PATH.

6. Start the server:
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

## API Usage

### Endpoints

#### POST `/get-genres`
- **Description**: Predict genres for an audio file or YouTube URL.
- **Parameters**:
  - `url` (query parameter, optional): YouTube URL of the audio to be analyzed.
  - `file` (multipart/form-data, optional): An audio file to be uploaded.
  - **Note**: Either `url` or `file` must be provided.

#### Example Request with File
```bash
curl -X POST "http://localhost:8000/get-genres" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@example_audio.wav"
```

#### Example Request with URL
```bash
curl -X POST "http://localhost:8000/get-genres?url=https://www.youtube.com/watch?v=example" \
  -H "accept: application/json"
```
# Licensing Information

This project integrates several open-source libraries, each with its own licensing terms. Below is a summary of the licenses governing the components used in this API:

## Essentia
- **License**: GNU Affero General Public License v3 (AGPLv3).
- **Essentia** is a library for audio analysis and music information retrieval.
- You must comply with the **AGPLv3**, which requires making the full source code of this project available if you make it publicly accessible (e.g., over a network).
- More information on licensing: [Essentia Licensing Information](https://essentia.upf.edu/licensing_information.html).

## yt-dlp
- **License**: MIT License and Unlicense.
- **yt-dlp** is used for downloading audio from YouTube.
- Both the **MIT License** and **Unlicense** allow free use, modification, and distribution of yt-dlp.
- License details can be found [here](https://github.com/yt-dlp/yt-dlp/blob/master/LICENSE).

## TensorFlow
- **License**: Apache License 2.0.
- **TensorFlow** is used to execute machine learning models for genre prediction.
- You must include a copy of the **Apache 2.0 License** and retain the attribution notice in any distribution.
- License details can be found [here](https://github.com/tensorflow/tensorflow/blob/master/LICENSE).

## Summary of Licensing Obligations

### AGPLv3 (Essentia)
- The **AGPLv3** license requires that the **entire source code** of this project must be open and available if you run it as a public service.
- If you distribute the software, you need to provide full source code, including any modifications.

### Apache 2.0 (TensorFlow)
- Ensure proper attribution is included.
- Keep the **Apache 2.0 License** as part of any distribution.
- Include patent grant clauses if applicable.

### MIT License and Unlicense (yt-dlp)
- There are no significant limitations, but you should include a copy of the **MIT License** and **Unlicense** when distributing.

## Providing Attribution and License Copies

In compliance with the licenses, this repository contains the following files:

- `LICENSES/AGPLv3.txt`: The full AGPLv3 license for Essentia.
- `LICENSES/Apache-2.0.txt`: The Apache 2.0 license for TensorFlow.
- `LICENSES/MIT.txt`: The MIT license for yt-dlp.
- `LICENSES/Unlicense.txt`: The Unlicense for yt-dlp.
- `NOTICE.txt`: Attribution notices for TensorFlow, yt-dlp, and Essentia.

### NOTICE Example
The `NOTICE.txt` file should include:
```
This product includes software developed by the Music Technology Group at Universitat Pompeu Fabra, Barcelona, as part of the Essentia library (AGPLv3).

This product includes software developed by the TensorFlow team, used under the Apache License, Version 2.0.

This product includes software developed by yt-dlp contributors, used under the MIT License and Unlicense.
```

## Commercial Licensing

If you plan to distribute this software without sharing the source code or wish to use it in a commercial context without adhering to the **AGPLv3** requirements, you may need to obtain a **commercial license** from the Essentia team. You can find more information on commercial licensing [here](https://essentia.upf.edu/licensing_information.html).

## Contributing

This project is open source and welcomes contributions. Please make sure to read and follow the licensing requirements outlined above when making contributions.

## Disclaimer

This software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, and noninfringement. In no event shall the authors be liable for any claim, damages, or other liability, whether in an action of contract, tort, or otherwise, arising from, out of, or in connection with the software or the use or other dealings in the software.

## Troubleshooting

### Common Issues

#### Audio Download Issues:
- Ensure **yt-dlp** is installed correctly and has the required permissions.
- Check that **FFmpeg** is available in your system path for proper post-processing.

#### License Compliance:
- Make sure all relevant license files are included when distributing the project.

#### Missing Dependencies:
- Ensure all Python dependencies are installed using the correct Python environment.


## Contact

For questions or licensing inquiries, please contact the maintainer at [david.g.cortinas@gmail.com].