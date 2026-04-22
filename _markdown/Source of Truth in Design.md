---
title: "Source of truth in Design"
permalink: /source-of-truth-in-design/
listed: true
---

在数字产品设计与工程的语境中，**单一事实来源 (Single Source of Truth, SSOT)**，或简称为 **Source of Truth (SoT)**，指的是一个明确的、集中的、具有绝对权威性的参考库或系统。它规定了产品在视觉呈现、交互逻辑和底层架构上“究竟应该是什么样”。

当设计团队、产品经理 (PM) 和前端工程师对某个按钮的圆角半径、某种主品牌色的十六进制代码、或某个组件的交互状态产生分歧时，**Source of Truth 就是最终的仲裁者**。

为了深入理解这个概念，我们可以将其拆解为系统构成、演进历程以及它在当下面临的结构性危机。

### 一、 Source of Truth 的系统构成

一个成熟的现代设计体系中，Source of Truth 通常由以下几个层级堆叠而成（这在本质上是一种系统工程 Systems Engineering 的降维应用）：

1. **设计令牌 (Design Tokens)：** 这是 SoT 的原子层。它将硬编码的数值（如 `#FF0000` 或 `16px`）抽象为具有语义的变量（如 `color-brand-primary` 或 `spacing-medium`）。它是跨平台一致性的基石。
2. **组件库 (Component Library)：** 使用 Tokens 构建的模块化 UI 元素（如按钮、输入框、导航栏）。SoT 规定了这些组件在不同状态下（Default, Hover, Disabled, Focused）的具体表现。
3. **模式与规范 (Patterns & Guidelines)：** 规定组件如何组合使用的宏观逻辑，例如“在破坏性操作的弹窗中，主要按钮必须放置在右侧且显示为红色”。
4. **交互文档 (Interaction/Behavioral Specs)：** 定义动效时长、缓动曲线 (Easing curves) 以及状态切换的逻辑。

### 二、 范式的演进：谁掌握了 SoT，谁就掌握了话语权

设计工具的更迭史，本质上就是对 Source of Truth 解释权的争夺史。

- **前置阶段（像素时代）：** Photoshop 时代没有真正的 SoT。设计稿是一张静态的位图 (Bitmap)，开发者靠肉眼测量和切图，实现结果与设计稿之间存在巨大的“翻译损耗”。
- **第一代 SoT（矢量与符号）：** Sketch 引入了 Symbols（符号），将 UI 元素模块化，确立了“设计文件”本身可以作为视觉的规范来源。
- **第二代 SoT（云端与全链路系统化）：** Figma 的崛起在于它建立了一套极其庞大且严密的私有原语（Variables, Variants, Auto-layout）。它让设计文件不仅仅是视觉稿，而是变成了一个**具有伪代码逻辑的关系型数据库**。Figma 成功说服了行业：**Figma 文件就是 Source of Truth**。工程师必须查阅 Figma 来编写代码。

### 三、 核心冲突：意图的近似值 vs. 物理现实

在实际运作中，将 Figma 等设计工具作为 Source of Truth 存在一个根本性的哲学悖论：**设计工具描绘的是“意图 (Intent)”，而代码才是产品最终存在的“物理现实 (Reality)”。**

- **The Translation Penalty（翻译惩罚）：** 当 Figma 宣称自己是 SoT 时，工程师每天的工作就是将 Figma 的专有原语（如嵌套了 8 层的 Variant）“翻译”成 React 或 Vue 的组件。这种翻译永远是有损的。
- **State Desynchronization（状态脱节）：** 如果工程师在代码库中为了修复一个 Bug 而微调了组件的 padding，但没有同步回 Figma（所谓的 Back-porting），Figma 作为 SoT 的权威性就瞬间瓦解了。久而久之，Figma 变成了“我们希望它是怎样的”，而 GitHub 代码库才是“它实际上是怎样的”。

### 四、Figma 的结构性劣势

- **训练数据的错位**：Figma 的胜利建立在其封闭、缺乏文档化且难以通过编程直接操作的专有格式上。这一护城河在 Agentic Era 变成了致命弱点——LLM 是基于海量代码（HTML/CSS/JS）训练的，而不是 Figma 的私有原语。
- **巴洛克式的系统冗余 (Baroque Infrastructure)**：Figma 为适配工程化需求，堆砌了极其复杂的系统（如 900+ 个颜色变量嵌套、无尽的组件变体和 Prop 属性）。当 AI 代理能够直接生成和修改高质量的底层代码时，这种在“有损近似媒介”中进行的手动系统化维护显得荒谬且低效。
- **Figma Make 的局限**：作者认为 Figma 推出的 AI 工具（Figma Make）仅仅是在现有的封闭系统中打补丁，它依然错误地假定“设计文件是权威的”，服务于那些被锁定在 Figma 生态内的用户。

### 五、 代理时代 (Agentic Era) 的回归：代码即 SoT

正如关于 Claude Design 的批判所指出的，大语言模型 (LLM) 和 Agentic Workflow 的爆发，正在强行将 Source of Truth 从专有的设计工具拉回到**代码库 (Codebase)** 本身。

1. **AI 的认知基础：** AI 编程代理（如 Claude Code、Cursor）是基于海量的 HTML、CSS、JavaScript 和 React 组件进行预训练的。它们理解 DOM 树，理解 CSS 盒模型，但它们不理解（也无法直接操作）Figma 封闭的二进制文件或私有节点树。
2. **Truth to Materials（材料的真实性）：** 如果最终的媒介是 Web 或 App 原生代码，那么直接在代码环境中定义变量、构建组件，并让 AI 代理实时渲染出视觉界面，消除了所有中间环节的损耗。
3. **消除“逆向同步”摩擦：** 当代码成为了唯一且绝对的 Source of Truth，设计与开发的界限将被溶解。设计师调整视觉，本质上就是在直接修改底层的 Design Tokens (CSS 变量或 JSON 配置文件)；工程师优化逻辑，视觉会自动更新。两者共享同一个物理现实，不再需要维护一个复杂的、平行的“视觉近似系统”。

简而言之，Source of Truth 在设计中就是**避免重复造轮子并消除沟通歧义的单一标准**。而在 AI 重塑生产流的当下，这个标准正在经历从“复杂的视觉规范文件”向“结构化的机器可读代码”的剧烈转移。