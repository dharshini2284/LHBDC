# LHBDC: Learned Hierarchical Bi-Directional Compression 🎥

## 📝 Project Overview

LHBDC is a video compression and decompression system developed in Python. It leverages motion estimation and bi-directional compensation to enhance compression efficiency. The system integrates RAFT optical flow for frame-to-frame motion estimation, residual encoding for improved compression, and multi-frame compensation for accurate video reconstruction. A Tkinter-based GUI provides an intuitive interface for handling video file input and output.

## 🚀 Features

- **Motion Estimation:** Uses RAFT optical flow for precise frame analysis.
- **Bi-Directional Compensation:** Improves compression by leveraging both past and future frames.
- **Residual Encoding:** Reduces redundant data for enhanced efficiency.
- **Key Frame Encoding/Decoding:** Maintains high-quality reference frames.
- **Multi-Frame Compensation:** Enhances accuracy in video reconstruction.
- **GUI Integration:** Built with Tkinter for easy video file handling.
- **Pickle-based Compression Storage:** Saves compressed data efficiently.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Motion Estimation:** RAFT Optical Flow
- **GUI Framework:** Tkinter
- **Data Storage:** Pickle
- **Video Processing:** OpenCV, NumPy

## 📌 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/dharshini2284/LHBDC.git
cd LHBDC
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application

```bash
python dc_package.py
```

## 🎯 Future Enhancements

- Improve compression efficiency using deep learning techniques.
- Optimize keyframe selection for better quality retention.
- Implement GPU acceleration for faster processing.

## 📬 Contact

For any queries or suggestions, feel free to reach out!

- **GitHub:** [@dharshini2284](https://github.com/dharshini2284)
- **Email:** [004dharshkumar@gmail.com](mailto:004dharshkumar@gmail.com)

