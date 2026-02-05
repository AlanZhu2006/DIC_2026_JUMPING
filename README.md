# VisualKiwi: Interactive Visual Learning Platform Based on Code2Video

<p align="right">
  <a href="./README.zh-CN.md">简体中文</a> | <b>English</b>
</p>

<p align="center">
  <b>VisualKiwi: Transforming LLM-Assisted Learning into Interactive Visual Understanding</b>
<br>
  Intelligent Educational Video Generation System Based on Code2Video Framework
</p>

---

## 🌟 Project Overview

**VisualKiwi** is a **Kiwi plugin** that transforms traditional text-based LLM learning into **interactive visual understanding** by combining multi-agent orchestration, RAG, and web search.

Most students currently use LLMs primarily for text-based learning (summaries, explanations, Q&A). However, many concepts (e.g., geometry, physics, algorithms, statistics, chemistry mechanisms) are fundamentally **visual and dynamic**. Text alone often fails to convey intuition, temporal processes, and structural relationships.

**VisualKiwi** can automatically generate the following content:

- 🎬 **Demonstration Videos** (step-by-step animations, narrated walkthroughs, simulated processes)
  - Generate high-quality educational videos based on the **Code2Video** framework
  - Use **Remotion** for video editing and composition

- 📊 **Interactive Graphs and Visualizations** (manipulable plots, sliders, parameter sweeps, "what-if" exploration)
  - Use AG-UI or custom protocols
  - Import open-source SDKs to render chemical formulas, etc.

- 📚 **Rich-Content Slides** (structured explanations with figures, animations, and embedded interactivity)
  - Use Slides MCP
  - Support Mermaid diagrams and mind maps

---

## ✅ Deployment Status

### Completed Deployment Steps

- [x] **Phase 1: Environment Setup**
  - ✅ Python 3.11.9 installed and verified
  - ✅ Virtual environment created (`venv/`)
  - ✅ pip upgraded to 26.0

- [x] **Phase 2: System Dependencies**
  - ✅ FFmpeg 8.0.1 installed and working
  - ✅ MiKTeX 24.1 installed and working
  - ✅ Graphics libraries ready

- [x] **Phase 3: Python Dependencies**
  - ✅ All 80+ packages installed successfully
  - ✅ Manim 0.19.0 installed
  - ✅ OpenAI, NumPy, SciPy, OpenCV, MoviePy all verified

- [x] **Phase 4: Manim Verification**
  - ✅ Manim Community v0.19.0 verified
  - ✅ Test scene rendered successfully
  - ✅ Complex example with DIC JUMPING end credits created

- [x] **Phase 5: API Configuration**
  - ✅ API configuration files created
  - ✅ ChatAnywhere free API service configured
  - ✅ GPT API (gpt-3.5-turbo) tested and working
  - ✅ API connection test scripts created
  - ✅ Configuration guides and documentation added

- [x] **Phase 7: Functional Testing**
  - ✅ Single knowledge point test completed
  - ✅ Video generation pipeline verified
  - ✅ Multiple test cases completed with different API models
  - ✅ Success rate: 100% (knowledge point processing), 100% (video rendering with GPT-5.2)
  - ✅ Generated files: outline, storyboard, Manim code, and final video

### Test Results Summary

**Latest Test** (2026-02-04) - GPT-5.2:
- **Knowledge Point**: "Circle area formula"
- **API**: gpt-5 (Official OpenAI, gpt-5.2)
- **Duration**: 4.80 minutes
- **Output**: Successfully generated `Circle_area_formula.mp4`
- **Sections**: Generated 7 sections, 7/7 successfully rendered (100%)
- **Token Usage**: 29,222 tokens
- **Quality**: Enhanced content with more detailed sections

**Previous Tests**:
- **GPT-4o Test**: 5 sections, 100% success, 1.99 minutes, 13,198 tokens
- **ChatAnywhere Test**: 6 sections, 83.3% success, 3.46 minutes

---

## 🚀 Quick Start

### 1. Environment Setup

#### Activate Virtual Environment

```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# After activation, verify
python --version  # Should show Python 3.11.9
pip --version     # Should show pip 26.0
```

#### System Requirements

