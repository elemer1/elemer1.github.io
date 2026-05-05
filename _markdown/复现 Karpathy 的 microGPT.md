---
title: "复现 Karpathy 的 microGPT"
permalink: /microgpt/
listed: true
---

> 在 Mac 上 1 分多钟，我把 Karpathy 写的一份"GPT 微缩模型"完整跑了一遍。整个程序 199 行 Python，没装任何东西，包括 ChatGPT 同款架构的全部核心。这篇博客把过程、结果、和我从中学到的东西讲清楚——目标读者不是工程师，是任何一个**每天用 ChatGPT 但不知道它内部到底在干什么的人**。

## 这篇文章想给你什么

如果你只有 30 秒，请记三件事：

1. **ChatGPT 不是黑盒，它的算法核心可以装进 199 行 Python**——比一份淘宝订单详情页的 HTML 还短。其余的部分（数据中心、几十亿参数、几十亿美元）都是把这 199 行**跑得更快**的工程包装，不是新的"智能"。
2. **它的"创造性"完全由一个整数决定**。我用种子 42 跑出 20 个杜撰的人名（kamon、karai、anton……），换台机器、再跑一次，结果一字不差。所谓"AI 灵感"在这一层只是被一颗骰子封印的伪随机过程。
3. **同一个程序换成"专业版"PyTorch 写法，速度快 165 倍但答案完全一样**——这就是 AI 工业化的全部秘密：算法没变，只是把同一件事做得更快。理解这句话，你就能读懂 90% 关于 AI 的新闻是怎么回事。

下面是过程、数据、和我为什么觉得花一下午做这个对**法学生、PM、投资人、医生**都值——不只是程序员。

## 一句话结论（给愿意多看 30 秒的人）

我跑出来的 20 个杜撰名字（`kamon, ann, karai, jaire, vialan, karia, yeran, anna, areli, kaina, konna, keylen, liole, alerin, earan, lenne, kana, lara, alela, anton`）和 Karpathy 博客里贴的样本**一字不差**。

这件事比想象中重要。**一个号称在"创造"内容的语言模型，它的全部"创造性"都被一个叫 seed 的整数完全决定**——同一颗 seed，全世界任何一台机器都会跑出完全一样的"胡言乱语"。当你读到"AI 写出了惊艳诗句"这种新闻时，记得这层底色：那个"惊艳"在算法层面和我这台 Mac 杜撰出 `kamon` 不是两件事，只是规模和包装不同。

## 我具体怎么做的：一步一步拆给你看

写技术博客最容易犯的错是跳过过程、只放结论。下面这一节我刻意做得啰嗦——把"打开终端 → 看到样本 → 验证一致性"的每一步都用截图和命令展示出来，让一个**从没写过 Python 的读者**也能跟着做。

### 第一步：打开终端，准备一个空文件夹

如果你没用过终端：在 Mac 上按 `⌘ + 空格`，输入 "Terminal"，回车。会弹出一个全黑的窗口——这就是命令行。下面这五行命令，复制粘贴一行回车一次：

![microGPT 完整 setup 流程](/assets/images/microgpt/setup_steps.png)

第一行 `mkdir` 是"在 Documents 里建一个叫 microgpt 的文件夹"；第二行 `curl` 是"从 Karpathy 的 GitHub 把那 199 行代码下载下来"；倒数第二行 `python3 microgpt.py` 是"把这段代码跑起来"。

**第一次跑会发生什么：** 程序会自己再下载一份 `names.txt`（32,033 个英文名字，228KB），然后开始训练——你会看到屏幕上一行 `step 1 / 1000 | loss 3.3660` 不断刷新，loss 数字在缓慢往下走。等到 `step 1000` 出现，紧跟着会打印 20 个杜撰的名字。整个过程在我这台 Mac 上是 **104.82 秒**。

### 第二步：看一眼模型在"读"什么

模型并不知道"emma 是个名字"。它看到的就是一串字符 + 一个特殊的"开头/结尾"标记。下面是它的训练数据：

![names.txt 数据集预览](/assets/images/microgpt/dataset_preview.png)

32,033 个名字，每个被一个特殊 token（`BOS` = "Beginning of Sequence"）包住。模型的全部任务是：**给定前面几个字符，预测下一个字符是什么**。你读到 `em-` 时大脑会预测下一个是 `m`，模型干的是同一件事——只不过它要从零开始，把这种预测能力从随机权重一步一步训练出来。

### 第三步：观察 loss 数字怎么从 3.3 降到 2.6

训练日志的精华版本：

![训练过程关键节点](/assets/images/microgpt/training_progression.png)

每一行都对应一个学习里程碑：
- step 1：模型完全没学到东西，loss 等于"随便乱猜 27 个字符之一"的理论值
- step 50：模型已经知道 `a / e / n` 比 `q / x / z` 常见——光这一条就让 loss 下来一大截
- step 250：模型开始知道"名字开头多用辅音、结尾多用元音"
- step 1000：训练结束，模型进入推理模式，开始"杜撰名字"

### 第四步：保留所有过程文件——这是博客可信度的物理基础

跑完后我的工作目录长这样（包含所有后续实验产物）：

![复现工作目录的完整文件树](/assets/images/microgpt/file_tree.png)

每一个 `.log`、`.csv`、`.json` 都是真实跑出来的中间状态——不是事后伪造的。任何看这篇博客的读者，只要用同样的命令 + 同样的 Python 版本，应当得到**几乎完全相同**的文件清单（除了时间戳）。这种"**所有数字都可被你自己验证**"的属性，是这篇博客和"二手转述教程"最关键的区别。

### 我具体跑出来的硬数字

| 项目 | 数值 |
|---|---|
| 训练数据集 | `names.txt`，32,033 个名字，~228 KB |
| 词表大小 | 27（26 个英文小写字母 + 1 个 BOS 特殊 token） |
| 参数数量 | **4,192** |
| 网络结构 | 1 层 Transformer，n_embd=16，4 头，block_size=16 |
| 训练步数 | 1,000 |
| 优化器 | Adam（手写实现，没有调用 PyTorch） |
| 训练耗时（real） | **104.82 秒** |
| 推理温度 | 0.5 |
| 设备 | MacBook，Apple Silicon，arm64，macOS 26.4.1，Python 3.10.13 |
| 全部依赖 | **只有 Python 3 标准库**：os / math / random / urllib——零 pip install |

Karpathy 在 M 系列 Macbook 上是约 60 秒，我这台耗时 105 秒——慢一些是合理的（不同 M 芯片、Python 解释器版本、后台进程都会影响）。重要的是它**确实在 Mac 上 1-2 分钟跑完**——这一点不是营销话术，是我刚才在你眼前一行一行执行下来的事实。

## 二度验证：同机器、不同 session、字节一致

为了确认上面那个"字节级可复现"的论断不是幸运巧合，我在同一台机器上、当天晚些时候、在一个完全独立的 shell session 里又跑了一遍 `microgpt.py`。两次的样本对比：

```
$ diff <(grep ^sample run_baseline.log) <(grep ^sample run_session2.log)
(empty — byte-identical)
```

20 个样本一字不差。两次的 wall clock 不同（104.82s vs 99.97s——CPU 调度、后台负载会影响计时），但**模型权重的演化路径、最后一步推理的 RNG 状态、到生成的字符串都完全可重放**。这是 `random.seed(42)` 一个种子封印整条计算链的结果——从 `random.shuffle(docs)`（决定训练样本顺序）到 `random.gauss(0, 0.08)`（决定参数初始化）再到 `random.choices`（决定推理采样），全部都从那一颗 seed 派生。

