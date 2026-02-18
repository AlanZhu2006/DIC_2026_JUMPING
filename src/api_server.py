"""
Code2Video API Server
FastAPI backend for video generation with SSE progress streaming
"""

import asyncio
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import threading
import queue

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
os.environ["PYTHONPATH"] = str(Path(__file__).parent.parent)

app = FastAPI(
    title="Code2Video API",
    description="Generate educational videos from knowledge points using AI",
    version="1.0.0"
)

# CORS - Allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store for tracking generation tasks
tasks = {}

class VideoRequest(BaseModel):
    knowledge_point: str
    api: str = "gpt-41"
    use_tts: bool = True
    tts_voice: str = "nova"

class TaskStatus(BaseModel):
    task_id: str
    status: str  # pending, running, completed, failed
    progress: int  # 0-100
    message: str
    video_url: Optional[str] = None
    error: Optional[str] = None

# Progress queue for SSE
progress_queues = {}

def run_video_generation(task_id: str, knowledge_point: str, api: str, use_tts: bool, tts_voice: str):
    """Run video generation in background thread"""
    from agent import TeachingVideoAgent, RunConfig
    from gpt_request import request_gpt41_token, request_gpt4o_token, request_gpt5_token
    
    q = progress_queues.get(task_id)
    
    def send_progress(progress: int, message: str):
        tasks[task_id]["progress"] = progress if progress >= 0 else tasks[task_id]["progress"]
        tasks[task_id]["message"] = message
        if q:
            q.put({"progress": progress, "message": message})
    
    try:
        tasks[task_id]["status"] = "running"
        send_progress(5, "🚀 Starting video generation...")
        
        # Select API function based on request (use _token versions that return (response, usage) tuple)
        api_map = {
            "gpt-41": request_gpt41_token,
            "gpt-4o": request_gpt4o_token,
            "gpt-5": request_gpt5_token,
        }
        api_func = api_map.get(api, request_gpt41_token)
        
        # Create output folder path
        folder_path = Path(__file__).parent / "CASES" / f"API-{task_id[:8]}"
        
        # Initialize config
        config = RunConfig(
            api=api_func,
            use_feedback=False,
            use_assets=False,
            use_tts=use_tts,
            tts_voice=tts_voice,
            max_fix_bug_tries=3,
        )
        
        send_progress(10, "📝 Generating outline...")
        
        generator = TeachingVideoAgent(
            idx=0,
            knowledge_point=knowledge_point,
            folder=folder_path,
            cfg=config,
        )
        
        # Override print to capture progress
        original_print = print
        def custom_print(*args, **kwargs):
            msg = " ".join(str(a) for a in args)
            original_print(*args, **kwargs)
            
            # Parse progress from messages
            if "Outline generated" in msg:
                send_progress(20, "📝 Outline generated")
            elif "Storyboard" in msg:
                send_progress(30, "🎬 Storyboard generated")
            elif "section_" in msg and "finished" in msg:
                # Extract section number
                current = tasks[task_id].get("sections_done", 0) + 1
                total = tasks[task_id].get("total_sections", 7)
                tasks[task_id]["sections_done"] = current
                progress = 30 + int(40 * current / total)
                send_progress(progress, f"🎥 Rendering video {current}/{total}")
            elif "audio generated" in msg.lower():
                send_progress(75, "🎙️ Generating voice narration...")
            elif "Merging" in msg:
                send_progress(85, "🔗 Merging video clips...")
            elif "success" in msg.lower():
                send_progress(95, "✅ Video generation successful!")
        
        import builtins
        builtins.print = custom_print
        
        try:
            # Run generation
            result = generator.GENERATE_VIDEO()
            
            if result is None:
                raise Exception("GENERATE_VIDEO returned None - check server logs for details")
            
            # Find output video
            video_path = generator.output_dir / f"{knowledge_point.replace(' ', '_')}.mp4"
            if not video_path.exists():
                # Try to find any mp4 in output dir
                mp4_files = list(generator.output_dir.glob("*.mp4"))
                if mp4_files:
                    video_path = mp4_files[0]
            
            if video_path.exists():
                tasks[task_id]["status"] = "completed"
                tasks[task_id]["video_path"] = str(video_path)
                tasks[task_id]["video_url"] = f"/api/video/{task_id}"
                send_progress(100, "🎉 Video generation complete!")
            else:
                raise Exception("Video file not found after generation")
                
        finally:
            builtins.print = original_print
            
    except Exception as e:
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"❌ Task {task_id} failed: {error_detail}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        send_progress(-1, f"❌ Generation failed: {str(e)}")
    
    # Signal end
    if q:
        q.put(None)

