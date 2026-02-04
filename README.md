# VisualKiwi: Interactive Visual Learning Platform Based on Code2Video
# VisualKiwi: 基于 Code2Video 的交互式视觉学习平台

<p align="right">
  <a href="./README.zh-CN.md">简体中文</a> | <b>English</b>
</p>

<p align="center">
  <b>VisualKiwi: Transforming LLM-Assisted Learning into Interactive Visual Understanding</b>
<br>
  <b>VisualKiwi: 将 LLM 辅助学习转化为交互式视觉理解</b>
<br>
  Intelligent Educational Video Generation System Based on Code2Video Framework
<br>
  基于 Code2Video 框架的智能教学视频生成系统
</p>

---

## 🌟 Project Overview | 项目概述

**VisualKiwi** is a **Kiwi plugin** that transforms traditional text-based LLM learning into **interactive visual understanding** by combining multi-agent orchestration, RAG, and web search.

**VisualKiwi** 是一个 **Kiwi 插件**，通过结合多智能体编排、RAG 和网络搜索，将传统的文本式 LLM 学习转化为**交互式视觉理解**。

Most students currently use LLMs primarily for text-based learning (summaries, explanations, Q&A). However, many concepts (e.g., geometry, physics, algorithms, statistics, chemistry mechanisms) are fundamentally **visual and dynamic**. Text alone often fails to convey intuition, temporal processes, and structural relationships.

当前大多数学生主要使用 LLM 进行基于文本的学习（摘要、解释、问答）。然而，许多概念（如几何、物理、算法、统计、化学机制）本质上是**视觉和动态的**。纯文本往往无法传达直觉、时间过程和结构关系。

**VisualKiwi** can automatically generate the following content:

**VisualKiwi** 可以自动生成以下内容：

- 🎬 **Demonstration Videos** (step-by-step animations, narrated walkthroughs, simulated processes)
  - Generate high-quality educational videos based on the **Code2Video** framework
  - Use **Remotion** for video editing and composition
- 🎬 **演示视频**（分步动画、带旁白的演练、模拟过程）
  - 基于 **Code2Video** 框架生成高质量教学视频
  - 使用 **Remotion** 进行视频编辑和合成

- 📊 **Interactive Graphs and Visualizations** (manipulable plots, sliders, parameter sweeps, "what-if" exploration)
  - Use AG-UI or custom protocols
  - Import open-source SDKs to render chemical formulas, etc.
- 📊 **交互式图表和可视化**（可操作的图表、滑块、参数扫描、"假设"探索）
  - 使用 AG-UI 或自定义协议
  - 导入开源 SDK 渲染化学公式等

- 📚 **Rich-Content Slides** (structured explanations with figures, animations, and embedded interactivity)
  - Use Slides MCP
  - Support Mermaid diagrams and mind maps
- 📚 **富内容幻灯片**（结构化解释，包含图表、动画和嵌入式交互性）
  - 使用 Slides MCP
  - 支持 Mermaid 图表和思维导图

---

## 🏗️ Architecture Design | 架构设计

### Core Architecture | 核心架构

```
User Prompt (Kiwi/LLM Agent) | 用户提示 (Kiwi/LLM Agent)
    ↓
MCP Server (VisualKiwi) | MCP 服务器 (VisualKiwi)
    ↓
Multi-Agent Orchestration System | 多智能体编排系统
    ├── Planner Agent (Storyboard Planning) | 故事板规划
    ├── Coder Agent (Code Generation - Code2Video) | 代码生成 - Code2Video
    ├── Critic Agent (Layout Optimization) | 布局优化
    └── Visual Assets Agent (Resource Management) | 资源管理
    ↓
Visual Component Generation | 视觉组件生成
    ├── Code2Video (Manim Videos) | Code2Video (Manim 视频)
    ├── Remotion (Video Editing) | Remotion (视频编辑)
    ├── Interactive Canvas (React/Web) | 交互式 Canvas (React/Web)
    └── Rich-Content Slides | 富内容 Slides
    ↓
Rendering & Display | 渲染与展示
    └── iframe/Web Components Embedded in Chat Interface | iframe/Web 组件嵌入对话界面
```

### Modular Design | 模块化设计

VisualKiwi adopts a **modular architecture** that can be easily integrated into any LLM platform supporting the MCP protocol:

VisualKiwi 采用**模块化架构**，可以轻松集成到任何支持 MCP 协议的 LLM 平台：

