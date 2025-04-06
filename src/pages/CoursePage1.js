import React, { useRef, useEffect, useState } from "react";
import "./CoursePage1.css";
import Navbar from "./Navbar";

const CoursePage1 = () => {
  const videoRef = useRef(null);
  const audioContextRef = useRef(null);
  const analyserRef = useRef(null);
  const dataArrayRef = useRef(null);

  const [mouthHeight, setMouthHeight] = useState(3);
  const [lipCurve, setLipCurve] = useState(85);
  const [messages, setMessages] = useState([]);
  const [emotion, setEmotion] = useState("");
  const [videoHeight, setVideoHeight] = useState(0);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === "speech") {
          setMessages((prev) => [...prev, `You said: ${data.text}`]);
        } else if (data.type === "response") {
          setMessages((prev) => [...prev, `AI: ${data.text}`]);
        } else if (data.type === "emotion") {
          setEmotion(data.emotion);
        } else if (data.type === "pause") {
          videoRef.current?.pause();
          setMessages((prev) => [...prev, `🛑 Video paused`]);
        } else if (data.type === "resume") {
          videoRef.current?.play();
          setMessages((prev) => [...prev, `▶️ Video resumed`]);
        }
      } catch (err) {
        console.error("WebSocket error:", err);
      }
    };

    return () => ws.close();
  }, []);

  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.addEventListener("play", setupAudioAnalysis);
      setVideoHeight(videoRef.current.clientHeight);
    }
    return () => {
      if (videoRef.current) {
        videoRef.current.removeEventListener("play", setupAudioAnalysis);
      }
    };
  }, []);

  const setupAudioAnalysis = () => {
    if (!audioContextRef.current) {
      audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      analyserRef.current.fftSize = 128;

      const source = audioContextRef.current.createMediaElementSource(videoRef.current);
      source.connect(analyserRef.current);
      analyserRef.current.connect(audioContextRef.current.destination);

      dataArrayRef.current = new Uint8Array(analyserRef.current.frequencyBinCount);
      requestAnimationFrame(updateMouthAnimation);
    }
  };

  const updateMouthAnimation = () => {
    if (analyserRef.current) {
      analyserRef.current.getByteFrequencyData(dataArrayRef.current);
      const avgFrequency = dataArrayRef.current.reduce((a, b) => a + b, 0) / dataArrayRef.current.length;
      setMouthHeight(Math.min(20, Math.max(3, avgFrequency / 7)));
      setLipCurve(85 - avgFrequency / 10);
      requestAnimationFrame(updateMouthAnimation);
    }
  };

  const getEmotionColor = () => {
    switch (emotion) {
      case "happy": return "yellow";
      case "sad": return "blue";
      case "angry": return "red";
      default: return "black";
    }
  };

  return (
    <div className="course-container">
      <Navbar />
      <div className="course-content">
        <div className="video-section">
          <video
            ref={videoRef}
            className="course-video"
            controls
            onLoadedMetadata={() => setVideoHeight(videoRef.current.clientHeight)}
          >
            <source src="/vid.mp4" type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="avatar-section">
          <div className="avatar-wrapper">
            <img src="/bb.png" alt="Avatar" className="avatar-image" />
            <div className="mouth-overlay" style={{ height: videoHeight }}>
              <svg width="55" height="82" viewBox="0 0 200 150" transform="rotate(180)">
                <path d={`M50 ${lipCurve} Q100 40 150 ${lipCurve}`} fill={getEmotionColor()} stroke="rgb(199, 108, 122)" strokeWidth="5" />
                <path d={`M50 85 Q100 ${85 + mouthHeight} 150 85`} fill="rgb(218, 160, 139)" stroke="rgb(199, 108, 122)" strokeWidth="5" />
                <path d={`M70 88 Q100 ${88 + mouthHeight} 130 88`} fill="rgb(180, 80, 100)" />
              </svg>
            </div>
          </div>
          <div className="message-box">
            {messages.map((msg, idx) => (
              <div key={idx} className="message">{msg}</div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CoursePage1;
