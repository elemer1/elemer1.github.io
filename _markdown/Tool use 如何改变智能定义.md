---
title: Tool Use 如何改写"智能"的定义
permalink: /tool-use-redefines-intelligence/
listed: true
---

## 一个被默认了七十五年的结构性前提

Alan Turing 在 1950 年发表于 *Mind* 的《Computing Machinery and Intelligence》里完成了一次重要的概念澄清。他把"机器能否思考"这个含糊的形而上学问题转译为一个可操作的判断题：在仅凭文字交换信息的条件下，如果一台机器的应答使观察者无法把它与人类区分开来，那么再坚持否认它"能思考"就会变得论证上乏力（Turing, 1950）。这个转译本身是有力的——它把一个定义之争推进到了检验之境，也奠定了随后几十年机器智能研究的基本形状。

然而这套设想里藏着一个结构性前提：**智能被默认为发生在封闭认知系统内部的属性**，它可以通过一台被隔离起来、只与外界交换符号的机器来展示和衡量。图灵设想中的那间房间，是一个认识论上的单子。房间内部的一切——记忆、推理、规划——必须独立完成，不得向外求援。

这个默认，七十年里塑造了 AI 研究的主流路径。从 Weizenbaum 1966 年的 ELIZA（Weizenbaum, 1966），到 Winograd 1972 年的 SHRDLU，到 Newell & Simon 那一脉物理符号系统假说（Newell & Simon, 1976），再到深度学习时代 Brown 等人在 2020 年公开的 GPT-3（Brown et al., 2020），衡量一个系统智能程度的主流方法始终是：给它一段封闭的输入，观察它在不借助外部资源的前提下能产出什么。Prompt engineering 在这个范式里成了一门独立手艺，但它所服务的对象，本质上是一个被隔离起来的神谕。

2022 至 2025 这四年间真正被拆解的，已经超过了模型能力这一层——它触及并改写了那个存续七十五年的预设本身。到 2025 年末，**仍然以"模型在封闭对话中能答什么"来衡量 AI 进展的人，其评估框架相对于工业前沿至少已经滞后两代**。本文要追溯的，是这场预设迁移的技术路径与其背后的哲学意涵。

---

## 一、Oracle 时代：参数里的智能

GPT-3 在 2020 年夏天发布时，产业界形成的主流使用姿势可以概括为"把模型当作神谕"：给它一段 prompt，它返回一段续写。中间没有工具、没有持久状态、没有动作。所有认知工作都必须被压入一次 forward pass——即一次"从 prompt 到续写"的参数推理——之内完成。

这一时期的震撼源自一种新鲜感：模型竟然能写出可读的诗句，能做一定程度的机器翻译，能解某些数学题，能续写结构合理的 Python 代码。工程上的几乎所有努力都集中在一个方向——把更多的知识和推理能力压入模型参数、让单次 forward pass 产生更多可用的输出。Wei 等人 2022 年在 NeurIPS 上提出的 Chain-of-Thought prompting 是这个范式的典型延伸：通过在 prompt 中诱导模型"把推理步骤写出来"，可以显著提升其在算术与常识推理任务上的表现（Wei et al., 2022）。但整个机制的边界仍然锁在同一间房间里——模型的所有思考都以 token 的形式发生在自己脑中。

这一范式的上限是清晰的。模型知道的事情被训练数据截断。它的算术逼近于语言模型的统计直觉而非可验证的计算过程——Cobbe 等人 2021 年在 *arXiv* 发布的 GSM8K 基准正是为揭示这一点设计（Cobbe et al., 2021）。它访问不了当天的新闻、企业的数据库、任意 API、文件系统。它没有手段执行代码来检验自己输出的正确性。所有这些限制在当时被普遍理解为"模型还不够强"——那是一个工程意义上待规模化解决的问题，scaling law（Kaplan et al., 2020; Hoffmann et al., 2022）被认为会逐步消化它。

直到学界开始意识到，这里要解的问题在类型学上就不同。模型能力的扩张当然重要，但把所有认知负载都塞进参数里这件事，从根本上回避了**认知可以借助环境资源**这一人类智能里最基本的事实。这一反思指向了一个后来被反复验证的判断：瓶颈不在模型容量，而在模型被使用的姿势。

---

## 二、ReAct 与 Toolformer：推理与行动的合流（2022–2023）