- **Python**: 3.11+ (✅ 3.11.9 installed)
- **FFmpeg**: For video processing (✅ 8.0.1 installed)
- **LaTeX**: For mathematical formulas (✅ MiKTeX 24.1 installed)
- **Memory**: At least 8GB RAM recommended
- **Storage**: At least 10GB free space

### 2. Install Dependencies

```bash
# Navigate to src directory
cd src/

# Install all dependencies (already done if following deployment steps)
pip install -r requirements.txt
```

**Key Dependencies Installed**:
- `manim==0.19.0` - Animation engine
- `openai==1.90.0` - LLM API
- `numpy==2.2.6` - Numerical computing
- `scipy==1.15.3` - Scientific computing
- `opencv-python==4.12.0.88` - Image/video processing
- `moviepy==2.2.1` - Video manipulation

### 3. Configure API Keys

**Important**: The `src/api_config.json` file is excluded from Git for security. You need to create it from the template.

#### Step 1: Create API Configuration File

```powershell
# Copy the template file
cd src
Copy-Item api_config.json.template api_config.json
```

#### Step 2: Get API Keys

#### Option 1: Official OpenAI API (Recommended for Production)

**Official OpenAI API** provides the best quality and reliability. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

**Steps**:
1. Visit https://platform.openai.com/api-keys
2. Sign up or log in to your OpenAI account
3. Create a new API key
4. Edit `src/api_config.json` and replace `YOUR_OPENAI_API_KEY` with your actual API key:

```json
{
    "gpt41": {
        "base_url": "https://api.openai.com/v1",
        "api_version": "",
        "api_key": "sk-YOUR_OPENAI_API_KEY",
        "model": "gpt-4o-mini"
    },
    "gpt4o": {
        "base_url": "https://api.openai.com/v1",
        "api_version": "",
        "api_key": "sk-YOUR_OPENAI_API_KEY",
        "model": "gpt-4o"
    }
}
```

**Note**: Official OpenAI API requires payment, but provides the best model quality and reliability.

#### Option 2: ChatAnywhere Free API (Alternative for Testing)