@app.get("/")
async def root():
    return {
        "name": "Code2Video API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.post("/api/generate")
async def generate_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Start video generation task"""
    task_id = str(uuid.uuid4())
    
    tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "progress": 0,
        "message": "Task created",
        "knowledge_point": request.knowledge_point,
        "created_at": datetime.now().isoformat(),
        "video_url": None,
        "error": None,
        "sections_done": 0,
        "total_sections": 7,
    }
    
    # Create progress queue
    progress_queues[task_id] = queue.Queue()
    
    # Start generation in background thread
    thread = threading.Thread(
        target=run_video_generation,
        args=(task_id, request.knowledge_point, request.api, request.use_tts, request.tts_voice)
    )
    thread.start()
    
    return {"task_id": task_id, "message": "Video generation started"}

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """Get task status"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    return TaskStatus(
        task_id=task_id,
        status=task["status"],
        progress=task.get("progress", 0),
        message=task.get("message", ""),
        video_url=task.get("video_url"),
        error=task.get("error")
    )

@app.get("/api/progress/{task_id}")
async def stream_progress(task_id: str):
    """SSE endpoint for real-time progress updates"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    async def event_generator():
        q = progress_queues.get(task_id)
        if not q:
            yield f"data: {json.dumps({'error': 'No progress queue'})}\n\n"
            return
        
        while True:
            try:
                # Non-blocking get with timeout
                data = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: q.get(timeout=30)
                )
                
                if data is None:
                    # End of stream
                    task = tasks[task_id]
                    final_data = {
                        "progress": 100 if task["status"] == "completed" else -1,
                        "message": task.get("message", ""),
                        "status": task["status"],
                        "video_url": task.get("video_url"),
                        "error": task.get("error"),
                        "done": True
                    }
                    yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"
                    break
                
                # Update task progress
                tasks[task_id]["progress"] = data.get("progress", 0)
                tasks[task_id]["message"] = data.get("message", "")
                
                yield f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
                
            except queue.Empty:
                # Send heartbeat
                yield f"data: {json.dumps({'heartbeat': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
                break
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@app.get("/api/video/{task_id}")
async def get_video(task_id: str):
    """Download generated video"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks[task_id]
    if task["status"] != "completed":
        raise HTTPException(status_code=400, detail="Video not ready")
    
    video_path = task.get("video_path")
    if not video_path or not Path(video_path).exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    
    return FileResponse(
        video_path,
        media_type="video/mp4",
        filename=f"{task['knowledge_point'].replace(' ', '_')}.mp4"
    )

@app.get("/api/tasks")
async def list_tasks():
    """List all tasks"""
    return [
        {
            "task_id": t["task_id"],
            "status": t["status"],
            "knowledge_point": t["knowledge_point"],
            "created_at": t["created_at"],
            "progress": t.get("progress", 0),
        }
        for t in tasks.values()
    ]

def clear_port(port: int):
    """Clear a port by killing processes using it (Windows only)"""
    import subprocess
    import platform
    
    if platform.system() != "Windows":
        return
    
    try:
        # Find processes using the port
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            shell=True
        )
        
        pids_to_kill = set()
        for line in result.stdout.split("\n"):
            if f":{port}" in line and ("LISTENING" in line or "ESTABLISHED" in line):
                parts = line.split()
                if parts:
                    try:
                        pid = int(parts[-1])
                        if pid > 0:
                            pids_to_kill.add(pid)
                    except ValueError:
                        pass
        
        for pid in pids_to_kill:
            try:
                subprocess.run(
                    ["taskkill", "/F", "/PID", str(pid)],
                    capture_output=True,
                    shell=True
                )
                print(f"  ✓ Terminated process PID: {pid}")
            except Exception:
                pass
        
        if pids_to_kill:
            import time
            time.sleep(2)
            print(f"  ✓ Port {port} cleared")
        else:
            print(f"  ✓ Port {port} is not in use")
            
    except Exception as e:
        print(f"  ⚠ Failed to clear port: {e}")

if __name__ == "__main__":
    import uvicorn
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-clear", action="store_true", help="Skip port clearing")
    args, _ = parser.parse_known_args()
    
    print("=" * 50)
    print("  🎬 Code2Video API Server")
    print("=" * 50)
    
    if not args.no_clear:
        print(f"\n🔧 Clearing port {args.port}...")
        clear_port(args.port)
    
    print(f"\n📍 Local:   http://localhost:{args.port}")
    print(f"📍 Network: http://<your-ip>:{args.port}")
    print(f"📖 Docs:    http://localhost:{args.port}/docs")
    print("=" * 50)
    uvicorn.run(app, host="0.0.0.0", port=args.port)