真正的分水岭出现在 2022 年 10 月。Yao 等人在一篇题为 *ReAct: Synergizing Reasoning and Acting in Language Models* 的论文中提出了一个朴素却决定性的设想：让模型在生成推理链的过程中穿插 "action" 步骤——调用搜索引擎、查询 Wikipedia API、读取知识库——并将返回的 observation 重新喂回到推理链中，再进入下一步思考（Yao et al., 2022）。这篇论文在 HotpotQA、FEVER、ALFWorld 等跨域基准上的表现都超过了纯 Chain-of-Thought 的基线。

表面上这是一个工程 trick，背后触及的却是认知结构的问题：**模型的推理过程可以突破自身参数边界**。思考被允许把一部分工作外包给世界。Yao 等人的贡献并非发明了"工具使用"这个想法——Nakano 等人在 2021 年的 WebGPT 工作里已经训练了一个能通过浏览器搜索信息的模型（Nakano et al., 2021）——而是把推理与动作这两个过去被割裂处理的模态缝合在同一个生成循环里。ReAct 之所以重要，是因为它证明这种缝合不需要重新训练模型，只需要恰当的 prompt 结构。

几乎同时出现的另一条路径来自 Meta FAIR。Schick 等人 2023 年发布的 *Toolformer: Language Models Can Teach Themselves to Use Tools*（八位作者联合署名）给出了一个互补的工程答案：用自监督学习的方式让模型在预训练阶段就学会判断何时需要调用外部工具、调用哪个、以及如何解释返回值（Schick et al., 2023）。这两条路径——prompt 层面的 ReAct 与训练层面的 Toolformer——共同把"tool use"从一种后处理式的工程 hack，推上了研究议程。

商业产品的反应速度惊人。2023 年 3 月，OpenAI 为 ChatGPT 上线 Plugin 接口，把第三方 API 纳入模型的调用范围；同年 6 月，OpenAI 在 API 层发布 function calling，允许开发者以结构化的方式为模型注册外部函数，由模型自主决定调用时机与参数（OpenAI, 2023）。开源生态同期迅速成型：Harrison Chase 启动的 LangChain 项目将"模型 + 工具 + 循环"这个模式封装成可复用的工程框架；Torantulino 在 GitHub 上开放的 AutoGPT 把"让模型自己循环调用工具直到完成目标"这一设想推到了公众面前。那段时间整个 AI 工程文化的重心，从"如何写好 prompt"悄悄挪到了"如何为模型配好工具并编排其调用"。

但 2023 年的 tool use 仍然脆弱。模型调用工具的成功率不高，在长对话里频繁丢失上下文，幻觉率显著。AutoGPT 最有名的特征是它能跑起来——但它几乎跑不完任何一件真实的事。用户的典型体验是看它在一个循环里反复调用同一个 API、烧掉 OpenAI credits，最终卡住。那一年真正令人激动的是**可能性**，可用性还远没有到位。Chase 在 LangChain 的早期文档里承认，那一阶段的 agent framework 更像是"在产品原型阶段"的展示，而非适合生产环境的基础设施。

---

## 三、2024：从玩具到工具的过渡年

2024 年是关键的一年。几件原本独立演化的事在这一年收敛。

第一是模型本身在工具使用上的可靠度进入了实用区间。Anthropic 2024 年 3 月发布的 Claude 3 Opus 及之后迭代的 Claude 3.5 Sonnet 是许多开发者第一次"感到模型能听话使用一组工具"的节点——模型学会了等待工具返回之后再继续，而不是在 observation 位置幻觉一个伪 API response。OpenAI 的 GPT-4 Turbo、Google 的 Gemini 1.5 也在同一时期把可用性推到了类似水位。这一阶段工程人员对模型的直觉发生了一次迁移：从"它在胡说八道"变成"它会按协议办事"。

第二是模型开始能把**整台计算机本身**作为工具。Anthropic 在 2024 年 10 月 22 日发布 Computer Use 功能，开放 Claude 3.5 Sonnet 的公测版本，允许模型直接操控一个桌面环境——观察屏幕截图、移动鼠标、输入键盘事件（Anthropic, 2024a）。官方公告中附带了一组颇有说服力的数字：同一更新同时把 SWE-bench Verified 的得分从 33.4% 提升到 49.0%，在 τ-bench 的零售域从 62.6% 提升到 69.2%、航空域从 36.0% 提升到 46.0%（Anthropic, 2024a）。更早几个月，创业公司 Cognition 在 2024 年 3 月用一个叫 Devin 的 demo 把"AI 软件工程师"这个概念直接扔到了公众面前，演示视频在社交媒体上掀起了关于演示真实性的激烈争论。无论那一次 demo 的含水量如何估计，Devin 改变了一件事——它把 "agent" 这个原本与 AutoGPT 式玩具绑定的词汇，拉进了"可能真的能用来干活"的讨论范围。