- **MCP Server**: Acts as the core interface, receiving user prompts and returning visual components
- **MCP 服务器**：作为核心接口，接收用户提示并返回视觉组件

- **Code2Video Integration**: Specifically handles scenarios requiring animated demonstrations (algorithms, mathematics, physics, etc.)
- **Code2Video 集成**：专门处理算法、数学、物理等需要动画演示的场景

- **Extensibility**: Different content types (videos, slides, interactive graphs) are handled by different agents
- **可扩展性**：不同内容类型（视频、幻灯片、交互式图表）由不同的智能体处理

---

## 🚀 Quick Start | 快速开始

### 1. Requirements | 环境要求

#### Basic Dependencies | 基础依赖

```bash
cd src/
pip install -r requirements.txt
```

#### Manim Installation | Manim 安装

Please refer to the [official installation guide for Manim Community v0.19.0](https://docs.manim.community/en/stable/installation.html) to properly set up the environment.

请参考 [Manim Community v0.19.0 官方安装指南](https://docs.manim.community/en/stable/installation.html) 正确设置环境。

### 2. Configure API Keys | 配置 API 密钥

Configure your API credentials in `src/api_config.json`:

在 `src/api_config.json` 中配置您的 API 凭证：

```json
{
    "claude": {
        "base_url": "...",
        "api_key": "YOUR_CLAUDE_API_KEY"
    },
    "gemini": {
        "base_url": "...",
        "api_version": "2024-03-01-preview",
        "api_key": "YOUR_GEMINI_API_KEY",
        "model": "gemini-2.5-pro-preview-05-06"
    },
    "iconfinder": {
        "api_key": "YOUR_ICONFINDER_KEY"
    }
}
```

**API Notes | API 说明**:

- **LLM API** (Claude/GPT): Used for Planner and Coder agents
  - Recommended: **Claude-4-Opus** for best Manim code quality
- **LLM API** (Claude/GPT)：用于 Planner 和 Coder 智能体
  - 推荐使用 **Claude-4-Opus** 以获得最佳 Manim 代码质量

- **VLM API** (Gemini): Used for Planner Critic agent
  - For layout and aesthetics optimization
  - Recommended: **gemini-2.5-pro-preview-05-06**
- **VLM API** (Gemini)：用于 Planner Critic 智能体
  - 用于布局和美学优化
  - 推荐使用 **gemini-2.5-pro-preview-05-06**

- **Visual Assets API** (IconFinder): For enriching videos with icon resources
- **Visual Assets API** (IconFinder)：用于丰富视频的图标资源

### 3. Generate Educational Videos with Code2Video | 使用 Code2Video 生成教学视频

#### Method 1: Single Knowledge Point | 方式一：单知识点生成

```bash
cd src/
sh run_agent_single.sh --knowledge_point "AVL Tree Rotation Operations"
```

**Parameter Notes** (configure in `run_agent_single.sh`):

**参数说明**（在 `run_agent_single.sh` 中配置）：

- `API`: Specify which LLM to use (e.g., `claude`)
- `API`: 指定使用的 LLM（如 `claude`）

- `FOLDER_PREFIX`: Output folder prefix (e.g., `VisualKiwi-single`)
- `FOLDER_PREFIX`: 输出文件夹前缀（如 `VisualKiwi-single`）

- `KNOWLEDGE_POINT`: Target concept, e.g., `"AVL Tree Rotation Operations"`
- `KNOWLEDGE_POINT`: 目标概念，如 `"AVL树旋转操作"`

#### Method 2: Batch Generation | 方式二：批量生成

```bash
cd src/
sh run_agent.sh
```

**Parameter Notes** (configure in `run_agent.sh`):

**参数说明**（在 `run_agent.sh` 中配置）：

- `API`: Specify which LLM to use
- `API`: 指定使用的 LLM

- `FOLDER_PREFIX`: Output folder prefix (e.g., `VisualKiwi-batch`)
- `FOLDER_PREFIX`: 输出文件夹前缀（如 `VisualKiwi-batch`）

- `MAX_CONCEPTS`: Number of concepts to include (`-1` means all)
- `MAX_CONCEPTS`: 要包含的概念数量（`-1` 表示全部）

- `PARALLEL_GROUP_NUM`: Number of groups to run in parallel
- `PARALLEL_GROUP_NUM`: 并行运行的组数

### 4. Project Structure | 项目结构

```
Code2Video/
│── src/
│   ├── agent.py              # Core agent implementation | 核心智能体实现
│   ├── run_agent.sh          # Batch generation script | 批量生成脚本
│   ├── run_agent_single.sh   # Single knowledge point script | 单知识点生成脚本
│   ├── api_config.json       # API configuration | API 配置
│   └── ...
│
├── assets/
│   ├── icons/                # Visual asset cache from IconFinder | IconFinder 下载的视觉资源缓存
│   └── reference/            # Reference images | 参考图像
│
├── json_files/               # JSON-based topic lists & metadata | JSON 格式的主题列表和元数据
├── prompts/                  # Prompt templates for LLM calls | LLM 调用的提示模板
│   ├── stage1.py            # Planner stage | Planner 阶段
│   ├── stage2.py            # Coder stage | Coder 阶段
│   ├── stage3.py            # Critic stage | Critic 阶段
│   └── ...
│
└── CASES/                    # Generated cases, organized by FOLDER_PREFIX | 生成的案例，按 FOLDER_PREFIX 组织
    └── VisualKiwi-single/   # Example single-topic generation results | 示例单主题生成结果
```

---

## 💡 Use Cases | 使用案例

### Case 1: Interactive AVL Tree Learning | 案例 1：交互式 AVL 树学习

**Student Prompt | 学生提示**:
> "I keep mixing up AVL rotations (LL/RR/LR/RL). Can you teach me with a video, but also let me manipulate nodes myself to see how balance factors change?"
> "我总是搞混 AVL 旋转（LL/RR/LR/RL）。你能用视频教我，同时让我自己操作节点来观察平衡因子的变化吗？"

**VisualKiwi Output | VisualKiwi 输出**:

1. **Generated Demonstration Video** (step-by-step, pausable)
   - Builds an AVL tree from an insertion sequence (e.g., 10 → 20 → 30 → 25 → 28)
   - At each step, overlays: node height, balance factor, and the first unbalanced ancestor
   - Shows the exact rotation type triggered (LL/RR/LR/RL) with before/after snapshots
   - Narrates the "why": which subtree got heavier and why that implies a specific rotation
1. **生成的演示视频**（分步、可暂停）
   - 从插入序列构建 AVL 树（如 10 → 20 → 30 → 25 → 28）
   - 每一步显示：节点高度、平衡因子、第一个不平衡的祖先节点
   - 显示触发的旋转类型（LL/RR/LR/RL），包含前后快照
   - 旁白解释"为什么"：哪个子树变重了，为什么需要特定旋转

2. **Interactive Frontend** (hands-on AVL editor)
   - Canvas: draggable tree nodes and edges (students can swap/reconnect nodes)
   - Side panel: real-time height + balance factor per node; highlights rule violations
   - Controls: Insert, Delete, Step, Auto-Rotate, Hint, Reset, Generate New Sequence
   - Validation: checks BST ordering and AVL balance constraints instantly
2. **交互式前端**（AVL 编辑器）
   - 画布：可拖拽的树节点和边（学生可以交换/重新连接节点）
   - 侧边栏：每个节点的实时高度和平衡因子；高亮显示规则违反
   - 控制：插入、删除、单步、自动旋转、提示、重置、生成新序列
   - 验证：即时检查 BST 排序和 AVL 平衡约束

**Key Interactions | 关键交互**:
- Students can intentionally drag the tree into an unbalanced state; the UI highlights the culprit node and suggests candidate rotations
- 学生可以故意将树拖到不平衡状态；UI 高亮显示问题节点并建议候选旋转

- Students choose a rotation manually; the system verifies correctness and explains mistakes
- 学生手动选择旋转；系统验证正确性并解释错误

- "What-if" mode: change the insertion order or delete a node and watch the rotation strategy change
- "假设"模式：改变插入顺序或删除节点，观察旋转策略的变化

### Case 2: Interactive Chemistry Titration Lab | 案例 2：交互式化学滴定实验

**Student Prompt | 学生提示**:
> "I don't understand why titration curves look different for strong vs weak acids. Can I interactively explore it and see the equivalence point?"
> "我不理解为什么强酸和弱酸的滴定曲线看起来不同。我能交互式地探索它并看到等当点吗？"

**VisualKiwi Output | VisualKiwi 输出**:

- **Lab Control Panel | 实验控制面板**:
  - Choose a system: strong acid–strong base / weak acid–strong base / weak acid–weak base
  - 选择系统：强酸-强碱 / 弱酸-强碱 / 弱酸-弱碱

  - Parameters: initial concentration, volume, Ka/Kb (optional temperature)
  - 参数：初始浓度、体积、Ka/Kb（可选温度）

  - Operation: a slider controlling added titrant volume (like turning a burette)
  - 操作：控制添加滴定剂体积的滑块（像转动滴定管）

- **Real-Time Visuals | 实时可视化**:
  - Dynamic pH vs volume curve
  - 动态 pH vs 体积曲线

  - Species composition view (HA/A⁻, H⁺/OH⁻ proportions)
  - 物种组成视图（HA/A⁻, H⁺/OH⁻ 比例）

  - Automatic markers for buffer region and equivalence point
  - 缓冲区和等当点的自动标记

  - Explanation triggers: crossing key regions (buffer → equivalence → excess base) pops concise explanations of the chemistry behind the curve shape
  - 解释触发器：跨越关键区域（缓冲 → 等当 → 过量碱）时弹出简洁的化学解释

**Key Interactions | 关键交互**:
- Adjust Ka and immediately see buffer region width and equivalence-point pH shift
- 调整 Ka 并立即看到缓冲区域宽度和等当点 pH 偏移

- "Indicator mode": choose an indicator; the UI shows whether its color-change range matches the equivalence point
- "指示剂模式"：选择指示剂；UI 显示其颜色变化范围是否匹配等当点

---

## 🔧 Integration with VisualKiwi MCP Server | 集成到 VisualKiwi MCP 服务器

### MCP Server Interface Design | MCP 服务器接口设计

VisualKiwi acts as an MCP server, receiving user prompts and returning visual components:

VisualKiwi 作为 MCP 服务器，接收用户提示并返回视觉组件：

```python
# Pseudocode example | 伪代码示例
def visualkiwi_mcp_tool(user_prompt: str) -> Dict:
    """
    Generate visual components based on user prompt
    根据用户提示生成视觉组件
    
    Returns | 返回格式:
    {
        "type": "video" | "interactive" | "slides",
        "content": "...",
        "metadata": {...}
    }
    """
    # 1. Analyze user intent | 分析用户意图
    intent = analyze_intent(user_prompt)
    
    # 2. Select appropriate generator | 选择合适的生成器
    if intent.needs_video:
        # Use Code2Video | 使用 Code2Video
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
        # Use interactive Canvas | 使用交互式 Canvas
        canvas = generate_interactive_canvas(intent)
        return {
            "type": "interactive",
            "content": canvas.component,
            "metadata": {...}
        }
    # ...
```

### Frontend Rendering | 前端渲染

In the chat interface, render different components based on the returned type:

在聊天界面中，根据返回的类型渲染不同的组件：

```html
<!-- Video Component | 视频组件 -->
<iframe 
    src="generated_video.html" 
    width="100%" 
    height="600px"
    allowfullscreen>
</iframe>

<!-- Interactive Canvas | 交互式 Canvas -->
<div id="interactive-canvas">
    <!-- React/Web Components | React/Web 组件 -->
</div>

<!-- Rich-Content Slides | 富内容幻灯片 -->
<div class="slides-container">
    <!-- Reveal.js or other slide frameworks | Reveal.js 或其他幻灯片框架 -->
</div>
```

---

## 📊 Tech Stack | 技术栈

### Video Generation | 视频生成
- **Code2Video**: Educational video generation framework based on Manim
- **Code2Video**: 基于 Manim 的教学视频生成框架

- **Remotion**: React video editing and composition
- **Remotion**: React 视频编辑和合成

- **Manim Community v0.19.0**: Mathematical animation engine
- **Manim Community v0.19.0**: 数学动画引擎

### Interactive Visualization | 交互式可视化
- **React**: Frontend framework
- **React**: 前端框架

- **AG-UI / Custom Protocol**: UI component system
- **AG-UI / 自定义协议**: UI 组件系统

- **Mermaid**: Diagrams and flowcharts
- **Mermaid**: 图表和流程图

- **Reveal.js**: Slide framework
- **Reveal.js**: 幻灯片框架

### Multi-Agent System | 多智能体系统
- **LangGraph**: Agent orchestration
- **LangGraph**: 智能体编排

- **Instructor**: Structured output
- **Instructor**: 结构化输出

- **RAG**: Retrieval-Augmented Generation
- **RAG**: 检索增强生成

### Graphics and Rendering | 图形和渲染
- **React D3 Tree**: Tree visualization
- **React D3 Tree**: 树形可视化

- **Excalidraw**: Drawing and feedback
- **Excalidraw**: 绘图和反馈

- **XYFlow**: Flowcharts and node graphs
- **XYFlow**: 流程图和节点图

---

## 🎯 Development Roadmap | 开发路线图

### Phase 1: Code2Video Integration (Current) | 阶段 1：Code2Video 集成（当前）
- [x] Integrate Code2Video core functionality
- [x] 集成 Code2Video 核心功能

- [x] Configure APIs and dependencies
- [x] 配置 API 和依赖

- [ ] Create MCP server interface
- [ ] 创建 MCP 服务器接口

- [ ] Implement video generation API
- [ ] 实现视频生成 API

### Phase 2: Interactive Components | 阶段 2：交互式组件
- [ ] Develop interactive Canvas components
- [ ] 开发交互式 Canvas 组件

- [ ] Implement AVL tree editor
- [ ] 实现 AVL 树编辑器

- [ ] Implement chemistry lab simulator
- [ ] 实现化学实验模拟器

- [ ] Integrate React frontend
- [ ] 集成 React 前端

### Phase 3: Multi-Agent Orchestration | 阶段 3：多智能体编排
- [ ] Implement Planner Agent
- [ ] 实现 Planner Agent

- [ ] Implement Coder Agent (based on Code2Video)
- [ ] 实现 Coder Agent（基于 Code2Video）

- [ ] Implement Critic Agent
- [ ] 实现 Critic Agent

- [ ] Implement resource management Agent
- [ ] 实现资源管理 Agent

### Phase 4: MCP Server | 阶段 4：MCP 服务器
- [ ] Implement MCP protocol interface
- [ ] 实现 MCP 协议接口

- [ ] Integrate with Kiwi platform
- [ ] 集成到 Kiwi 平台

- [ ] Testing and optimization
- [ ] 测试和优化

---

## 🤝 Contributing | 贡献指南

Contributions are welcome! Please follow these steps:

欢迎贡献！请遵循以下步骤：

1. Fork this repository
1. Fork 本仓库

2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)

3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)

