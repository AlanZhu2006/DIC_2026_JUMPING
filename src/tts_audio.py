"""
TTS Audio Generation Module for Code2Video
Uses OpenAI TTS API to generate narration audio from lecture lines
"""

import os
import json
import subprocess
import pathlib
from typing import List, Optional, Tuple
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment


# Load config
_CFG_PATH = pathlib.Path(__file__).with_name("api_config.json")
with _CFG_PATH.open("r", encoding="utf-8") as _f:
    _CFG = json.load(_f)


def get_tts_config(key: str, default=None):
    """Get TTS configuration value"""
    return os.getenv(f"TTS_{key}".upper(), _CFG.get("tts", {}).get(key, default))


class TTSGenerator:
    """OpenAI TTS audio generator"""
    
    # Available voices: alloy, echo, fable, onyx, nova, shimmer
    VOICES = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: str = "tts-1",
        voice: str = "nova",
        speed: float = 1.0,
    ):
        """
        Initialize TTS generator
        
        Args:
            api_key: OpenAI API key (falls back to config or env)
            base_url: API base URL (falls back to config or env)
            model: TTS model ("tts-1" for standard, "tts-1-hd" for high quality)
            voice: Voice name (alloy, echo, fable, onyx, nova, shimmer)
            speed: Speech speed (0.25 to 4.0)
        """
        self.api_key = api_key or get_tts_config("api_key") or _CFG.get("gpt41", {}).get("api_key")
        self.base_url = base_url or get_tts_config("base_url") or "https://api.openai.com/v1"
        self.model = model or get_tts_config("model", "tts-1")
        self.voice = voice or get_tts_config("voice", "nova")
        self.speed = speed or get_tts_config("speed", 1.0)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        
    def generate_audio(
        self,
        text: str,
        output_path: str,
        voice: Optional[str] = None,
        speed: Optional[float] = None,
    ) -> str:
        """
        Generate TTS audio from text
        
        Args:
            text: Text to convert to speech
            output_path: Output file path (.mp3)
            voice: Override default voice
            speed: Override default speed
            
        Returns:
            Path to generated audio file
        """
        voice = voice or self.voice
        speed = speed or self.speed
        
        try:
            response = self.client.audio.speech.create(
                model=self.model,
                voice=voice,
                input=text,
                speed=speed,
                response_format="mp3",
            )
            
            response.stream_to_file(output_path)
            print(f"🔊 Audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ TTS generation failed: {e}")
            raise
    
    def generate_section_audio(
        self,
        section_id: str,
        lecture_lines: List[str],
        output_dir: Path,
        voice: Optional[str] = None,
        add_pauses: bool = True,
    ) -> str:
        """
        Generate audio for a video section from lecture lines
        
        Args:
            section_id: Section identifier (e.g., "section_1")
            lecture_lines: List of narration text lines
            output_dir: Directory to save audio files
            voice: Override default voice
            add_pauses: Add short pauses between lines
            
        Returns:
            Path to the combined audio file for the section
        """
        if not lecture_lines:
            print(f"⚠️ No lecture lines for {section_id}, skipping audio generation")
            return None
            
        output_dir = Path(output_dir)
        audio_dir = output_dir / "audio"
        audio_dir.mkdir(exist_ok=True)
        
        # Generate audio for each line
        line_audio_files = []
        for i, line in enumerate(lecture_lines):
            line_audio_path = audio_dir / f"{section_id}_line_{i+1}.mp3"
            
            if line_audio_path.exists():
                print(f"📂 Found existing audio: {line_audio_path.name}")
            else:
                self.generate_audio(
                    text=line.strip(),
                    output_path=str(line_audio_path),
                    voice=voice,
                )
            line_audio_files.append(str(line_audio_path))
        
        # Combine line audios into section audio
        section_audio_path = audio_dir / f"{section_id}_audio.mp3"
        
        if len(line_audio_files) == 1:
            # Only one line, just copy/use it
            import shutil
            shutil.copy(line_audio_files[0], section_audio_path)
        else:
            # Combine multiple line audios with optional pauses
            combined = AudioSegment.empty()
            pause_duration = 500  # 500ms pause between lines
            
            for i, audio_file in enumerate(line_audio_files):
                segment = AudioSegment.from_mp3(audio_file)
                combined += segment
                
                # Add pause between lines (except after the last one)
                if add_pauses and i < len(line_audio_files) - 1:
                    combined += AudioSegment.silent(duration=pause_duration)
            
            combined.export(str(section_audio_path), format="mp3")
        
        print(f"🎵 Section audio created: {section_audio_path}")
        return str(section_audio_path)


def get_audio_duration(audio_path: str) -> float:
    """Get duration of audio file in seconds"""
    try:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) / 1000.0  # Convert ms to seconds
    except Exception as e:
        print(f"⚠️ Failed to get audio duration: {e}")
        return 0.0


def get_video_duration(video_path: str) -> float:
    """Get duration of video file in seconds using ffprobe"""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ],
            capture_output=True,
            text=True,
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"⚠️ Failed to get video duration: {e}")
        return 0.0