第三是评测体系的重心悄然迁移。2023 年学界还在 MMLU（Hendrycks et al., 2021）、GSM8K（Cobbe et al., 2021）这类静态知识与推理题上排名次；从 2024 年开始，认真讨论的基准换成了 SWE-bench（Jimenez et al., 2023，Princeton / University of Chicago 团队，要求模型从真实 GitHub 仓库中独立解决 issue）、WebArena（Zhou et al., 2023，CMU 团队，让模型在逼真的网页环境中完成多步任务）、以及 τ-bench（Yao et al., 2024，测试模型在客户服务对话中完成完整多步任务的能力）。这些基准衡量的对象换了一个层级——从"模型能答出什么"挪到了"agent 能完成什么"。这里发生的已经超出了指标迭代的范畴，它改写的是评价哲学本身。

第四是基础设施开始形成标准。2024 年 11 月 25 日，Anthropic 开源了 Model Context Protocol（MCP），一个用于标准化 AI 应用与外部工具、数据源之间连接方式的协议（Anthropic, 2024b）。MCP 的目标是把之前每个模型厂商各自造一套工具接入机制的"N × M 接入问题"——N 个模型厂商乘以 M 个数据源，每一组合都要单独开发——折叠成一个"实现一次 client、实现一次 server"的通用协议。技术上它借鉴了微软 VS Code 团队发明的 Language Server Protocol（LSP），传输层基于 JSON-RPC 2.0。那一刻外界对它的反应并不强烈，部分开发者在 Hacker News 上的评论用了"another standard that will die in committee"这样的句子。然而一年之后，OpenAI CEO Sam Altman 在 2025 年 3 月公开宣布全线产品支持 MCP，Google DeepMind 的 Demis Hassabis 在 4 月确认 Gemini 系列支持，GitHub、Block、Replit、Sourcegraph 等工具链公司相继接入；到 2025 年 12 月，Anthropic 把 MCP 捐赠给了 Linux Foundation 旗下新成立的 Agentic AI Foundation，MCP 成为事实上的行业标准（The New Stack, 2025）。

这四条线索同时抵达某个临界点的时候，2024 年的整体形势可以被这样描述：模型够可靠了，计算机整体成了工具，评测从静态知识转向动态任务，接入协议开始标准化。**每一项单独看都是渐进的，合在一起形成的是姿势层面的代际迁移。**

---

## 四、2025：agent 成为默认工作方式

2025 年的变化发生得很快。一年之内，"让 agent 去跑"从一种实验性做法变成了**工程上的默认姿势**。

观察产业变化最直观的方式，是看从业者坐在编辑器前的实际行为。2022 年的一个工程师在 IDE 前自己打字，偶尔问 AI 一两句；2025 年的同一位工程师，屏幕上开着若干 Claude Code 或类似 agent 会话在并行跑任务，他自己在几个任务之间切换做 review。Anthropic 2025 年发布 Claude Sonnet 4.5 时，官方报告了一个具体数字——它可以在一个复杂软件工程任务中连续执行超过 30 小时而不失去一致性（Anthropic, 2025a）。这件事在两年前是科幻。

能力基准上的变化同样剧烈。SWE-bench Verified 这一由 OpenAI 在 2024 年 8 月精选并校验过的 500 题子集，2024 年初的 SOTA 还在 30% 区间；2024 年底 Claude 3.5 Sonnet (new) 做到 49%；到 2025 年 11 月，Anthropic 发布的 Claude Opus 4.5 成为**首个突破 80% 阈值的模型**，具体得分 80.9%（Anthropic, 2025b）。截至本文写作时，SWE-bench 榜单首位的 Claude Opus 4.7 已将该得分推进到 82.0%（SWE-bench Leaderboard, 2026）。基准测试本身也在追着能力跑——研究社区在 2025 年发布了 SWE-bench Pro、SWE-bench Live（Zan et al., 2025）、SWE-Lancer（OpenAI, 2025）等更难的版本。SWE-Lancer 尤其有意思——它让 agent 跑真实的 Upwork 自由职业任务，评价指标是"最终交付物能从人类客户那里拿到多少美元的报酬"。评测体系从"静态答题"移动到了"经济意义上的有效产出"。