这个性质在 LLM 的产业讨论里基本被淹没了——生产模型不是确定性的（不同的 batch 调度、GPU 内核、混合精度都会引入不可重放的浮点漂移）。但**算法本身是确定性的**——只是 efficiency 那一侧塞进了大量"非确定性副产品"。这又是一个 Karpathy "其余皆 efficiency" 的微观例证：你失去的可复现性，是为了换吞吐量而支付的代价。

## 把 199 行核心代码完整贴出来——这是这篇博客的"物证"

到目前为止我都在描述这段代码做了什么。但**这篇博客最重要的东西，是这段代码本身**——不是我的描述，不是图表，不是分析。如果你只能从这篇博客带走一样东西，应该是下面这 199 行。

为什么这段代码这么重要？

**第一，它是 GPT 算法被压到的最低密度。** 类似的 GPT 实现在它之前已经有过——Karpathy 自己的 nanoGPT（约 600 行）、minGPT（约 300 行）、TinyStories 一类的教学项目。但 microGPT 第一次做到了**把 tokenizer、autograd、Transformer、Adam、训练循环、推理循环全部塞进 199 行 Python 标准库**——零 NumPy、零 PyTorch、零 GPU。这不是简化，是**密度的极限**。再砍下去，你必须开始牺牲算法完整性（比如去掉 attention，或不写 backward）。

**第二，它把"GPT 是什么"这个问题变成了一个可验证的、不需要诉诸权威的物证。** 在它出现之前，"ChatGPT 内部到底是什么"这个问题，只能通过读论文、看 demo、相信权威专家来获得答案。在它出现之后，**任何识字的人都可以用 5 分钟读完这 199 行**，并验证：是的，这就是它的全部。这种"不可被遮蔽的物证"在 AI 监管、AI 伦理、AI 哲学的讨论中是稀缺品。

**第三，它把"创造性"和"统计规律"之间的界线做成了肉眼可见的代码行。** 你向下翻，会看到第 30-72 行是 `Value` 类（autograd），第 108-144 行是 `gpt(...)` 函数（Transformer 架构），第 153-184 行是训练循环（Adam）。这些不是隐喻，不是黑箱，是**字面上的若干行 Python**。它们加起来等于 ChatGPT。

下面是完整的代码，逐字粘贴自 Karpathy 的 [gist](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95)，没有改一个字符。我把它分成 6 段，每段前面给一句话解释；这样即使你不写代码，也能跟着读出"这段在做什么"。

### 段 1（第 1-12 行）：完全没有依赖

```python
"""
The most atomic way to train and run inference for a GPT in pure, dependency-free Python.
This file is the complete algorithm.
Everything else is just efficiency.

@karpathy
"""

import os       # os.path.exists
import math     # math.log, math.exp
import random   # random.seed, random.choices, random.gauss, random.shuffle
random.seed(42) # Let there be order among chaos
```

这十二行是 microGPT 的"全部进口商品"——`os` 用来检查文件、`math` 用来算对数指数、`random` 用来生成伪随机数。`random.seed(42)` 是把所有随机性钉死的那一颗钉子。

### 段 2（第 14-27 行）：把字符变成数字（"tokenizer"）

```python
# Let there be a Dataset `docs`: list[str] of documents (e.g. a list of names)
if not os.path.exists('input.txt'):
    import urllib.request
    names_url = 'https://raw.githubusercontent.com/karpathy/makemore/988aa59/names.txt'
    urllib.request.urlretrieve(names_url, 'input.txt')
docs = [line.strip() for line in open('input.txt') if line.strip()]
random.shuffle(docs)
print(f"num docs: {len(docs)}")

# Let there be a Tokenizer to translate strings to sequences of integers ("tokens") and back
uchars = sorted(set(''.join(docs))) # unique characters in the dataset become token ids 0..n-1
BOS = len(uchars) # token id for a special Beginning of Sequence (BOS) token
vocab_size = len(uchars) + 1 # total number of unique tokens, +1 is for BOS
print(f"vocab size: {vocab_size}")
```

这是 tokenizer——把字符串 `"emma"` 变成 `[BOS, e, m, m, a, BOS]` 这样的整数序列。生产 LLM 用 BPE（字节对编码），词表数万；microGPT 用最朴素的字符级，词表 27（26 字母 + 1 个 BOS）。算法上**完全等价**，只是粒度和 efficiency 不同。

### 段 3（第 29-72 行）：Autograd——这是手写微积分

```python
# Let there be Autograd to recursively apply the chain rule through a computation graph
class Value:
    __slots__ = ('data', 'grad', '_children', '_local_grads')

    def __init__(self, data, children=(), local_grads=()):
        self.data = data                # scalar value of this node calculated during forward pass
        self.grad = 0                   # derivative of the loss w.r.t. this node, calculated in backward pass
        self._children = children       # children of this node in the computation graph
        self._local_grads = local_grads # local derivative of this node w.r.t. its children

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data + other.data, (self, other), (1, 1))

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        return Value(self.data * other.data, (self, other), (other.data, self.data))

    def __pow__(self, other): return Value(self.data**other, (self,), (other * self.data**(other-1),))
    def log(self): return Value(math.log(self.data), (self,), (1/self.data,))
    def exp(self): return Value(math.exp(self.data), (self,), (math.exp(self.data),))
    def relu(self): return Value(max(0, self.data), (self,), (float(self.data > 0),))
    def __neg__(self): return self * -1
    def __radd__(self, other): return self + other
    def __sub__(self, other): return self + (-other)
    def __rsub__(self, other): return other + (-self)
    def __rmul__(self, other): return self * other
    def __truediv__(self, other): return self * other**-1
    def __rtruediv__(self, other): return other * self**-1

    def backward(self):
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._children:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            for child, local_grad in zip(v._children, v._local_grads):
                child.grad += local_grad * v.grad
```

这 44 行是整个 microGPT 最容易被低估的部分。它是**自动求导引擎**——把高中微积分的链式法则用一个 Python 类实现出来。每一次 `a + b`、`a * b`、`a.log()` 不只算出数值，还把"这个数对它的两个父节点的导数"记下来，最后通过 `backward()` 把整棵计算图反向遍历，把所有梯度算出来。

PyTorch 的 `torch.Tensor` 在做完全相同的事情，但 PyTorch 有 200 万行 C++ + CUDA。这 44 行 Python 在算法上**和它等价**——只是慢了几个数量级。

### 段 4（第 74-90 行）：参数初始化

```python
# Initialize the parameters, to store the knowledge of the model
n_layer = 1     # depth of the transformer neural network (number of layers)
n_embd = 16     # width of the network (embedding dimension)
block_size = 16 # maximum context length of the attention window (note: the longest name is 15 characters)
n_head = 4      # number of attention heads
head_dim = n_embd // n_head # derived dimension of each head
matrix = lambda nout, nin, std=0.08: [[Value(random.gauss(0, std)) for _ in range(nin)] for _ in range(nout)]
state_dict = {'wte': matrix(vocab_size, n_embd), 'wpe': matrix(block_size, n_embd), 'lm_head': matrix(vocab_size, n_embd)}
for i in range(n_layer):
    state_dict[f'layer{i}.attn_wq'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wk'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wv'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.attn_wo'] = matrix(n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc1'] = matrix(4 * n_embd, n_embd)
    state_dict[f'layer{i}.mlp_fc2'] = matrix(n_embd, 4 * n_embd)
params = [p for mat in state_dict.values() for row in mat for p in row] # flatten params into a single list[Value]
print(f"num params: {len(params)}")
```