def merge_video_audio(
    video_path: str,
    audio_path: str,
    output_path: str,
    audio_volume: float = 1.0,
    loop_audio: bool = False,
) -> str:
    """
    Merge video and audio using ffmpeg
    
    Args:
        video_path: Path to input video
        audio_path: Path to input audio
        output_path: Path for output video with audio
        audio_volume: Audio volume multiplier (1.0 = original)
        loop_audio: Whether to loop audio if shorter than video
        
    Returns:
        Path to output video file
    """
    video_duration = get_video_duration(video_path)
    audio_duration = get_audio_duration(audio_path)
    
    print(f"📹 Video duration: {video_duration:.2f}s, Audio duration: {audio_duration:.2f}s")
    
    # Build ffmpeg command
    cmd = ["ffmpeg", "-y", "-i", video_path, "-i", audio_path]
    
    # If audio is longer than video, trim audio to match video
    # If video is longer than audio, audio will naturally end and rest will be silent
    filter_complex = []
    
    if audio_volume != 1.0:
        filter_complex.append(f"[1:a]volume={audio_volume}[aout]")
        audio_map = "[aout]"
    else:
        audio_map = "1:a"
    
    if loop_audio and audio_duration < video_duration:
        # Loop audio to match video duration
        loops_needed = int(video_duration / audio_duration) + 1
        filter_complex.insert(0, f"[1:a]aloop=loop={loops_needed}:size={int(audio_duration * 48000)}[alooped]")
        if audio_volume != 1.0:
            filter_complex = [f"[1:a]aloop=loop={loops_needed}:size={int(audio_duration * 48000)}[alooped]", 
                           f"[alooped]volume={audio_volume}[aout]"]
            audio_map = "[aout]"
        else:
            audio_map = "[alooped]"
    
    if filter_complex:
        cmd.extend(["-filter_complex", ";".join(filter_complex)])
        cmd.extend(["-map", "0:v", "-map", audio_map])
    else:
        cmd.extend(["-map", "0:v", "-map", "1:a"])
    
    # Output settings
    cmd.extend([
        "-c:v", "copy",  # Copy video stream without re-encoding
        "-c:a", "aac",   # Encode audio as AAC
        "-b:a", "192k",  # Audio bitrate
        "-shortest",     # End when shortest stream ends
        output_path
    ])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video with audio created: {output_path}")
            return output_path
        else:
            print(f"❌ FFmpeg merge failed: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Video-audio merge failed: {e}")
        return None


def merge_videos_with_audios(
    section_videos: dict,
    section_audios: dict,
    output_dir: Path,
) -> dict:
    """
    Merge each section's video with its corresponding audio
    
    Args:
        section_videos: Dict mapping section_id to video path
        section_audios: Dict mapping section_id to audio path
        output_dir: Output directory for merged videos
        
    Returns:
        Dict mapping section_id to merged video path
    """
    merged_videos = {}
    
    for section_id, video_path in section_videos.items():
        audio_path = section_audios.get(section_id)
        
        if not audio_path or not Path(audio_path).exists():
            print(f"⚠️ No audio for {section_id}, using video without audio")
            merged_videos[section_id] = video_path
            continue
        
        # Create output path for merged video
        video_name = Path(video_path).stem
        merged_path = output_dir / f"{video_name}_with_audio.mp4"
        
        result = merge_video_audio(video_path, audio_path, str(merged_path))
        
        if result:
            merged_videos[section_id] = result
        else:
            # Fallback to original video
            merged_videos[section_id] = video_path
    
    return merged_videos


def generate_all_section_audios(
    storyboard: dict,
    output_dir: Path,
    tts_generator: TTSGenerator,
) -> dict:
    """
    Generate audio for all sections in the storyboard
    
    Args:
        storyboard: Storyboard dict with sections containing lecture_lines
        output_dir: Directory to save audio files
        tts_generator: TTSGenerator instance
        
    Returns:
        Dict mapping section_id to audio file path
    """
    section_audios = {}
    
    sections = storyboard.get("sections", [])
    
    for section in sections:
        section_id = section.get("id")
        lecture_lines = section.get("lecture_lines", [])
        
        if not lecture_lines:
            print(f"⚠️ {section_id} has no lecture_lines, skipping audio")
            continue
        
        try:
            audio_path = tts_generator.generate_section_audio(
                section_id=section_id,
                lecture_lines=lecture_lines,
                output_dir=output_dir,
            )
            
            if audio_path:
                section_audios[section_id] = audio_path
                
        except Exception as e:
            print(f"❌ Failed to generate audio for {section_id}: {e}")
    
    return section_audios


# Convenience function for testing
def test_tts():
    """Test TTS functionality"""
    try:
        tts = TTSGenerator()
        test_output = Path(__file__).parent / "test_tts_output.mp3"
        tts.generate_audio(
            text="Hello! This is a test of the OpenAI text-to-speech system.",
            output_path=str(test_output),
        )
        print(f"✅ TTS test passed! Output: {test_output}")
        return True
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False


if __name__ == "__main__":
    test_tts()