具体变化发生在四个维度上。

**时间尺度**发生了一个数量级的拉伸。Oracle 时代"模型帮我干一件事"的自然时间单位是秒到分钟；2025 年的典型单位变成了数十分钟到数小时。一个 coding agent 接到复杂重构任务后运行 40 分钟，读取数十个文件，在其中一半被自己运行的测试推翻后重来——这个过程中没有人类在 loop 里。人类只在开头定义问题、在结尾验收结果。

**并行度**发生了一个对应的跃迁。单位任务时长拉伸，加上边际推理成本持续下降，使得"一个用户同时监管多个 agent"从小众操作变成了普通工作流。用户在 A 任务上等着的时候去启动 B 任务，B 任务跑的时候回去审 A 的进度。人类在工作流里的角色从执行者转变为调度者——这种转变在 2025 年的开发者社群讨论中被反复提及，业界习惯用"从 IC（individual contributor）变成 manager"这个类比来概括它。

**协作结构**也变了。2025 年许多严肃工作流里，在跑的已经是一组分工明确的多 agent 系统，单 agent 反倒成了简单场景的特例：一个 agent 负责规划，一个执行，一个审查，一个回放日志查错。Anthropic 2025 年公开的内部工程经验与 Google DeepMind、OpenAI 相继发布的 agent 框架里，multi-agent orchestration 都成了核心设计话题（Anthropic, 2025c；参见 Schick 等人后续工作）。MCP 的生态作用在这里至关重要——它让一组 agent 之间的工具调用可以跨厂商、跨模型、跨环境复用，从外部看这是件没有多少声响的工程事件，从内部看它是决定性的。

**开发经验的沉淀方向**也迁移了。2023 年工程圈讨论的是"怎么写 prompt"；2024 年是"怎么接工具"；2025 年则围绕一整套新问题展开：context engineering（如何编排上下文以让 agent 在长任务中保持一致）、tool ergonomics（如何为模型设计易用的工具接口）、observability（如何对 agent 的决策过程做可回放的可观测性）、以及 evaluation under agentic settings（在 agent 场景下如何定义和测量性能）。Anthropic 工程团队 2025 年连续发布的多篇技术博客——关于 effective context engineering、building effective agents、以及 skills 框架——可以被视为这一新工程学科的早期权威文献（Anthropic, 2024c; 2025d）。

**回头看，从 ReAct 这篇 2022 年 10 月的论文到 2025 年的产业爆发，中间走了大约三年。这三年里没有发生一次算力意义上的"质变"——底层架构仍然是 transformer，scaling law 仍然是那个 scaling law。真正变的是姿势：从让模型在脑子里想明白，转变为让模型调动外部世界的资源去把事情做成。**

---

## 五、延展心智：从哲学论证到工程默认

这场工程迁移在无意中回答了一个已经被辩论了二十多年的哲学问题。

1998 年，Andy Clark 与 David Chalmers 在 *Analysis* 期刊上合作发表了 *The Extended Mind*（Clark & Chalmers, 1998）。他们提出了一个在当时颇具挑衅意味的主张：**人类认知从来就不是严格发生在颅骨之内的**。他们设计了一个思想实验——Otto 与 Inga。Inga 听说博物馆有一场展览，她在记忆里回想起博物馆地址，动身前往；Otto 患有早期阿兹海默症，他随身携带一个笔记本，听说展览后他翻开笔记本查到了博物馆地址，动身前往。Clark 与 Chalmers 的论点是：如果 Inga 从生物记忆中调用地址这件事可以算作一次认知过程，那么 Otto 从笔记本中调用地址这件事也同样应该被算作一次认知过程——两者在功能角色上对等（他们称之为 parity principle）。差别仅在于信息载体是神经元还是纸页，而功能主义的立场下，载体差别不足以构成认知论上的类别差别。