[ChatAnywhere](https://github.com/chatanywhere/GPT_API_free) provides free API forwarding service supporting multiple models. One API key works for all models!

**Steps**:
1. Visit https://github.com/chatanywhere/GPT_API_free
2. Use GitHub account to login and get free API key
3. Edit `src/api_config.json` and use `gpt41-chatanywhere` or `gpt4o-chatanywhere` configuration, replace `YOUR_CHATANYWHERE_API_KEY` with your actual API key:

```json
{
    "gpt41": {
        "base_url": "https://api.chatanywhere.tech/v1",
        "api_version": "2024-03-01-preview",
        "api_key": "sk-YOUR_CHATANYWHERE_API_KEY",
        "model": "gpt-3.5-turbo"
    },
    "claude": {
        "base_url": "https://api.chatanywhere.tech/v1",
        "api_key": "sk-YOUR_CHATANYWHERE_API_KEY",
        "model": "claude-3-opus"
    },
    "gemini": {
        "base_url": "https://api.chatanywhere.tech/v1",
        "api_version": "2024-03-01-preview",
        "api_key": "sk-YOUR_CHATANYWHERE_API_KEY",
        "model": "gemini-pro"
    },
    "iconfinder": {
        "api_key": "YOUR_ICONFINDER_KEY"
    }
}
```

**Note**: ChatAnywhere free version mainly supports GPT models. Claude models may not be available.

#### Option 2: Official APIs (For Production)

Edit `src/api_config.json`:

```json
{
    "claude": {
        "base_url": "https://api.anthropic.com/v1/messages",
        "api_key": "YOUR_CLAUDE_API_KEY"
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta",
        "api_version": "2024-03-01-preview",
        "api_key": "YOUR_GEMINI_API_KEY",
        "model": "gemini-2.5-pro-preview-05-06"
    },
    "iconfinder": {
        "api_key": "YOUR_ICONFINDER_KEY"
    }
}
```

**API Notes**:

- **LLM API** (Claude/GPT): Used for Planner and Coder agents
  - ChatAnywhere: `gpt-3.5-turbo` (free, tested ✅)
  - Official: **Claude-4-Opus** for best Manim code quality

- **VLM API** (Gemini): Used for Planner Critic agent
  - For layout and aesthetics optimization
  - Recommended: **gemini-2.5-pro-preview-05-06**

- **Visual Assets API** (IconFinder): For enriching videos with icon resources (optional)

**Test API Connection**:
```powershell
cd src
python test_api_connection.py
```

**Security Note**: 
- ✅ `src/api_config.json` is excluded from Git (in `.gitignore`)
- ✅ Template file `src/api_config.json.template` is provided for reference
- ⚠️ Never commit your real API keys to the repository

### 4. Generate Educational Videos

#### Method 1: Single Knowledge Point

**Windows PowerShell**:
```powershell
# Set Python path and run
$env:PYTHONPATH = "$PWD"
cd src
python agent.py --API gpt-41 --folder_prefix TEST-single --no_feedback --no_assets --knowledge_point "Circle area formula"
```

**Linux/macOS**:
```bash
cd src/
sh run_agent_single.sh --knowledge_point "AVL Tree Rotation Operations"
```

**Parameter Notes**:

- `--API`: Specify which LLM to use (e.g., `gpt-41` for ChatAnywhere, `claude` for official API)
- `--folder_prefix`: Output folder prefix (e.g., `TEST-single`)
- `--knowledge_point`: Target concept, e.g., `"Circle area formula"` or `"AVL Tree Rotation Operations"`
- `--no_feedback`: Disable Critic feedback (recommended if Gemini API not configured)
- `--no_assets`: Disable IconFinder assets (optional)

**Output Location**: `src/CASES/{folder_prefix}_{API_name}/{knowledge_point}/`

#### Method 2: Batch Generation

```bash
cd src/
sh run_agent.sh
```

**Parameter Notes** (configure in `run_agent.sh`):

- `API`: Specify which LLM to use
- `FOLDER_PREFIX`: Output folder prefix (e.g., `VisualKiwi-batch`)
- `MAX_CONCEPTS`: Number of concepts to include (`-1` means all)
- `PARALLEL_GROUP_NUM`: Number of groups to run in parallel

---

## 🎬 Manim Examples

### Example 1: Complex Example with DIC JUMPING End Credits

We've created a comprehensive Manim example (`complex_example.py`) that demonstrates:

1. **Gradient Text** - Colorful title animations
2. **Mathematical Formulas** - LaTeX rendering (Euler's formula)
3. **Shape Transformations** - Circle to square morphing
4. **Group Animations** - Multiple shapes rotating together
5. **Number Line** - Interactive number line with moving dot
6. **Function Graphs** - Sine wave visualization
7. **DIC JUMPING End Credits** - Custom end credits with jumping letters

#### How to Run

```powershell
# 1. Activate virtual environment
.\venv\Scripts\Activate.ps1

# 2. Quick preview (low quality, fast)
manim -ql complex_example.py ComplexExample

# 3. High quality (1080p, 60fps)
manim -qh complex_example.py ComplexExample

# 4. 4K quality (2160p, 60fps)
manim -qk complex_example.py ComplexExample
```

#### Output Location

```
media/videos/complex_example/[quality]/ComplexExample.mp4
```

#### Video Preview

<video width="800" controls>
  <source src="https://raw.githubusercontent.com/AlanZhu2006/DIC_2026_JUMPING/main/assets/videos/examples/ComplexExample.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

*Alternative: [Download video](assets/videos/examples/ComplexExample.mp4)*

*Note: For higher quality versions, see `media/videos/complex_example/1080p60/` or `2160p60/` directories.*

#### DIC JUMPING End Credits Features

The end credits include:

- **Letter-by-letter appearance** - Each letter drops from above with animation
- **Jumping animation** - All letters jump together 3 times
- **Subtitle** - "VisualKiwi Project" appears below
- **Sparkle effect** - 12 yellow dots surround the text
- **Final fade out** - Smooth ending transition

---

### Example 2: Circle Area Formula (Code2Video Generated)

This is a real example generated by the Code2Video framework using GPT-5.2 (Official OpenAI API).

**Knowledge Point**: "Circle area formula"

**Generation Command**:
```powershell
$env:PYTHONPATH = "$PWD"
& "venv\Scripts\python.exe" "src\agent.py" --API gpt-5 --folder_prefix TEST-gpt52 --no_feedback --no_assets --knowledge_point "Circle area formula"
```

**Generated Content**:
- ✅ **Teaching Outline** - Structured learning plan (`outline.json`)
- ✅ **Storyboard** - 7 sections with detailed animations (`storyboard.json`)
- ✅ **Manim Code** - 7 Python files (`section_1.py` ~ `section_7.py`)
- ✅ **Final Video** - Merged educational video (`Circle_area_formula.mp4`)

#### Output Structure

```
src/CASES/TEST-single_Chatgpt41/0-Circle_area_formula/
├── Circle_area_formula.mp4          # Final merged video (865 KB)
├── outline.json                      # Teaching outline
├── storyboard.json                   # Storyboard with 6 sections
├── section_1.py                      # Section 1: Introduction to Circles
├── section_2.py                      # Section 2: Radius and Diameter
├── section_3.py                      # Section 3: Area Formula Derivation
├── section_4.py                      # Section 4: Example Calculations
├── section_5.py                      # Section 5: Applications
├── section_6.py                      # Section 6: Summary
└── media/videos/
    ├── section_1/480p15/Section1Scene.mp4
    ├── section_2/480p15/Section2Scene.mp4
    ├── section_3/480p15/Section3Scene.mp4
    ├── section_4/480p15/Section4Scene.mp4
    └── section_6/480p15/Section6Scene.mp4
```

#### Test Results

- **Generation Time**: 3.46 minutes
- **Success Rate**: 100% (knowledge point processing), 83.3% (video rendering)
- **Sections Generated**: 6 sections
- **Sections Rendered**: 5/6 successfully (section_5 had code error, skipped)
- **Final Output**: Complete educational video ready for use

#### Video Preview (GPT-5.2 Generated)

<video width="800" controls>
  <source src="https://raw.githubusercontent.com/AlanZhu2006/DIC_2026_JUMPING/main/assets/videos/examples/Circle_area_formula_gpt52.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

*Alternative: [Download video](assets/videos/examples/Circle_area_formula_gpt52.mp4)*

**Note**: This video was generated using GPT-5.2, featuring 7 detailed sections with enhanced educational content.

*This video was automatically generated by Code2Video framework using GPT-3.5-turbo API.*

#### Video Features

The generated video includes:
- **Structured Content** - Organized into logical sections
- **Mathematical Formulas** - LaTeX-rendered formulas
- **Visual Animations** - Step-by-step demonstrations
- **Grid Layout System** - Professional layout with title and content areas
- **Smooth Transitions** - Well-timed animations between concepts

---

### Example 3: Simple Test Example

```bash
# Run simple test scene
manim -ql test_manim.py TestScene
```

---

## 📂 Project Structure

```
Code2Video/
│── src/
│   ├── agent.py              # Core agent implementation
│   ├── run_agent.sh          # Batch generation script
│   ├── run_agent_single.sh   # Single knowledge point script
│   ├── api_config.json       # API configuration
│   ├── requirements.txt      # Python dependencies
│   └── ...
│
├── assets/
│   ├── icons/                # Visual asset cache from IconFinder
│   └── reference/            # Reference images
│
├── json_files/               # JSON-based topic lists & metadata
├── prompts/                  # Prompt templates for LLM calls
│   ├── stage1.py            # Planner stage
│   ├── stage2.py            # Coder stage
│   ├── stage3.py            # Critic stage
│   └── ...
│
├── venv/                     # Python virtual environment
│
├── media/                    # Manim output directory
│   └── videos/
│       ├── complex_example/  # Complex example videos
│       └── test_manim/       # Test scene videos
│
├── complex_example.py        # Complex Manim example with DIC JUMPING
├── test_manim.py            # Simple test scene
│
└── CASES/                    # Generated cases, organized by FOLDER_PREFIX
    └── VisualKiwi-single/   # Example single-topic generation results
```

---

## 🏗️ Architecture Design

### Core Architecture

```
User Prompt (Kiwi/LLM Agent)
    ↓
MCP Server (VisualKiwi)
    ↓
Multi-Agent Orchestration System
    ├── Planner Agent (Storyboard Planning)
    ├── Coder Agent (Code Generation - Code2Video)
    ├── Critic Agent (Layout Optimization)
    └── Visual Assets Agent (Resource Management)
    ↓
Visual Component Generation
    ├── Code2Video (Manim Videos)
    ├── Remotion (Video Editing)
    ├── Interactive Canvas (React/Web)
    └── Rich-Content Slides
    ↓
Rendering & Display
    └── iframe/Web Components Embedded in Chat Interface
```

### Modular Design

VisualKiwi adopts a **modular architecture** that can be easily integrated into any LLM platform supporting the MCP protocol:

- **MCP Server**: Acts as the core interface, receiving user prompts and returning visual components

- **Code2Video Integration**: Specifically handles scenarios requiring animated demonstrations (algorithms, mathematics, physics, etc.)

- **Extensibility**: Different content types (videos, slides, interactive graphs) are handled by different agents

---

## 💡 Use Cases

### Case 1: Interactive AVL Tree Learning

**Student Prompt**:
> "I keep mixing up AVL rotations (LL/RR/LR/RL). Can you teach me with a video, but also let me manipulate nodes myself to see how balance factors change?"

**VisualKiwi Output**:

1. **Generated Demonstration Video** (step-by-step, pausable)
   - Builds an AVL tree from an insertion sequence (e.g., 10 → 20 → 30 → 25 → 28)
   - At each step, overlays: node height, balance factor, and the first unbalanced ancestor
   - Shows the exact rotation type triggered (LL/RR/LR/RL) with before/after snapshots
   - Narrates the "why": which subtree got heavier and why that implies a specific rotation

2. **Interactive Frontend** (hands-on AVL editor)
   - Canvas: draggable tree nodes and edges (students can swap/reconnect nodes)
   - Side panel: real-time height + balance factor per node; highlights rule violations
   - Controls: Insert, Delete, Step, Auto-Rotate, Hint, Reset, Generate New Sequence
   - Validation: checks BST ordering and AVL balance constraints instantly

**Key Interactions**:
- Students can intentionally drag the tree into an unbalanced state; the UI highlights the culprit node and suggests candidate rotations
- Students choose a rotation manually; the system verifies correctness and explains mistakes
- "What-if" mode: change the insertion order or delete a node and watch the rotation strategy change

### Case 2: Interactive Chemistry Titration Lab

**Student Prompt**:
> "I don't understand why titration curves look different for strong vs weak acids. Can I interactively explore it and see the equivalence point?"

**VisualKiwi Output**:

- **Lab Control Panel**:
  - Choose a system: strong acid–strong base / weak acid–strong base / weak acid–weak base
  - Parameters: initial concentration, volume, Ka/Kb (optional temperature)
  - Operation: a slider controlling added titrant volume (like turning a burette)

- **Real-Time Visuals**:
  - Dynamic pH vs volume curve
  - Species composition view (HA/A⁻, H⁺/OH⁻ proportions)
  - Automatic markers for buffer region and equivalence point
  - Explanation triggers: crossing key regions (buffer → equivalence → excess base) pops concise explanations of the chemistry behind the curve shape

**Key Interactions**:
- Adjust Ka and immediately see buffer region width and equivalence-point pH shift
- "Indicator mode": choose an indicator; the UI shows whether its color-change range matches the equivalence point

---

## 🔧 Integration with VisualKiwi MCP Server

### MCP Server Interface Design

VisualKiwi acts as an MCP server, receiving user prompts and returning visual components:

```python
# Pseudocode example
def visualkiwi_mcp_tool(user_prompt: str) -> Dict:
    """
    Generate visual components based on user prompt
    
    Returns:
    {
        "type": "video" | "interactive" | "slides",
        "content": "...",
        "metadata": {...}
    }
    """
    # 1. Analyze user intent
    intent = analyze_intent(user_prompt)
    
    # 2. Select appropriate generator
    if intent.needs_video:
        # Use Code2Video
        video = code2video.generate(intent.knowledge_point)
        return {
            "type": "video",
            "content": video.embed_url,
            "metadata": {
                "duration": video.duration,
                "manim_code": video.code,
                "interactive": False
            }
        }
    elif intent.needs_interactive:
        # Use interactive Canvas
        canvas = generate_interactive_canvas(intent)
        return {
            "type": "interactive",
            "content": canvas.component,
            "metadata": {...}
        }
    # ...
```

### Frontend Rendering

In the chat interface, render different components based on the returned type:

```html
<!-- Video Component -->
<iframe 
    src="generated_video.html" 
    width="100%" 
    height="600px"
    allowfullscreen>
</iframe>

<!-- Interactive Canvas -->
<div id="interactive-canvas">
    <!-- React/Web Components -->
</div>

<!-- Rich-Content Slides -->
<div class="slides-container">
    <!-- Reveal.js or other slide frameworks -->
</div>
```

---

## 📊 Tech Stack

### Video Generation
- **Code2Video**: Educational video generation framework based on Manim
- **Remotion**: React video editing and composition
- **Manim Community v0.19.0**: Mathematical animation engine (✅ Installed and verified)

### Interactive Visualization
- **React**: Frontend framework
- **AG-UI / Custom Protocol**: UI component system
- **Mermaid**: Diagrams and flowcharts
- **Reveal.js**: Slide framework

### Multi-Agent System
- **LangGraph**: Agent orchestration
- **Instructor**: Structured output
- **RAG**: Retrieval-Augmented Generation

### Graphics and Rendering
- **React D3 Tree**: Tree visualization
- **Excalidraw**: Drawing and feedback
- **XYFlow**: Flowcharts and node graphs

---

## 🎯 Development Roadmap

### Phase 1: Code2Video Integration (✅ Completed)
- [x] Integrate Code2Video core functionality
- [x] Configure APIs and dependencies
- [x] Environment setup (Python, FFmpeg, LaTeX)
- [x] Manim verification and examples
- [ ] Create MCP server interface
- [ ] Implement video generation API

### Phase 2: Interactive Components
- [ ] Develop interactive Canvas components
- [ ] Implement AVL tree editor
- [ ] Implement chemistry lab simulator
- [ ] Integrate React frontend

### Phase 3: Multi-Agent Orchestration
- [ ] Implement Planner Agent
- [ ] Implement Coder Agent (based on Code2Video)
- [ ] Implement Critic Agent
- [ ] Implement resource management Agent

### Phase 4: MCP Server
- [ ] Implement MCP protocol interface
- [ ] Integrate with Kiwi platform
- [ ] Testing and optimization

---

## 🛠️ Troubleshooting

### Common Issues

1. **Manim rendering fails**
   - Check FFmpeg installation: `ffmpeg -version`
   - Verify LaTeX: `latex --version`
   - Check OpenGL drivers

2. **API calls fail**
   - Verify API keys in `src/api_config.json`
   - Check network connection
   - Review API quota limits

3. **Memory issues**
   - Reduce parallel processing: adjust `PARALLEL_GROUP_NUM`
   - Increase system memory
   - Optimize video resolution

4. **Dependency installation fails**
   - Use Chinese mirror sources (Tsinghua, Aliyun)
   - Upgrade pip and setuptools
   - Check Python version compatibility (3.11+)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📌 Related Resources

### Video Generation Frameworks
- [Code2Video](https://showlab.github.io/Code2Video/) - Core framework this project is based on
- [Remotion](https://www.remotion.dev/) - React video editing
- [Generate Explanation Videos](https://arxiv.org/html/2502.19400v1) - Related research

### UI Protocols
- [JSON Render](https://github.com/vercel-labs/json-render)
- [Tambo](https://github.com/tambo-ai/tambo)

### Agent Frameworks
- [Instructor](https://github.com/567-labs/instructor)
- [LangGraph](https://github.com/langchain-ai/langgraph)

### Graphs and Visualization
- [XYFlow](https://github.com/xyflow/xyflow)
- [Excalidraw](https://github.com/excalidraw/excalidraw)
- [React D3 Tree](https://github.com/bkrem/react-d3-tree)
- [Mermaid](https://github.com/mermaid-js/mermaid)
- [Reveal.js](https://github.com/hakimel/reveal.js)

---

## 🙏 Acknowledgements

- **Code2Video Team**: Provided an excellent code-driven video generation framework
- **Manim Community**: Powerful mathematical animation engine
- **3Blue1Brown**: Inspired the design philosophy of educational videos
- **Show Lab @ NUS**: Original development team of Code2Video

---

## 📄 License

This project is based on the Code2Video project. Please refer to the original project's LICENSE file.

---

## 📧 Contact

For questions or suggestions, please contact us via:

- Submit an Issue
- Open a Pull Request

---

---

<p align="center">
  <b>Make learning visual, interactive, and fun!</b>
</p>