4. Push to the branch (`git push origin feature/AmazingFeature`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)

5. Open a Pull Request
5. 开启 Pull Request

---

## 📌 Related Resources | 相关资源

### Video Generation Frameworks | 视频生成框架
- [Code2Video](https://showlab.github.io/Code2Video/) - Core framework this project is based on | 本项目基于的核心框架
- [Remotion](https://www.remotion.dev/) - React video editing | React 视频编辑
- [Generate Explanation Videos](https://arxiv.org/html/2502.19400v1) - Related research | 相关研究

### UI Protocols | UI 协议
- [JSON Render](https://github.com/vercel-labs/json-render)
- [Tambo](https://github.com/tambo-ai/tambo)

### Agent Frameworks | 智能体框架
- [Instructor](https://github.com/567-labs/instructor)
- [LangGraph](https://github.com/langchain-ai/langgraph)

### Graphs and Visualization | 图表和可视化
- [XYFlow](https://github.com/xyflow/xyflow)
- [Excalidraw](https://github.com/excalidraw/excalidraw)
- [React D3 Tree](https://github.com/bkrem/react-d3-tree)
- [Mermaid](https://github.com/mermaid-js/mermaid)
- [Reveal.js](https://github.com/hakimel/reveal.js)

---

## 🙏 Acknowledgements | 致谢

- **Code2Video Team**: Provided an excellent code-driven video generation framework
- **Code2Video 团队**：提供了优秀的代码驱动视频生成框架

- **Manim Community**: Powerful mathematical animation engine
- **Manim Community**：强大的数学动画引擎

- **3Blue1Brown**: Inspired the design philosophy of educational videos
- **3Blue1Brown**：启发了教学视频的设计理念

- **Show Lab @ NUS**: Original development team of Code2Video
- **Show Lab @ NUS**：Code2Video 的原始开发团队

---

## 📄 License | 许可证

This project is based on the Code2Video project. Please refer to the original project's LICENSE file.

本项目基于 Code2Video 项目，请参考原始项目的 LICENSE 文件。

---

## 📧 Contact | 联系方式

For questions or suggestions, please contact us via:

如有问题或建议，请通过以下方式联系：

- Submit an Issue
- 提交 Issue

- Open a Pull Request
- 开启 Pull Request

---

<p align="center">
  <b>Make learning visual, interactive, and fun!</b>
<br>
  <b>让学习变得可视化、交互式和有趣！</b>
</p>