这个观点在哲学圈内部一度引发激烈反弹。Adams 与 Aizawa（2008）等人批评它过度稀释了"心智"这个概念的边界，认为若允许笔记本进入认知系统，那手机、图书馆、朋友的大脑也都将被迫算作认知的一部分——这使得心智的外延变得几乎不可控。但 Clark 的回应是——**他接受这个推论**。他后来在 *Natural-Born Cyborgs*（Clark, 2003）和 *Supersizing the Mind*（Clark, 2008）中进一步阐述：人类之所以为人类，恰恰在于大脑是一种特别擅长把自己嵌入外部工具脚手架的器官；颅内的生物认知与颅外的技术支架本就是同一套系统演化上的两面。

这类论点在认知科学中并不孤立。Hutchins 1995 年的 *Cognition in the Wild* 通过对海军舰船导航团队的民族志研究，展示了一次复杂导航计算如何分布在多人、多工具、多外部表征之间——"认知"发生在整个团队 - 工具系统里，而非任一个个体头脑里（Hutchins, 1995）。Donald Norman 在 *Things That Make Us Smart*（1993）里指出人类智能的一大特征是"认知外包"（cognitive offloading）——我们把算术交给计算器，把记忆交给日历，把注意力交给待办清单。早期具身认知研究者 Rodney Brooks 在 MIT AI Lab 1991 年的 *Intelligence Without Representation* 则从机器人学方向挑战了传统符号主义的"所有智能都要在模型内部完成"的假设（Brooks, 1991）。

这些思想在 1998 至 2010 年代的哲学与认知科学中被持续讨论，但它们始终停留在**论证的层面**——一种对传统内在主义心智观的挑战，被许多传统派学者视为过度激进。

2022 至 2025 的工程变革，把这场论证悄悄地关上了。

一个 2025 年的 agent，本质上是一个联合体：**相对较小的核心模型 + 一组工具（search、code execution、file system、browser automation、MCP 连接的外部服务集合）+ 一段结构化记忆（向量数据库、knowledge graph、长期文件）+ 可能若干协同 agent**。要评估这个联合体的"智能"，评价对象必须从核心模型的参数量挪到整个联合体的协同能力。换掉一代核心模型，联合体继续工作；换掉一组工具，同一个核心模型能做的事情截然不同。**智能的承载单元已经从单个模型挪到了整套 agent 架构**。Clark 和 Chalmers 所论证的那种"延展心智"，在这里从一个哲学论证变成了工业默认配置。

这件事反过来也重新解释了人类智能本身。一个人的聪明程度，从来不只取决于他脑子里装了什么，同样取决于他身边的书架、他的联系人网络、他调用哪些工具在思考。过去我们把这些称作"外围配置"——是因为在人身上，核心（大脑）与外围（工具、笔记、关系）之间的界限相对稳定，外围不可替换性让我们倾向于把它视作背景。AI 让核心这一项变成了可替换模块之后，这条界限本身才显现出来——被看见的同时也被相对化了。

---

## 六、在代际之间稳定的结构

模型会继续迭代。今天最强的 frontier model 到明年就会变成中等水平。这一事实要求任何一篇讨论 tool use 的文章，如果希望其结论能活过几代模型，就必须把讨论对象从"某一代模型具体能做什么"那一层抬高，锁定那些在代际之间依然稳定的结构。

**第一，智能的计量单位不会再回到封闭系统**。即使未来某一代模型的参数规模与推理能力大到它在不借助任何外部工具时就能独立处理许多任务，产业界也不会回到只评估它"闭卷成绩"的状态。原因在于：2022 至 2025 的工程经验已经充分证明，"开卷 + 工具 + 多 agent 协同"的架构在同等核心能力下表现总是优于封闭架构——且该优势会随着任务复杂度的增加而扩大。这是一扇单向门，推开了以后就关不上。

**第二，衡量 AI 系统的关键指标，从静态能力挪到了动态编排**。一个系统的核心模型能力当然重要，但同等——有时更重要——的是它能调动多少工具、调用的准确性、在多长的任务序列里保持一致、在多少步之后仍能自我纠正。这些属性所刻画的是现实世界本身的结构——现实包含大量工具、任务需要长时间执行、错误会累积且需要被发现与修正——它们的重要性并不随某一代模型的更替而波动。只要现实世界的这些属性保持稳定，这些指标的分量就会跨越模型代际而延续。

**第三，agent 的设计经验开始独立于模型代际积累**。如何为 agent 设计良好的工具接口（tool ergonomics），如何管理它的上下文与记忆（context engineering），如何组织多 agent 之间的分工（orchestration patterns），如何做可观测性与回放（agent tracing），这些问题在 2025 年还相当年轻，但它们的答案在加速积累。每一代新模型出来后，这些经验大部分迁移得过去，只有小部分需要因模型能力变化而重调。这是一门正在诞生的新工程学科，它的半衰期长于任何一代具体模型。

