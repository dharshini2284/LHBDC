# -*- coding: utf-8 -*-
"""dc_package

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1i-p2WqTs30cN6wWyQfNHUgH10Wr7pJXj
"""

import torch
import torch.nn as nn
import numpy as np
import cv2
from torchvision.models.optical_flow import raft_small

# Load video and save compressed data
def load_video(file_path):
    cap = cv2.VideoCapture(file_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Convert to RGB format
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    cap.release()
    return frames

# Save the reconstructed frames to a video
def save_video(file_path, frames, fps=30):
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    for frame in frames:
        # Convert back to BGR format
        out.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    out.release()

# Simple example functions for key frame encoding/decoding
def encode_key_frame(frame):
    # Placeholder: Compress key frame (you can replace with actual model)
    return frame

def decode_key_frame(compressed_frame):
    # Placeholder: Decompress key frame (you can replace with actual model)
    return compressed_frame

# Placeholder for motion estimation
def estimate_flow(frame1, frame2):
    model = raft_small(weights="Raft_Small_Weights.DEFAULT").eval()  # Using weights
    transform = nn.functional.interpolate
    frame1_tensor = torch.from_numpy(frame1).float().permute(2, 0, 1).unsqueeze(0) / 255.0
    frame2_tensor = torch.from_numpy(frame2).float().permute(2, 0, 1).unsqueeze(0) / 255.0
    # Reshape to match RAFT input requirements
    frame1_tensor = transform(frame1_tensor, size=(256, 256), mode='bilinear')
    frame2_tensor = transform(frame2_tensor, size=(256, 256), mode='bilinear')

    with torch.no_grad():
        flow_forward = model(frame1_tensor, frame2_tensor)[0]  # Flow from frame1 to frame2
        flow_backward = model(frame2_tensor, frame1_tensor)[0]  # Flow from frame2 to frame1

    return flow_forward, flow_backward  # Return both flows


# Simple blending compensation
def bi_directional_compensation(frame1, frame2, forward_flow, backward_flow):
    # Placeholder: Combine frame1 and frame2 using motion flows
    return (frame1 // 2 + frame2 // 2)

# Simple residual encoding/decoding
def encode_residual(residual):
    # Placeholder: Encode residual
    return residual

def decode_residual(encoded_residual):
    # Placeholder: Decode residual
    return encoded_residual

# Encode a video using the LHBDC-inspired method
def encode_video(frames, gop_size=8):
    compressed_frames = []
    num_frames = len(frames)

    for i in range(0, num_frames, gop_size):
        key_frame = frames[i]
        # Encode key frame
        compressed_key_frame = encode_key_frame(key_frame)
        compressed_frames.append(compressed_key_frame)

        # Determine the last frame in the current GOP safely
        end_frame_index = min(i + gop_size - 1, num_frames - 1)

        # Process bi-directional frames within the GOP
        for j in range(1, gop_size):
            if i + j >= num_frames:
                break
            frame = frames[i + j]

            # Use the last valid frame for flow estimation
            forward_flow, backward_flow = estimate_flow(frames[i], frames[end_frame_index])

            # Perform bi-directional compensation
            compensated_frame = bi_directional_compensation(frames[i], frames[end_frame_index], forward_flow, backward_flow)
            residual = frame - compensated_frame
            encoded_residual = encode_residual(residual)
            compressed_frames.append((forward_flow, backward_flow, encoded_residual))

    return compressed_frames


# Decode a video using the LHBDC-inspired method
def decode_video(compressed_frames, gop_size=8):
    reconstructed_frames = []
    num_compressed_frames = len(compressed_frames)

    for i in range(0, num_compressed_frames, gop_size):
        key_frame = decode_key_frame(compressed_frames[i])
        reconstructed_frames.append(key_frame)

        # Determine the last frame in the current GOP safely
        end_frame_index = min(i + gop_size - 1, num_compressed_frames - 1)

        # Decode bi-directional frames
        for j in range(1, gop_size):
            if i + j >= num_compressed_frames:
                break
            forward_flow, backward_flow, encoded_residual = compressed_frames[i + j]

            # Ensure the end reference frame is within bounds
            if len(reconstructed_frames) <= end_frame_index:
                end_reference_index = len(reconstructed_frames) - 1
            else:
                end_reference_index = end_frame_index

            # Compensate using the closest available reconstructed frames
            compensated_frame = bi_directional_compensation(reconstructed_frames[i], reconstructed_frames[end_reference_index], forward_flow, backward_flow)
            residual = decode_residual(encoded_residual)
            frame = compensated_frame + residual
            reconstructed_frames.append(frame)

    return reconstructed_frames


# Main function to load video, compress, and decompress
import pickle

def main(input_video_path, output_compressed_path, output_decompressed_path):
    frames = load_video(input_video_path)

    # Encode video
    print("Encoding video...")
    compressed_frames = encode_video(frames)
    print("Encoding completed...")

    # Decode video
    print("Decoding video...")
    reconstructed_frames = decode_video(compressed_frames)
    print("Decoding completed...")

    # Save compressed data using pickle
    with open(output_compressed_path, 'wb') as f:
        pickle.dump(compressed_frames, f)  # Save the compressed frames

    # Save reconstructed video
    save_video(output_decompressed_path, reconstructed_frames)

# Run the example
input_video_path = "/content/sample_data/video.mp4"
output_compressed_path = "compressed_video.pkl"  # Change the extension to .pkl
output_decompressed_path = "decompressed_video.mp4"
main(input_video_path, output_compressed_path, output_decompressed_path)