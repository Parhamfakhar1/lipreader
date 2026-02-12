
# LipReader

A lightweight, CPU-only lip reading toolkit for command recognition from video.  
No GPU required — runs efficiently on Intel i5 and similar systems.

## ✨ Features

- **CPU-only**: No GPU or deep learning dependencies.
- **CLI & API**: Use via command line or import as a Python library.
- **Trainable**: Learn custom lip motion patterns from your own videos.
- **JSON-based**: All data stored in human-readable JSON format.
- **Real-time ready**: Optimized for low-latency inference.

## 📦 Installation

Install in development mode (recommended):

```bash
pip install lipreader
```

> Requires: Python 3.7+, OpenCV, NumPy

## 🚀 Usage

### Train a new command

```bash
lipreader train --video start.mp4 --word start
```

You can train the same word multiple times with different videos:

```bash
lipreader train -v start1.mp4 -w start
lipreader train -v start2.mp4 -w start
```

### Predict from a video

```bash
lipreader predict --video test.mp4
```

**Sample output:**
```
🎯 Prediction: start

📈 Probabilities:
   start: 86.3%
   stop: 13.7%
```

### CLI Options

| Flag | Description |
|------|-------------|
| `-v`, `--video` | Path to input video (MP4, AVI, etc.) |
| `-w`, `--word` | Label for training (e.g., "start", "stop") |
| `-d`, `--data` | Path to JSON data file (default: `lip_data.json`) |

## 💻 Python API

Use `LipReader` directly in your code:

```python
from lipreader import LipReader

# Initialize
reader = LipReader("commands.json")

# Train
reader.train("start.mp4", "start")

# Predict
predicted_word, probabilities = reader.predict("unknown.mp4")
print(f"Detected: {predicted_word}")
```

## 🗃️ Data Format

All trained patterns are saved in `lip_data.json`:

```json
{
  "start": {
    "samples": [
      {
        "avg_ratio": 1.28,
        "ratio_std": 0.25,
        "min_ratio": 0.78,
        "max_ratio": 1.88,
        "frame_count": 120,
        "video": "start1.mp4"
      }
    ]
  }
}
```

## ⚠️ Limitations

- Works best in **good lighting** with **front-facing video**.
- Accuracy depends on **clear lip motion** (silent articulation works).
- Not designed for full-sentence lip reading — optimized for **short commands**.

## 📄 License

MIT License
```