**第四，关于人类认知的哲学视角也不会退回去**。一旦工程实践里承认了延展心智这种结构，把人脑视为一个单点封闭系统的旧图景就会显得陈旧。这一转变最终会渗透到更基础的层面——教育的目标（不再只是让学生"脑子里装东西"，而是训练学生编排外部认知资源的能力）、组织的设计（把"人 + 工具 + 信息流"当作一个整体系统来优化）、乃至"什么算一个人的能力"这类判断的基本架构。

---

## 结语：问题形状的改变

Turing 1950 年那篇论文的标题是一个问题——机器能不能思考？七十五年之后，问题的形状已经变了。"机器能不能思考"这个问法里预设了一个封闭的单点主体，而 2022 至 2025 真正被改写的，正是这个预设。

问题现在更接近这样一种形式：**一个会调用工具、会与其他 agent 协作、会把任务分解为几十步并在出错时自我纠偏的联合系统，它的行为与过去我们称之为"思考"的那种活动，在功能层面还有什么不可磨灭的区别？**

如果答案是没有区别，那么"思考"这件事从一开始就不曾是它过去被描述的那样——它在人身上发生的时候，也从来没有完全发生在颅骨之内。图灵当年设想中的那间房间，从来都不是一个真正封闭的空间。只是我们过去没有工程手段把墙拆掉，因此就把它当作认识论上的边界了而已。

Clark 和 Chalmers 1998 年写下 *The Extended Mind* 时，他们面对的是一个哲学命题。二十七年之后，这个命题已经被工程化、产品化、行业标准化。在这个意义上，tool use 这个技术词条背后真正发生的事，比它表面的工程色彩要深得多——它不只是 AI 能力的一次扩张，它同时是人类关于"智能"这个词所使用的图景的一次结构性重构。

---

## 参考文献

### 哲学与认知科学

- Adams, F., & Aizawa, K. (2008). *The Bounds of Cognition*. Wiley-Blackwell. ISBN: 978-1405157858.
- Brooks, R. A. (1991). Intelligence without representation. *Artificial Intelligence*, 47(1–3), 139–159. DOI: https://doi.org/10.1016/0004-3702(91)90053-M
- Clark, A. (2003). *Natural-Born Cyborgs: Minds, Technologies, and the Future of Human Intelligence*. Oxford University Press. ISBN: 978-0195177510.
- Clark, A. (2008). *Supersizing the Mind: Embodiment, Action, and Cognitive Extension*. Oxford University Press. ISBN: 978-0195333213.
- Clark, A., & Chalmers, D. (1998). The extended mind. *Analysis*, 58(1), 7–19. DOI: https://doi.org/10.1093/analys/58.1.7 ｜ JSTOR: http://www.jstor.org/stable/3328150
- Hutchins, E. (1995). *Cognition in the Wild*. MIT Press. ISBN: 978-0262581462.
- Newell, A., & Simon, H. A. (1976). Computer science as empirical inquiry: Symbols and search. *Communications of the ACM*, 19(3), 113–126. DOI: https://doi.org/10.1145/360018.360022
- Norman, D. A. (1993). *Things That Make Us Smart: Defending Human Attributes in the Age of the Machine*. Addison-Wesley / Basic Books. ISBN: 978-0201626957.
- Turing, A. M. (1950). Computing machinery and intelligence. *Mind*, LIX(236), 433–460. DOI: https://doi.org/10.1093/mind/LIX.236.433 ｜ OUP: https://academic.oup.com/mind/article/LIX/236/433/986238
- Weizenbaum, J. (1966). ELIZA — A computer program for the study of natural language communication between man and machine. *Communications of the ACM*, 9(1), 36–45. DOI: https://doi.org/10.1145/365153.365168

### 语言模型与 scaling

- Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., et al. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, 33. arXiv:2005.14165. https://arxiv.org/abs/2005.14165
- Hoffmann, J., Borgeaud, S., Mensch, A., Buchatskaya, E., Cai, T., Rutherford, E., et al. (2022). Training compute-optimal large language models (Chinchilla). arXiv:2203.15556. https://arxiv.org/abs/2203.15556
- Kaplan, J., McCandlish, S., Henighan, T., Brown, T. B., Chess, B., Child, R., et al. (2020). Scaling laws for neural language models. arXiv:2001.08361. https://arxiv.org/abs/2001.08361
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *NeurIPS 2022*. arXiv:2201.11903. https://arxiv.org/abs/2201.11903

