import argparse
import sys
from .core import LipReader

def main():
    parser = argparse.ArgumentParser(
        description="Lip Reading CLI — Train and predict lip motion patterns.",
        prog="lipreader"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Train command
    train_parser = subparsers.add_parser("train", help="Train a word from video")
    train_parser.add_argument("--video", "-v", required=True, help="Input video path")
    train_parser.add_argument("--word", "-w", required=True, help="Target word/label")
    train_parser.add_argument("--data", "-d", default="lip_data.json", help="Data file")

    # Predict command
    pred_parser = subparsers.add_parser("predict", help="Predict word from video")
    pred_parser.add_argument("--video", "-v", required=True, help="Test video path")
    pred_parser.add_argument("--data", "-d", default="lip_data.json", help="Data file")

    args = parser.parse_args()

    try:
        reader = LipReader(args.data)

        if args.command == "train":
            stats = reader.train(args.video, args.word)
            print(f"✅ Trained word '{args.word}'")
            print(f"   Avg Ratio: {stats['avg_ratio']:.2f} ± {stats['ratio_std']:.2f}")

        elif args.command == "predict":
            pred, probs = reader.predict(args.video)
            if pred is None:
                print("⚠️ No match found.")
                sys.exit(1)
            print(f"🎯 Prediction: {pred}")
            print("\n📈 Probabilities:")
            for w in sorted(probs, key=probs.get, reverse=True):
                print(f"   {w}: {probs[w]:.1f}%")

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)