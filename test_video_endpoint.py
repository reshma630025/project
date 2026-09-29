import cv2
import numpy as np
import tempfile
import os
import urllib.request
import json

def test_video():
    print("Testing Video Frame-by-Frame Analysis Endpoint...", flush=True)
    temp_mp4 = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_path = temp_mp4.name
    temp_mp4.close()

    # Create 2 seconds of 10fps video with simulated face-like oval
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_path, fourcc, 10.0, (200, 200))
    for i in range(20):
        frame = np.full((200, 200, 3), 40 + i * 5, dtype=np.uint8)
        # draw simulated face circle
        cv2.circle(frame, (100, 100), 50, (180, 200, 220), -1)
        cv2.circle(frame, (85, 90), 8, (40, 40, 40), -1)
        cv2.circle(frame, (115, 90), 8, (40, 40, 40), -1)
        out.write(frame)
    out.release()

    with open(temp_path, 'rb') as f:
        video_bytes = f.read()
    os.remove(temp_path)

    boundary = "----WebKitFormBoundaryVideoTest789"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode('utf-8'))
    body.extend(b'Content-Disposition: form-data; name="video"; filename="test_sample.mp4"\r\n')
    body.extend(b"Content-Type: video/mp4\r\n\r\n")
    body.extend(video_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode('utf-8'))

    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/analyze/video",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode('utf-8'))

    print(f"Video Result: {res.get('classification')} ({res.get('classification_label')})", flush=True)
    print(f"Total Frames: {res.get('total_frames')}, Analyzed Frames: {res.get('analyzed_frames')}, Suspicious: {res.get('suspicious_frames')}", flush=True)
    print(f"Frame Results: {len(res.get('frame_results', []))} frames", flush=True)
    if res.get('frame_results'):
        for fr in res['frame_results'][:3]:
            print(f"  Frame #{fr['frame_number']} @ {fr['timestamp']}s -> {fr['prediction']} ({fr['confidence']}%)", flush=True)
    assert res.get("analyzed_frames", 0) > 0
    print("VIDEO ENDPOINT TEST PASSED SUCCESSFULLY!", flush=True)

if __name__ == "__main__":
    test_video()