### Tool use 与 Agent 论文

- Nakano, R., Hilton, J., Balaji, S., Wu, J., Ouyang, L., Kim, C., et al. (2021). WebGPT: Browser-assisted question-answering with human feedback. arXiv:2112.09332. https://arxiv.org/abs/2112.09332
- Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T. (2023). Toolformer: Language models can teach themselves to use tools. arXiv:2302.04761. https://arxiv.org/abs/2302.04761
- Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y. (2022). ReAct: Synergizing reasoning and acting in language models. *ICLR 2023*. arXiv:2210.03629. https://arxiv.org/abs/2210.03629

### 评测基准

- Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., et al. (2021). Training verifiers to solve math word problems (GSM8K). arXiv:2110.14168. https://arxiv.org/abs/2110.14168
- Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2021). Measuring massive multitask language understanding (MMLU). *ICLR 2021*. arXiv:2009.03300. https://arxiv.org/abs/2009.03300
- Jimenez, C., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. (2023). SWE-bench: Can language models resolve real-world GitHub issues? arXiv:2310.06770. https://arxiv.org/abs/2310.06770
- Miserendino, S., Wang, M., Patwardhan, T., & Heidecke, J. (2025). SWE-Lancer: Can frontier LLMs earn \$1 million from real-world freelance software engineering? arXiv:2502.12115. https://arxiv.org/abs/2502.12115 ｜ OpenAI 公告：https://openai.com/index/swe-lancer/
- SWE-bench Leaderboard. (持续更新). https://www.swebench.com
- Yao, S., Shinn, N., Razavi, P., & Narasimhan, K. (2024). τ-bench: A benchmark for tool-agent-user interaction in real-world domains. arXiv:2406.12045. https://arxiv.org/abs/2406.12045 ｜ Sierra Research 介绍：https://sierra.ai/blog/benchmarking-ai-agents
- Zan, D., Huang, Z., Liu, A., Lin, H., Liu, Y., Chen, B., et al. (2025). SWE-bench-Live: Towards contamination-free evaluation of large language models on real-world software engineering tasks. arXiv:2505.23419. https://arxiv.org/abs/2505.23419
- Zhou, S., Xu, F. F., Zhu, H., Zhou, X., Lo, R., Sridhar, A., et al. (2023). WebArena: A realistic web environment for building autonomous agents. arXiv:2307.13854. https://arxiv.org/abs/2307.13854

### Anthropic 官方公告与工程文档

- Anthropic. (2024, October 22). Introducing computer use, a new Claude 3.5 Sonnet, and Claude 3.5 Haiku. https://www.anthropic.com/news/3-5-models-and-computer-use
- Anthropic. (2024, November 25). Introducing the Model Context Protocol. https://www.anthropic.com/news/model-context-protocol
- Anthropic (Schluntz, E., & Zhang, B.). (2024, December 19). Building effective agents. https://www.anthropic.com/research/building-effective-agents
- Anthropic. (2025, September 29). Introducing Claude Sonnet 4.5. https://www.anthropic.com/news/claude-sonnet-4-5
- Anthropic. (2025, September). Effective context engineering for AI agents. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Anthropic. (2025, October). Equipping agents for the real world with Agent Skills. https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
- Anthropic. (2025, November 24). Introducing Claude Opus 4.5. https://www.anthropic.com/news/claude-opus-4-5

### OpenAI 官方公告

- OpenAI. (2023, June 13). Function calling and other API updates. https://openai.com/index/function-calling-and-other-api-updates/
- OpenAI. (2025, February 18). Introducing the SWE-Lancer benchmark. https://openai.com/index/swe-lancer/

### 其他引用

- The New Stack. (2025, December 18). Why the Model Context Protocol won. https://thenewstack.io/why-the-model-context-protocol-won/
- Willison, S. (2023, June 13). OpenAI: Function calling and other API updates [评论：function calling 在技术上对应于 ReAct pattern]. https://simonwillison.net/2023/Jun/13/function-calling/
- Willison, S. (2024, December 20). Building effective agents [对 Anthropic 该文的评论]. https://simonwillison.net/2024/Dec/20/building-effective-agents/