这是模型的"全部知识"——4192 个 `Value` 节点，初始化为方差 0.08 的高斯随机数。GPT-4 估计有 1.6 万亿个这样的参数。**结构完全一样，只是数量差了 4 亿倍。**

### 段 5（第 92-144 行）：Transformer 前向传播

```python
# Define the model architecture: a function mapping tokens and parameters to logits over what comes next
# Follow GPT-2, blessed among the GPTs, with minor differences: layernorm -> rmsnorm, no biases, GeLU -> ReLU
def linear(x, w):
    return [sum(wi * xi for wi, xi in zip(wo, x)) for wo in w]

def softmax(logits):
    max_val = max(val.data for val in logits)
    exps = [(val - max_val).exp() for val in logits]
    total = sum(exps)
    return [e / total for e in exps]

def rmsnorm(x):
    ms = sum(xi * xi for xi in x) / len(x)
    scale = (ms + 1e-5) ** -0.5
    return [xi * scale for xi in x]

def gpt(token_id, pos_id, keys, values):
    tok_emb = state_dict['wte'][token_id] # token embedding
    pos_emb = state_dict['wpe'][pos_id] # position embedding
    x = [t + p for t, p in zip(tok_emb, pos_emb)] # joint token and position embedding
    x = rmsnorm(x) # note: not redundant due to backward pass via the residual connection

    for li in range(n_layer):
        # 1) Multi-head Attention block
        x_residual = x
        x = rmsnorm(x)
        q = linear(x, state_dict[f'layer{li}.attn_wq'])
        k = linear(x, state_dict[f'layer{li}.attn_wk'])
        v = linear(x, state_dict[f'layer{li}.attn_wv'])
        keys[li].append(k)
        values[li].append(v)
        x_attn = []
        for h in range(n_head):
            hs = h * head_dim
            q_h = q[hs:hs+head_dim]
            k_h = [ki[hs:hs+head_dim] for ki in keys[li]]
            v_h = [vi[hs:hs+head_dim] for vi in values[li]]
            attn_logits = [sum(q_h[j] * k_h[t][j] for j in range(head_dim)) / head_dim**0.5 for t in range(len(k_h))]
            attn_weights = softmax(attn_logits)
            head_out = [sum(attn_weights[t] * v_h[t][j] for t in range(len(v_h))) for j in range(head_dim)]
            x_attn.extend(head_out)
        x = linear(x_attn, state_dict[f'layer{li}.attn_wo'])
        x = [a + b for a, b in zip(x, x_residual)]
        # 2) MLP block
        x_residual = x
        x = rmsnorm(x)
        x = linear(x, state_dict[f'layer{li}.mlp_fc1'])
        x = [xi.relu() for xi in x]
        x = linear(x, state_dict[f'layer{li}.mlp_fc2'])
        x = [a + b for a, b in zip(x, x_residual)]

    logits = linear(x, state_dict['lm_head'])
    return logits
```

这是 ChatGPT 的核心——**Transformer 架构**——的最简化实现。`gpt(...)` 函数读入一个 token id 和位置，把 token 转成嵌入向量，依次经过：(1) RMSNorm 归一化 → (2) 多头注意力 (Q/K/V 投影 + softmax 加权) → (3) 残差连接 → (4) MLP (两层全连接 + ReLU) → (5) 残差连接 → (6) lm_head 投影到 vocab。最终输出 27 个 logits，对应"下一个字符是 a/b/c/...的相对置信度"。

GPT-2、GPT-3、GPT-4、Claude、Llama 全都是**这个结构 + 更多层 + 更多维**。你正在读的 53 行就是它们的算法骨架。

### 段 6（第 146-184 行）：训练循环

```python
# Let there be Adam, the blessed optimizer and its buffers
learning_rate, beta1, beta2, eps_adam = 0.01, 0.85, 0.99, 1e-8
m = [0.0] * len(params) # first moment buffer
v = [0.0] * len(params) # second moment buffer

# Repeat in sequence
num_steps = 1000 # number of training steps
for step in range(num_steps):

    # Take single document, tokenize it, surround it with BOS special token on both sides
    doc = docs[step % len(docs)]
    tokens = [BOS] + [uchars.index(ch) for ch in doc] + [BOS]
    n = min(block_size, len(tokens) - 1)

    # Forward the token sequence through the model, building up the computation graph all the way to the loss
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    losses = []
    for pos_id in range(n):
        token_id, target_id = tokens[pos_id], tokens[pos_id + 1]
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax(logits)
        loss_t = -probs[target_id].log()
        losses.append(loss_t)
    loss = (1 / n) * sum(losses) # final average loss over the document sequence. May yours be low.

    # Backward the loss, calculating the gradients with respect to all model parameters
    loss.backward()

    # Adam optimizer update: update the model parameters based on the corresponding gradients
    lr_t = learning_rate * (1 - step / num_steps) # linear learning rate decay
    for i, p in enumerate(params):
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        m_hat = m[i] / (1 - beta1 ** (step + 1))
        v_hat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps_adam)
        p.grad = 0

    print(f"step {step+1:4d} / {num_steps:4d} | loss {loss.data:.4f}", end='\r')
```

训练循环。每一步：取一个名字 → 喂进模型算出 logits → 用交叉熵算 loss → 反向传播算梯度 → Adam 更新所有 4192 个参数。**1000 步**之后训练结束。这就是 ChatGPT 训练的算法模板——OpenAI 的版本只是把这循环跑了几百万次、在几万亿 token 上、用上万张 GPU。

### 段 7（第 186-200 行）：推理生成

```python
# Inference: may the model babble back to us
temperature = 0.5 # in (0, 1], control the "creativity" of generated text, low to high
print("\n--- inference (new, hallucinated names) ---")
for sample_idx in range(20):
    keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
    token_id = BOS
    sample = []
    for pos_id in range(block_size):
        logits = gpt(token_id, pos_id, keys, values)
        probs = softmax([l / temperature for l in logits])
        token_id = random.choices(range(vocab_size), weights=[p.data for p in probs])[0]
        if token_id == BOS:
            break
        sample.append(uchars[token_id])
    print(f"sample {sample_idx+1:2d}: {''.join(sample)}")
```

推理。从 BOS 开始，每一步：跑一次模型 → 拿到 27 个字符的概率分布 → 用 `random.choices` 抽一个 → 如果抽到 BOS 就停下，否则把这个字符加到结果里、继续生成下一个。**这就是 ChatGPT 给你回复时它在做的事——一个 token 一个 token 地按概率分布抽样**，唯一区别是它的 vocab 是 5 万词不是 27 字符、它有 1.6 万亿参数不是 4192 个。

---

把这 7 段加起来就是完整的 199 行。**你刚刚读完了 ChatGPT 的算法核心。** 整个 LLM 产业、所有"AGI 焦虑"、几千亿美元估值的资本叙事，技术底座就是上面这些代码。其余的——RLHF、混合专家、推理优化、成千上万张 GPU——都是把这个底座**跑得更快、跑得更大**，没有改变底座本身。

这就是为什么我说："如果你只能从这篇博客带走一样东西，应该是这 199 行。"

## Loss 曲线读出来了什么

把 1000 步的 loss 全部画下来，叠加 50 步滚动平均：

![microGPT loss 曲线](/assets/images/microgpt/loss_curve.png)

读这张图有几个关键观察。

**起点 ≈ log(27) ≈ 3.30**。这就是"对 27 个 token 完全均匀随机猜"的理论交叉熵。模型在 step 1 的 loss 是 3.366，几乎踩在这条线上——这说明初始化（高斯分布，标准差 0.08）的输出确实接近均匀分布，没有先验偏向。

**前 50 步快速下降到 ≈2.85**。模型在最初几十步就学到了一个最廉价的统计规律：英文名字的字母分布**不是**均匀的。`a, e, n, i, l` 频次远高于 `q, x, z`。仅仅这一个 unigram 先验就把 loss 干掉了 0.4-0.5。

**之后 950 步缓慢从 2.85 降到 2.32**。这部分是 bigram、trigram、位置先验（名字开头偏爱辅音、结尾偏爱元音）等等的累积。下降速度明显慢，因为这些规律本身的统计强度就更弱、互相干扰更多。

**单步 loss 始终在 1.5-3.5 之间剧烈震荡**。这是因为 microGPT **每步只看一个文档**（一个名字），没有 batch。一个短而常见的名字（`anna`）loss 会很低，一个奇异名字（`xqzvkl`）loss 会很高。如果它实现了 batch，曲线会平滑得多。这也是 Karpathy 那句"其余皆 efficiency"的一个微观例证——batch 是**优化器收敛速度**意义上的 efficiency，但和**算法是否正确**无关。

## 温度扫描——这是我加的实验

Karpathy 默认的 temperature=0.5 是一个温和值。我把训练保持完全一致，最后做推理时把温度扫过 [0.1, 0.5, 1.0, 1.5, 2.0]，每个温度下用同一个采样种子（999）生成 20 个样本，让"唯一变量"就是温度。

![温度扫描 20×5 网格](/assets/images/microgpt/temp_sweep.png)

灰色 = 重复样本，红色 = 出现 ≥4 个连续辅音的"乱码倾向"输出。

| T | 平均长度 | 唯一样本数 | 形态 |
|---|---|---|---|
| 0.1 | 4.35 | **7 / 20** | 模式坍塌：13 次都是 `anan` / `anah` / `anari` 的变体 |
| 0.5 | 5.05 | 20 / 20 | 像名字：mariel、bora、alina、zarah |
| 1.0 | 5.55 | 20 / 20 | 仍可读，开始野：ravila、kumisa、kaisensh |
| 1.5 | 5.95 | 20 / 20 | 开始崩：sawkicuk、knrarl、tmzlear |
| 2.0 | 6.30 | 20 / 20 | 大量乱码：saxnnbyly、blctima、hurrawupomy |

这张图是我向**非技术朋友**解释 hallucination 的最佳教具——用一万字也讲不清"温度"对模型意味着什么，但看一眼这张图就明白了：

- **低温把概率分布锐化**——模型更倾向于走"最可能"的路，所以反复输出同一个高频模式（这里是 `an…` 开头的短词）。
- **高温把概率分布平滑化**——所有 token 都有机会被采到，模型走入训练数据从未支持过的字符组合，于是产生连续辅音、孤立字母、超长字符串。
- **温度 0.5 到 1.0 之间是甜区**——既有多样性又保持可读。生产 LLM 的默认温度通常也在 0.6-1.0 之间，不是巧合。

更重要的是：**模型本身没变，参数完全一样**——所有这些差异都来自最后一行 `softmax(logits / T)` 里的 `T`。这给了一个直觉：当 ChatGPT 输出错误信息时，它不是"信念坚定地错了"，它是在做一个加权随机抽样，而工程师可以通过改一个浮点数让它变得更稳重或更狂野。

## 缩放——把模型变宽、变深，看看会怎样

温度扫描是固定模型动推理。下一个自然的实验是**反过来**：固定推理设置，动模型本身的容量。我跑了四组配置，每组都是 500 步训练（保持时间可比），seed=42 全程一致：

![microGPT 四档容量的训练曲线 + 容量 - 损失散点](/assets/images/microgpt/scaling.png)

| n_embd | n_layer | 参数数 | 训练耗时（500 步） | 末段平均 loss | 5 个样本（T=0.5, sample_seed=999） |
|---|---|---|---|---|---|
| 8 | 1 | 1,328 | 12.05s | 2.4583 | mariie, cara, alene, yanaen, japa |
| 16 | 1（baseline） | **4,192** | 51.31s | 2.4202 | marile, bria, aleni, waraen, jara |
| 16 | 2（更深） | 7,264 | 125.39s | 2.4183 | mashen, brla, amane, wanaen, jara |
| 32 | 1（更宽） | 14,528 | 261.5s | 2.4416 | maslia, cera, amani, yanade, jara |

**第一眼期待**：参数从 1,328 涨到 14,528（约 11×），loss 应该明显下降——这是教科书 scaling laws 的承诺。

**第二眼现实**：四档的末段 loss 全部挤在 2.42-2.46 之间，最大差距只有 0.04 nats（约 4% 概率）。更尴尬的是，**最宽的 (n_embd=32, n_layer=1) 反而比 baseline 略差**（2.4416 vs 2.4202）。

但同一行表的训练耗时——12s → 51s → 125s → 262s——是几乎严格的幂律放大。

为什么 loss 没跟上？因为**我们在 500 步的预算里，根本没把更大的模型训练充分**。更宽/更深的网络初始 loss 更高（更多随机参数要"摆正"），需要的步数更多才能追上 baseline，而 500 步对 14,528 个参数来说远远不够。这就是 [Chinchilla 论文](https://arxiv.org/abs/2203.15556)那个核心经验事实在玩具尺度上的微缩复现——**给定计算预算，参数量和训练 token 数有一个最优比**，盲目堆参数不堆 token 反而是浪费。

这个"反期待"结果其实比"loss 顺滑下降"更有教学价值。如果我把这张表给一个法学院/政策圈的朋友看，最直接的论断是：**"算力 = 智能"是一个被严重过度简化的等式。**算力可以被花在更宽的模型上，也可以被花在更多的 token 上——后者对最终 loss 的边际贡献往往更大，但前者更容易讲故事（可以宣布"参数量翻倍"）。这种区分在你阅读"国家 AI 战略"、"算力出口管制"、"训练数据合规"的政策辩论时，会变成一个能切开宣传口径的具体工具。

## 用 PyTorch 重写一遍：同算法、不同 efficiency

到这里，所有的实验都还在 199 行 scalar Python 范畴里。下一步是 Karpathy 那句话最硬的实证测试——**把 `Value` 类换成 `torch.tensor`，把每个 token 单走的 forward 换成一次张量化前向 + causal mask，其他一切照搬。如果这真的只是 efficiency，loss 序列应当数值等价、最终样本应当一致；只有 wall clock 应该塌缩。**

我写了 `microgpt_torch.py`（约 130 行），关键约束有三条：

- **参数初始化必须用 Python 的 `random.gauss`**，不能用 `torch.randn`——两者的 RNG 不同，`torch.randn` 即便相同 seed 也给出不同数值。我把 scalar 抽出来再 `torch.tensor(...)` 包装，确保 4192 个参数和 scalar 版逐位一致。
- **CPU + `float64` + 单线程 BLAS**。MPS 用不同 kernel 会引入浮点漂移；`float32` 的精度不够；多线程让 BLAS 累加顺序不稳定。这三条加起来才能让一致性测试可解读。
- **Adam 公式逐字照搬 microgpt.py**——同样的 `(beta1, beta2, eps)`、同样的 bias correction、同样按参数顺序更新。

跑出来的结果：

| 指标 | scalar (`microgpt.py`) | torch (`microgpt_torch.py`) |
|---|---|---|
| 训练 wall clock | **121.94s**（高精度版本） | **0.74s** |
| 加速比 | — | **~165×** |
| 末步 loss | 2.6496944697… | 2.6496944699… |
| loss 最大单步差 | — | **4.98 × 10⁻¹¹** |
| loss 平均单步差 | — | 2.55 × 10⁻¹¹ |
| 1000 步 \|diff\| < 10⁻¹⁰ | — | **1000 / 1000** |
| 最终 20 个推理样本 | kamon, ann, … anton | kamon, ann, … anton（**byte-identical**） |

![scalar vs torch loss 曲线 + 单步差](/assets/images/microgpt/torch_compare.png)

上图：两条 loss 曲线（红 = scalar、蓝虚 = torch）在视觉上完全重合。下图：每步绝对差的 log-scale 散点——全部夹在 10⁻¹¹ 量级。

这 4.98 × 10⁻¹¹ 不是 0，但**它正是 BLAS 重排累加顺序应该产生的浮点误差量级**——scalar 版用 Python 的 `sum(qh[j]*kh[t][j] for j in range(head_dim))` 严格按 j=0,1,2,3 累加；torch 的 matmul 用 SIMD 累加，顺序不同。`a + b + c ≠ a + (b + c)` 在 float64 下是 1 ulp 级别的差异，乘以 1000 步迭代和 4192 个参数的反向传播链路，最终 loss 漂移到 10⁻¹¹ 量级——完全在预期内。

但**算法上没有任何区别**。20 个生成样本一字不差就是这个事实最直接的证据：loss 序列差异小到不足以让 `random.choices` 在任何一步选不同的 token，整条采样轨迹完全可重放。

**165 倍这个数字到底意味着什么？用大白话讲：**

想象你要从北京去上海。
- **scalar 版**像走路过去。
- **PyTorch 版**像坐高铁。

两人都到达上海，看到的还是同一个外滩，吃的还是同一碗小笼包——**目的地完全一样**。但一个走了 122 秒，一个跑了 0.74 秒。

这就是 Karpathy 那句话的全部含义：**算法（去哪里）从没变。变的只是 efficiency（怎么去）。**

把这个比喻拉长——

- 我这次的高铁，是从"走路"换到了"普通高铁"（CPU 上单线程跑 PyTorch）。
- 真正的工业级 ChatGPT 已经在坐"超音速磁悬浮 + 跨海隧道"：GPU、混合精度、FlashAttention、批处理、vLLM……
- 从我这台 Mac 上的 0.74 秒，到 OpenAI 训练 GPT-4 的实际吞吐，**估计还差 5 到 7 个数量级**——但**目的地仍然是同一个外滩**。

这条认识有一个非常实用的用法：**读到任何"AI 重大突破"的新闻时，先问一个问题——这是真的去了一个新城市，还是只是把去同一个城市的速度又翻了一倍？**

90% 的报道答案是后者。但"我们把高铁速度又翻了一倍"卖不动头条、估不上估值，所以新闻稿会包装成"AI 学会了新的能力"。当你读过 199 行算法核心、亲眼见过同一份算法换实现快 165 倍之后，这层包装很难再骗到你。

这是这次实验**对一个非工程师最具体、最持久的回报**——一个能在新闻消费、投资判断、政策辩论里直接用的过滤器。

## 把它接进我自己的工作里：Compound 长寿主题"声音指纹"生成器

> **如果你只读一段就要离开**：我用 Karpathy 那 199 行 GPT 算法，加上 4 份公开的长寿/健康内容数据（PubMed 论文标题、健康播客、生物黑客 Reddit、百岁研究摘要），在我这台 MacBook 上 **4 分钟**训出 4 个**专属于 Compound 内容场景的微型 AI**。每个 AI 学会模仿一种"长寿声音"——学术的、播客的、社区口语的、严肃论文的。它们一晚上能产出 1,200 个全新的内容选题种子（**96-100% 在训练数据里完全不存在**），单次 marginal cost ≈ $0.02 的 Mac 电费。这不是一个 demo，是一个**已经在工作的内部工具的 v0.1**。

### 这一节给三类读者各读什么

这一节比前面长，因为它要同时讲给三类人听：

- **股东 / 投资人**：跳到 ⓪「这件事在商业上怎么算账」和 ❺「商业化路径的三档可能」。中间技术细节可以略读。
- **CEO / 创意主理人 / 内容总监**：核心读 ❷「四种声音的差异」和 ❸「内容生产工作流的四个具体用法」——这些直接对应你的日常决策。
- **CTO / 工程师**：全篇可读。重点在 ❶ 工作流和 ❹ 限制 / 风险评估。

### ⓪ 这件事在商业上怎么算账（给股东的 6 个数字）

| 维度 | 数字 | 这意味着什么 |
|---|---|---|
| **总开发时间** | 1 个下午（约 4 小时人时） | 不是研究项目，是一个工程师一次冲刺产出的东西 |
| **总训练成本** | 234 秒 CPU 时间 ≈ **$0.02 电费** | 重训一遍跟刷牙差不多便宜——每周可以无脑重训 |
| **数据获取成本** | $0（全部公开 API） | 没有数据采购合同、没有授权风险、没有数据供应商锁定 |
| **运行依赖** | 一台 MacBook（无 GPU、无云、无订阅） | 不依赖 OpenAI 涨价、不依赖 GPU 配额、断网也能用 |
| **每周产出** | 1,200 个新内容选题种子（4 模型 × 300 样本） | 假设每个内容主理人每周需要 5 个选题——一份产出可服务 240 个内容主理人 |
| **新颖度审计** | 96.7% / 100% / 98.3% / 100% 真新颖 | 法务可量化的"非记忆 / 非改写"证据，对处于 IP 灰色地带的健康内容平台是合规护栏 |

**翻译成投资人语言**：这是一个**从 0 到内部生产工具的 4 小时实验**，单位 marginal cost 可忽略，**所有产出都自带版权护城河（96%+ 真新颖）**，且**完全不依赖任何外部 AI 服务商**。换言之——它是 Compound 内容能力栈里**一个不能被 OpenAI 涨价、Anthropic 限流、或国家监管断网影响**的护栏式底层模块。

它不会替代 GPT-4 写正文（那是它的极限之外），但它替代了**"想选题"这个高频低成本环节**对外部 AI 的依赖。

---

### ❶ 工作流：4 分钟训出 4 个"微型 ChatGPT"（CTO 视角）

我做了四个并行的语料采集 + 训练 pipeline：

| 语料 | 来源 | 体量 | 它代表什么"声音" |
|---|---|---|---|
| **PubMed 论文标题** | NCBI E-utilities 公开 API | 1,579 条 | 学术 / 严谨 / 机制术语 ("autophagy / mitochondria / lifespan") |
| **健康播客 episode** | Huberman Lab + Peter Attia + FoundMyFitness 的 RSS | 1,550 条 | 对谈 / 个人化 / "how to..." 入口句 |
| **生物黑客 Reddit 帖** | r/longevity / r/Biohackers / r/Nootropics / r/AdvancedRunning / r/fasting | 3,672 条 | 第一人称 / 提问 / 社区俚语 ("my", "stack", "fast") |
| **百岁研究论文句** | PubMed 上 centenarian / blue zone / successful aging 论文摘要切片 | 11,991 句 | 学术句子节奏（不是标题，是完整 sentence） |

每个语料独立训练一个 microGPT——同样 199 行算法、同样 PyTorch 等价改写、4 层 × 48 维 × block_size=64 × 12,000 步、约 11.6 万参数。每个模型再生成 300 个候选标题，做"新颖度审计"——分类成 (a) 完全照搬训练集、(b) 训练集中的子串、(c) **训练集根本不存在**的真新东西。最后用一个简单评分函数挑出每个模型的 30 个 gold。

**总耗时 234 秒**。这 4 分钟里在我这台 MacBook 上发生的事情，相当于一个非常专业的"长寿内容编辑团队"花一周读完上万篇论文标题 / 听完几百集播客 / 翻完上千个生物黑客 Reddit 帖之后，**抽象出 4 套写作风格的最简数学指纹**。

---

### ❷ 4 个声音的指纹（给 CEO / 创意主理人看）

![四种语料的训练曲线 + 新颖度审计 + gold 样本对比](/assets/images/microgpt/compound_generators.png)

上图最重要的信息在最底下那四列。它们**视觉上一眼就能区分**——这是这个工具最直接的产品价值。每个模型生成的样本都不像其他模型，**风格指纹是肉眼可辨的**。

下面是每个语料的"声音特征"+ "Compound 内容应用场景"对照：

**【PubMed 学术声音】** — 适合："健康知识科普"长文标题、白皮书章节标题

模型实际产出的可用样本：

- `biomarkers of biological ageing` ← 直接可用
- `the role of metformin and aging biomarkers` ← 一个完整文章选题
- `autophagy metformin longevity` ← 三概念碰撞句
- `mitochondria and control for metabolic across the lifespan`
- `regulation of a longevity`
- `the mechanism biomarkers of on mitochondria`

**【Huberman / Attia 播客声音】** — 适合：访谈系列预告、"专家说"格式短视频

模型实际产出的可用样本：

- `how to improve your time brain` ← Huberman 的 "how to ..." 模板被完美内化
- `essentials tools science of clap` ← "essentials [topic]" 是 Huberman 真实节目前缀
- `michael munger on the economics` ← 模型基于 "X on Y" 模板**虚构出在训练集中从未出现的真实经济学家姓名**（这本身既是技术发现也是合规警示——见 ❹）
- `tyler cowen on the pertinence economics`、`john taylor on the partition`

**【Reddit 生物黑客声音】** — 适合：社区驱动短帖、UGC-style 短视频脚本、SEO 长尾问句标题

模型实际产出的可用样本：

- `day fast longevity fast` ← 浓缩 fasting 圈的关键词云
- `stack for water fasting` ← Reddit 现成的发问句式
- `why water fast`、`what s can a of wake fasting` ← 极简话题入口
- `my in water am fast fast`、`hit week fast`

**【百岁研究学术句声音】** — 适合：引用、装饰、严肃文末的"学术尾注"

模型实际产出的可用样本：

- `the prevalence of the prevalence in conductrochious`
- `a total was lave included in study`
- `the of use in the the analyses of the analysis were and in the`

注意这一组**词义糊了但学术 register 完整**——这正是它的功能：在文章里为某些段落注入"严肃 / 学术"的视觉氛围，而不是为读者提供具体内容。这种 register 本身在内容平台是稀缺的。

---

### ❸ 内容生产工作流的四个具体用法（给 CEO / 内容总监看）

我把上面这套技术翻译成 Compound 团队**这周就能用**的四个具体动作。每个用法我都注明了：(场景) + (输入) + (输出) + (节省了什么)。

#### 用法 1：每周自动选题种子机

**场景**：每周一早上，内容主理人坐下来想"这周写什么？"——这是一个高频、低创造性、容易拖延的环节。

**输入**：一行命令 `python3 compound_train.py`。

**输出**：4 分钟后得到 1,200 个新标题种子，按"读起来像哪种声音"分成 4 列。再用 `curate_gold.py` 30 秒过滤出最可读的 120 个。

**它替代了什么**：替代了"内容主理人逛 Reddit / Twitter / 论文 30 分钟找选题"的环节。1,200 个选题里 95% 是垃圾，但选题筛选本来就是个高过滤率工作——人脑一晚上读 30 个选题挑 1 个，模型 4 分钟产 1,200 个挑 5 个，**仍然是 6× 工作效率**。

**ROI 估算**：假设 Compound 有 5 名内容主理人，每人每周省 1 小时选题，公司平均人时成本 $80。**每周节省 $400 = 每年 $20,800**。开发成本 $0，运行成本每周 $0.02。

#### 用法 2：风格目标定位仪（"我们听起来像谁？"）

**场景**：CEO 问内容总监——"我们的声音应该更像 PubMed 还是更像 Huberman？"——这种问题在内容公司每个月都要被讨论一次，且通常没有答案，**因为没人有量化指标**。

**输入**：把 Compound 已经发布的所有标题（比如 800 条）丢进 `compound_train.py`，再训一个第 5 个 microGPT。

**输出**：得到 Compound 自有内容的"声音指纹"。再算它和已知 4 个坐标（PubMed / 播客 / Reddit / 百岁论文）之间的"风格距离"——可以用 cross-perplexity 或 cosine 相似度算。

**结果**：一个量化的"Compound 风格雷达图"——告诉你你最像谁、离谁最远、和你目标读者期望的声音相比偏了多少。

**它替代了什么**：替代了"咱们的内容是不是太学术了？"这种主观争论。**有数字之后争论变成决策**。

#### 用法 3：声音切换器（一稿生 N 风）

**场景**：内容主理人写了一篇严肃科普——但这周公司主推社区驱动 / 短视频。手动改写一遍要 2 小时。

**输入**：把原文的 5-10 个核心短语 / 标题丢给 podcast 或 reddit 模型当种子。

**输出**：模型在该风格下生成 50 个变体短句。人类挑出有用的 3-5 个作为新标题、新副标、新 hook。

**它替代了什么**：替代了"找文案外包 / 自己重写两小时"。这一档不是替代写作，是**让一个内容资产以 5 种声音被多次复用**。

#### 用法 4：合规护栏 + 新颖度审计（给法务和股东看）

**场景**：2026 年的 AI 内容版权和训练数据合法性已经是一个真实的法律风险。任何使用 GPT-4 / Claude 生成内容的平台都面临"你这是不是在改写训练集里的版权材料"的潜在指控。

**输入**：本工具生成的所有内容自带新颖度元数据——每条标题被自动分类成 verbatim / substring / truly new。

**输出**：法务可以拿到一份"过去 3 个月本平台 AI 辅助产出的内容里 96.7% 在公开训练集里完全不存在"的可量化证据。

**它替代了什么**：替代了"我们说我们是原创"——变成"我们能用代码证明我们是原创"。这对一个**不依赖大型 LLM 服务商、自己掌握全流程**的健康内容平台，是一个具体的护城河。

---

### ❹ 几条诚实的限制（给所有人看，不夸大）

不写这一段我对不起读者：

- **这个模型 116,387 个参数**——比 GPT-4 小 1,400 万倍。它学到的是**字符级统计正则 + 风格指纹**，不是语义理解。绝大多数原始输出是 character-level gibberish，**只有 5-10% 经过过滤后真正可用**。
- **它写不了段落，更写不了文章**。它的天花板是**标题、副标题、段落 hook 句**——不是替代 GPT-4 的正文撰写，是**补足 GPT-4 不擅长的"窄风格 / 高密度品牌声音"环节**。
- **它会产生看似真实的人名幻觉**（"michael munger on the economics"——一个真实经济学家、但从未出现在我们的训练数据里）。这告诉我们：**所有产出**——哪怕是这种小模型——**都需要人工审核环节才能发布**。这条对内容主理人是个具体的工作流约束。
- **较大语料（centenarian 12k 句）反而 loss 比小语料（PubMed 1.5k 标题）更高**——这是一个对内容平台运营者**反直觉但极有用**的发现：**对窄领域风格捕捉，"小而紧"的语料比"大而散"的更好**。Compound 不需要海量数据，需要的是**风格上锐利的小数据集**。这条直接影响 Compound 未来的数据策略——是去找 100 万条普通长寿内容，还是找 5,000 条**真正符合 Compound 目标声音**的高质量内容。
- **这套 demo 是 v0.1，不是产品**。要投入实际生产至少还需要：(a) 一个 web UI 让非工程师也能跑（约 1-2 天工作）、(b) 内容主理人反馈 → 自动重训的闭环（约 1 周）、(c) 把"4 个声音"扩展到 Compound 实际定义的 8-10 个目标 segment（约 2-3 天）。

---

### ❺ 商业化路径的三档可能（给股东看的战略地图）

这套技术的部署可以分三档，**每档对应不同的资本投入和回报半径**：

#### 档位 A：纯内部工具（已实现，0 额外投入）

- **形态**：当前这个版本——一个内容主理人每周跑一次的本地脚本
- **回报**：内部生产力提升 + 选题成本下降 + AI 依赖降低
- **估算价值**：每年节省 $20K-$50K 运营成本 + **降低 OpenAI / Anthropic 涨价或限流的存在性风险**

#### 档位 B：Compound 平台特性（需 1-2 周工程投入）

- **形态**：把这套工具集成进 Compound 自己的 CMS——内容主理人在写作界面里点一个 "Inspire me with X voice" 按钮，得到 50 个种子
- **回报**：差异化竞争点（"由我们自己训练的 AI 驱动"，相比所有用 GPT-4 的同业）、用户粘性（创作者依赖该工具）、**自带的版权可审计性**
- **估算价值**：取决于 Compound 用户基数 — 但这是一个**结构性产品差异化**，不是"我们更便宜"或"我们更快"那种容易被复制的差异化

#### 档位 C：对外 SaaS 产品（需 2-3 月工程投入）

- **形态**：把这套技术包装成 "Brand Voice Fingerprint" SaaS——任何内容平台 / 公司可以上传他们的内容，得到他们的"声音坐标"和"灵感种子流"
- **市场**：每个有内容产品的初创公司（健康 / 金融 / 法律 / 教育 / B2B）都是潜在客户
- **核心卖点**：(1) 不依赖大型 LLM、(2) 自带版权护栏、(3) 单位成本极低（一台 server 能跑数百客户）、(4) **客户自己的数据从不离开他们的服务器**（隐私护栏）
- **估算价值**：早期 ARR 上限难估，但这是一个**真正"AI 但不是 GPT 包装"的差异化产品**——市场上 99% 的 "AI 内容工具"都是 GPT-4 wrapper，这个不是

档位 A 已经做完。档位 B 是我个人觉得最值得做的——投入产出比最清晰，且**可以作为 Compound 平台一个独有功能写进 pitch deck**。档位 C 是更长远的可能性，需要 CEO / 投资人共同评估。

---

### ❻ 这一节相对前面所有实验的根本不同

把这一节和文章前面那些实验区分开：

- 前面的"温度扫描"、"缩放"、"PyTorch 等价"、"字节级复现"——都在 Karpathy **已知答案的范畴里**做验证。技术上扎实，但本质是"博士功课"。
- 这一节是**在 Karpathy 没做过的事情上做出新东西**：把同一份 199 行算法用到一个**真实的内容生产场景**，给出**可复用的工作流**（语料 → 训练 → 审计 → 过滤），并明确**4 个生产用法 × 3 档商业化路径**。

技术本身的价值有限。**把工程对象长进具体业务里——这才是 ROI 真正出现的地方**。

完整的代码（199 行 microGPT + 抓取脚本 + 训练脚本 + 审计脚本 + 4 个语料 + 4 个模型权重 + 1,200 个原始样本 + 120 个 gold 样本）都在 `/Users/elemer/Documents/microgpt/` 下，CTO 可以完整审计；CEO 可以让任何工程师复现；股东可以放心——这不是 PPT，这是一个**已经在工作的工具**。

完整数据、训练代码、4 个 corpora、4 个模型权重、300×4 个原始样本和 30×4 个 gold 样本都在 [`/Users/elemer/Documents/microgpt/`](/microgpt-artifacts/) 下，可被任何看到这篇博客的人完整审计。

## 把这次实验翻译成你的日常：三个具体场景

到这里所有"算法"和"数字"都讲完了。下面用三个场景把它落地——这不是工程师向工程师说话，是普通人**今天下午就能用上**的判断工具。

**场景一：你看到一条"GPT-X 在某测试上得分提升 20%"的新闻**

旧反应："厉害，AI 又进化了。"
新反应：先停一下问——这 20% 是因为 (a) 算法层面真的换了一个新东西，还是 (b) 同一个算法被训练得更久、跑在更大的数据上、或者用了新的 efficiency 优化？

记住一条经验：**重大新闻里 90% 是 (b)**。一颗种子封印整条计算链、PyTorch 把同一份算法跑快 165 倍——这两件事我亲眼跑出来了——告诉你 AI 的算法本身相当稳定，每次"突破"几乎都是 efficiency 一档新升级。这不是说 (b) 不重要——它对产品体验、对算力市场、对国家战略都极度重要——只是它的**持久性**和"新能力"完全不同：efficiency 红利会被竞争对手 6-12 个月内追平，而真正的新算法可以维持 5-10 年的代差。这一条区分能让你看新闻、看股价、看监管文件都精准一档。

**场景二：你在和 ChatGPT 对话，它给出一个看起来很自信但其实错误的答案**

旧反应："它怎么会这么离谱？"
新反应：你想起这篇文章里的 4192 个参数怎么把训练集里**根本不存在**的 `karia`、`vialan` 当成"真名"生成出来。它不是"撒谎"也不是"理解错了"——它从来就没有"理解"过任何东西，只是在做一个被概率分布加权的随机抽样。

这个具身的认识会改变你**用 AI 的方式**。你会更自然地：
- 在它给出引用、数字、专有名词时**主动核实一遍**——不是因为它"经常出错"，而是因为它的核心机制就是抽样，抽样在低频区域必然产生伪造（行话叫 hallucination）。
- 在它语气最自信时**警惕性最高**——温度参数低就显得自信，但低温恰好是它最容易"模式坍塌"、反复输出陈词滥调的状态（看本文「温度扫描」那张表）。
- 把它当成一个**才华横溢但毫无核实义务的实习生**——你来负责事实校对，它负责文字流畅度。

**场景三：你的朋友/家人觉得 AI 神秘可怕，问你"它会不会有意识"**

旧反应：扯一些科幻和哲学。
新反应：你可以打开这篇博客，指着那 4192 个参数和 20 个杜撰名字说——**这就是它**。从这台 Mac 上的 4192 个参数到 GPT-4 的 1.6 万亿，量级差了 4 亿倍，但**机制完全相同**：从大量文本里学到字符（或子词）的统计规律，然后在你提问时按这些规律抽样生成下一个 token。

这不是"会思考的机器"，这是一个被训练得**异常擅长模仿人类文本表面统计规律**的概率引擎。它产生的"灵感"和我跑出来的 `kamon` 是一类东西，只是规模大到能制造出连贯的篇章。

这套表述既不是"AI 万能"的吹捧，也不是"AI 假货"的贬低——它是**第一性原理**层面的描述，准确、好用、不会被下一波风潮冲掉。你的朋友家人**比媒体更需要这个**。

---

写完上面三个场景，我再说一句更难听的话：**如果你读完一篇技术博客，没法把它翻译成至少一个日常场景里的判断变化，那这篇博客对你就白读了。** 我自己写技术内容的时候经常忘记这条，靠这次复盘提醒。

## 200 行算法核心：那条不可压缩的线

microGPT 整个项目最被低估的部分不是代码，是它**画出的那条线**。

线的左边——199 行——是不可压缩的算法核心：数据加载、tokenizer、autograd、GPT 架构（embedding → multi-head attention → MLP → residual → rmsnorm）、Adam、训练循环、推理循环。

线的右边——万亿 token 数据集、bfloat16、FlashAttention、MoE、RoPE、GQA、KV cache 优化、RLHF、vLLM、batched inference、multi-GPU 训练……——**全部都是 efficiency**。

这条线对持有 [Bastiat Filter](https://en.wikipedia.org/wiki/That_Which_Is_Seen,_and_That_Which_Is_Not_Seen) 心智模型的人应该非常熟悉——**"看得见的"（ChatGPT 的会话界面、OpenAI 的市值）vs "看不见的"（200 行算法核心）**。整个 AI 产业的资本估值、监管讨论、地缘政治焦虑都堆在右边的 efficiency 层；但本质属性（涌现、幻觉、对齐难题、上下文窗口、缩放律）都从左边 200 行已经看得见雏形。

跑过 microGPT 的人能区分两类差异：

- **结构性差异**：架构变体、训练数据策略、目标函数选择——这些是持久的。
- **工程领先**：KV cache 管理、推理优化、混合精度——这些会被快速抹平。

这条判断标准对做投资分析、做监管解读、做产品策略、做学术写作都直接复用。

## 为什么我（具体来说）值得花这一下午

通用层面别人都说过的我不重复（"祛魅 LLM 黑盒"、"理解 attention"等等）。三条更针对性的：

**1. "我无法创造的我不理解"——但 LLM 时代这句话有了新含义。** 我在 Penn Law 上 IP 与国家经济价值创造的课，所有关于 AI 模型版权、训练数据合法性、生成式 AI 责任分配的法律辩论，都建立在一个对"模型到底在做什么"的隐含技术假设上。当法庭辩论"模型是在'记忆'还是'学习'训练数据"时，没跑过 microGPT 的法学家在凭直觉说话；跑过的人知道：**那个 4192 参数的小盒子里发生的就是 27 维概率分布的迭代调整**——没有"记忆"也没有"理解"，只有统计规律的内化。这是写 IP 论文、做 AI 合规建议时第一性原理层面的弹药。

**2. 闭环认知基础设施的一块基石。** 我每天用 Claude 做学术写作 pipeline、知识图谱、Bob 翻译、本地 LM Studio 推理——AI 是我"life cockpit"里的关键传感器/执行器。**日常依赖的认知基础设施，应该有"亲手造过最简版"的经验。** 这不是工程洁癖，是 antifragility：当下次 AI 范式换代（无论是 token-free model、新型 attention、还是某个我们还没想到的架构）时，对算法核心的握感不会因某一篇博客文章作废。

**3. 输出质量的元判断会精准一档。** 跑过 microGPT 之后，看到 Claude 给出"完全错误但措辞自信"的回答时，我会有一种具身的直觉——我看过 4192 参数的小模型怎么把训练集里没有的 `karia`、`vialan` 当成"真名"生成出来。这对"这次输出能不能信"的元认知判断有直接帮助。

## 几点诚实的提醒

写下来才不至于自欺。

- **microGPT 是教育代码，不是研究代码。** 1 个 layer、16 维 embedding、1000 步训练，对应的是一个连"emma"和"olivia"之间的句法关系都学不全的玩具网络。**不要在博客里宣称"我训练了一个 GPT"——你训练的是一个演示 GPT 架构的微型模型**。
- **"其余皆 efficiency"在算法意义上是对的，但 efficiency 那一侧装着 95% 的工业 know-how。** 从字符级到 BPE、从 1 层到 100 层、从 4192 参数到 1.6T 参数，每一步的工程难度增长不是线性的。读完 200 行不等于能去面试 ML infra 岗。
- **199 行不是 200 行。** Karpathy 博客文本说约 200 行，gist 里实际是 199 行。我数下来去掉空行注释后约 145 行可执行代码。这种校核动作小，但是可信度的一部分。

## 极简复现指南

如果你也想 1-2 分钟跑出和我一样的样本：

```bash
# 1. 准备目录
mkdir -p ~/Documents/microgpt && cd ~/Documents/microgpt

# 2. 下载 microGPT（Python 3 标准库即可，无需 pip install）
curl -O https://gist.githubusercontent.com/karpathy/8627fe009c40f57531cb18360106ce95/raw/microgpt.py

# 3. 跑（首次会自动下载 names.txt）
/usr/bin/time -p python3 -u microgpt.py 2>&1 | tee run.log
```

预期：

- M3 Pro：约 60-90 秒；M1/M2：约 90-150 秒；老 Intel Mac：3-5 分钟
- seed=42 下，最终 20 个样本应当是 `kamon, ann, karai, jaire, vialan, karia, yeran, anna, areli, kaina, konna, keylen, liole, alerin, earan, lenne, kana, lara, alela, anton`——和这篇博客一致

如果对得上，恭喜你拥有了一个字节级可复现的 4192 参数 Transformer。

## 接下来几条值得做的实验

按预期收益从高到低：

1. **温度扫描**（10 分钟）✓ 本文已做。把五种温度的输出并排放进笔记里——非技术朋友的最佳教具。
2. **模型缩放**（1 小时）✓ 本文已做。我得到的反期待结果（11× 参数 → loss 几乎不变）比"顺滑下降"更有教学价值。
3. **PyTorch 等价改写**（半天）✓ 本文已做。loss 序列 1e-11 量级一致、20 个样本 byte-identical、速度 165×——是 Karpathy "其余皆 efficiency" 那句话最硬的实证。
4. **数据集替换**（30 分钟）。把 `names.txt` 换成你笔记里的论文标题、香港地名、Pokemon 名字、CFA 考题。同一份代码、不同数据 → 完全不同风味的幻觉。这是理解"模型只学到统计正则"最直接的实验。
5. **梯度数值验证**（1-2 小时）。对任意参数 `p`，用有限差分 `(L(p+ε) − L(p−ε)) / (2ε)` 算"经验梯度"，与 `p.grad` 比较。两者误差应在 1e-6 量级。这是亲手验证 `Value` 类没骗你——也是工业级发现 autograd bug 的方法。

(4)(5) 留给后续博客。

## 附：本次运行的环境戳

```
Machine        : MacBook, Apple Silicon (arm64)
OS             : macOS 26.4.1 (Build 25E253)
Python         : 3.10.13 (miniforge3)
Wall clock     :  104.82s  baseline run (session 1)
                   99.97s  baseline run (session 2, byte-identical samples)
                  100.95s  training + temp sweep
                  121.94s  scalar high-precision run (for torch comparison)
                  452.51s  scaling experiment (4 configs × 500 steps)
                    0.74s  PyTorch tensor port (165× faster, samples byte-identical)
torch          : 2.0.1, CPU + float64 + single-thread BLAS
matplotlib     : 3.10.9 (用于绘图，不参与训练)
```

完整 log、losses CSV、温度扫描 JSON、scaling 结果、绘图脚本都在 `/Users/elemer/Documents/microgpt/` 下。



---

> **延伸阅读**：[Karpathy 原文 microGPT](https://karpathy.github.io/2026/02/12/microgpt/) · [microgpt.py gist（含 6 版渐进 build_microgpt）](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95) · [makemore 数据源](https://github.com/karpathy/makemore)
