---
title: Writing an OS for My Children
permalink: /writing-an-os-for-my-children/
listed: true
---

*The Hardcore Minimalism and Educational Experiment of mini-os*

## The Origin: Breaking the Cognitive Collusion of "Technological Magic"

Modern software engineering is a massive black box built upon countless layers of abstraction.

When a child presses a button on a screen, witnesses an animation, and hears a sound, if they ask, "How is this implemented?", the explanation provided by most adults stops at "programmers wrote code." If the child pushes further, asking, "How does code turn into an image?", existing youth programming tools (like Scratch or highly encapsulated Python libraries) fail to provide an answer. They hide nearly twenty layers of underlying logic. This educational approach only teaches children how to "assemble blocks," while concealing the actual material and structure of the wood itself.

When technology is extremely abstracted, it transforms into magic in the eyes of the next generation. This worship of magic erodes the fundamental self-confidence required to deconstruct the world and alter its foundations.

To shatter this "black-box collusion of technology," I conducted a thought experiment: If we want to strip away all the packaging of modern computers in the shortest possible span of code, allowing a child to look directly into the essence of hardware, how should that code be written?

In collaboration with Claude Code, I manually constructed a bare-metal bootable, hardware-keyboard-responsive, interactive shell-capable minimal operating system entirely in C++.

It features zero third-party libraries and lacks any modern operating system base. The entire codebase is exactly 492 lines.

This project is called **mini-os**. It is a tangible, runnable entity designed to prove to future children that the world is not a black box monopolized by untouchable tech conglomerates—the underlying layer is clear and perceptible.

<figure>
<img src="/assets/images/mini-os-boot.png" alt="mini-os booting inside QEMU: a green banner reads 'Hello from dad's mini-OS!', followed by blue lines stating it was written in C++ and booted by GRUB via Multiboot1 on bare metal, and a yellow line reading 'Stage 2 reached: kernel is alive.'">
<figcaption>mini-os reaching its C++ entry point inside QEMU. Every glyph here—the green banner, the blue boot provenance, the yellow "kernel is alive"—was placed by writing one 16-bit value at a time into video memory. There is no operating system beneath this; the kernel <em>is</em> the whole machine.</figcaption>
</figure>

---

## Architecture and Engineering Choices

### Minimalist Selection Matrix

When defining the technology stack, my sole evaluation criterion was: Does this decision maximize the "transparency of causality" while eliminating industrial-grade noise that distracts from core comprehension?

| Dimension | Option A | Option B | Final Choice | Educational Logic Behind the Engineering Decision |
| --- | --- | --- | --- | --- |
| **Processor Architecture** | 32-bit i686 | 64-bit x86_64 | **i686** | Entering 64-bit Long Mode requires writing around 40 additional lines of obscure assembly initialization code. This is protocol noise that contributes nothing to understanding the core essence of computers. |
| **Boot Method** | GRUB + Multiboot1 | UEFI + Limine | **GRUB** | The Multiboot1 specification is incredibly elegant; its core protocol can be read on a single page. Conversely, the complexity of UEFI is an absolute monolith that would discourage a child before the machine even boots. |
| **Keyboard Input** | Hardware Interrupts (IRQ) | Port Polling | **Port Polling** | Interrupts require configuring the GDT, IDT, and PIC remapping, which involves nearly a hundred lines of hardcoded setup. Polling takes only about 30 lines of code; when a key is pressed, the register changes instantly, creating an extremely short causal feedback loop. |
| **Development Language** | C / Rust | C++ | **C++** | C lacks modern architectural organization like namespaces; Rust's Borrow Checker introduces an excessive cognitive load. C++ allows us to clearly express engineering intent using `namespace`, `constexpr`, and `enum class` while maintaining absolute honesty regarding memory. |

### Hardware Boot Chain

From pressing the simulated power button to printing the first character on the screen, the physical and logical chain is entirely traceable, leaving no layer where you must tell a child, "You'll understand when you're older":

```
[ Physical Power Button Pressed ]
               │
               ▼
[ BIOS POST and Reads Optical Drive ]
               │
               ▼
[ Load GRUB Bootloader from ISO ]
               │
               ▼
[ GRUB Parses grub.cfg and Loads kernel.bin ]
               │
               ▼
[ GRUB places the kernel image at physical memory 1 MiB per the Multiboot1 header ]
               │
               ▼
[ Hardware jumps to assembly entry _start ] ─── Establish Stack Pointer
               │
               ▼
[ Call C++ entry kmain() ]
               │
               ▼
[ Initialize VGA Video Memory Buffer → Launch Keyboard-Polling Shell shell::run() ]
```

### Code Organization and Line Alignment

The distribution of these 492 lines of code across the repository is exceptionally disciplined, with each line representing an indispensable cornerstone of computing:

| File Path | Physical Lines | Core Responsibility / Hardware Mapping |
| --- | ---: | --- |
| `src/boot.s` | 36 | Declares the Multiboot1 magic number, initializes the CPU stack, and handles the handoff from assembly to C++. |
| `linker.ld` | 32 | Linker script. Explicitly commands the linker to place the kernel code and data segments at physical address 0x100000 (1 MiB). |
| `src/kernel.cpp` | 17 | Core kernel entry `kmain()`, responsible for hardware scheduling and initialization. |
| `src/vga.h / .cpp` | 107 | Maps the 0xB8000 text-mode video memory, handling cursor movement, screen scrolling, and backspace logic. |
| `src/io.h` | 19 | Encapsulates inline assembly `inb` / `outb` instructions to achieve direct communication between the CPU and peripheral ports. |
| `src/keyboard.h / .cpp` | 80 | Takes over the PS/2 controller ports, converting raw scan-code state machines into ASCII characters. |
| `src/shell.h / .cpp` | 135 | The system's REPL (Read-Eval-Print Loop) shell, implementing a self-contained built-in command parser. |
| `Makefile` | 59 | Automates the cross-compilation toolchain, builds the ISO image, and mounts the QEMU virtual machine. |
| `grub.cfg` | 7 | Instructs the GRUB bootloader on the physical path of the kernel. |
| **Total** | **492** | **A complete, self-contained, interactive bare-metal operating system.** |

<figure>
<img src="/assets/images/mini-os-shell-help.png" alt="The mini-os shell after running the help command, listing five built-in commands—help, echo, about, colors, and clear—each with a one-line description, and a green mini-os prompt awaiting input">
<figcaption>What those 135 lines of <code>shell.cpp</code> produce: a complete REPL. Each entry in this menu is a single <code>if</code> branch, and the blinking <code>mini-os&gt;</code> prompt is the entire user interface—no terminal emulator, no shell process, no kernel underneath doing the work for it.</figcaption>
</figure>

---

## Technical Philosophy: How to Realize "Demystification" through Code

### 1. Eliminate All Hidden Runtimes

The core reason for choosing C++ is its honesty.

In modern application development, Python conceals memory addresses, and Go hides the thread pauses of Garbage Collection (GC). In this codebase, nothing is concealed:

```cpp
volatile uint16_t* const BUFFER = reinterpret_cast<uint16_t*>(0xB8000);
```

This is the heart of `src/vga.cpp`. This single line of code directly reveals the ultimate secret of graphical interfaces to a child: the "screen" is fundamentally just a specific segment of memory. Writing a 16-bit number to the physical address `0xB8000` instantly illuminates a character at the corresponding coordinates on the screen. The higher 8 bits control the background and foreground colors, while the lower 8 bits map to the ASCII encoding. There are no window libraries, no rendering engines—only direct writes to physical hardware.

### 2. Closed-Loop Hardware Causality

In application-level programming, a user presses a key, the event is captured by the operating system, passed to a graphics framework, and then routed to the application logic—a pipeline spanning millions of lines of code.

In mini-os, the causality is raw and direct:

- Physical keyboard is pressed → emits a physical electrical signal.
- CPU fetches a raw byte (e.g., `0x23`) directly from the I/O port via the `inb(0x60)` instruction in `src/io.h`.
- `keyboard.cpp` looks up the table: `0x23` maps to the character `'h'`.
- `shell.cpp` receives `'h'` and calls `vga::putc('h')`.
- The character is written to the memory slot corresponding to `0xB8000`.
- The graphics card hardware (VGA controller) scans this video memory at a fixed frequency, projecting the pixels of `'h'` onto the display.

Every link in this chain corresponds to a few lines of transparent code in this repository. Children can manually modify the scan-code mapping table or invert character colors; upon running `make run`, the hardware's behavior shifts instantaneously.

<figure>
<img src="/assets/images/mini-os-shell-echo.png" alt="The mini-os shell running 'echo hi from qemu', which prints 'hi from qemu' on the following line beneath the command list">
<figcaption>The causal chain made visible. Typing <code>echo hi from qemu</code> drives every keystroke through the PS/2 port, the scan-code table, the shell parser, and finally into the bytes at <code>0xB8000</code>. Nothing on this screen arrived by magic—each character was put there by code short enough to read in an afternoon.</figcaption>
</figure>

---

## Progressive Educational Deconstruction

I do not believe in patronizing, "top-down" instruction. When guiding a developing mind, this 492-line repository should be peeled back layer by layer like an onion, matching different stages of cognitive development:

| Cognitive Stage | Accessible Technical Layer | Experiment & Interaction Design |
| --- | --- | --- |
| **Visual & Perceptual Phase** (Ages 5–7) | Presenting the presentation layer and the essence of color | Skip the code. Simply execute the `colors` command and observe the 16-color palette. Explain to them: "The world inside a computer is just like painting. The vibrant colors on the screen are actually the operating system counting numbers. Once it reaches 15, it runs out of colors." |
| **Logical Enlightenment Phase** (Ages 8–10) | Deconstructing instruction flows and conditional control | Open `shell.cpp` and demonstrate the `if-else` branches of the built-in commands. Let them try to manually add a `joke` command, directly modifying the compiled string to understand that "a program is a deterministic causal chain running along a set track." |
| **Underlying Contact Phase** (Ages 11–13) | Mapping physical space and hardware interfaces | Introduce concepts of pointers, physical addresses, and I/O ports. Read `vga.cpp` together, and bypass the shell to "draw" their own name at an arbitrary position on the screen by directly reading from and writing to the `0xB8000` physical memory. |
| **System Architecture Phase** (Ages 14+) | Understanding the bare-metal boundaries of computers | Completely dissect the assembly file `boot.s`, the linker script `linker.ld`, and CPU register operations. Grasp exactly how a computer pulls itself up by its own bootstraps in a vacuum completely devoid of software support. |

---

## Bare-Metal Evolution Spaces: Engineering Checkpoints for Their Growth

Exceptional system design resembles an architectural use of negative space, intentionally leaving extensible interfaces behind. Atop this 492-line foundation, I have deliberately reserved clean pathways for evolution. As their cognitive abilities advance to higher levels, these can serve as weekend hacker challenges:

- **Timer Interrupt:** By configuring the GDT, IDT, and the 8259 PIC chips, hijack the CPU's `0x20` interrupt to render a hardware clock in the bottom-right corner of the screen that ticks precisely every second.
- **Concurrency Primitives (Task Switching):** Allocate two distinct stack spaces in memory. When a timer interrupt triggers, force the saving and restoring of CPU register states via assembly (a context switch), allowing two different shell functions to execute concurrently and alternately. This marks the true starting point of a modern multitasking operating system.
- **Block Device Reading (Storage & FAT12):** Implement a rudimentary IDE channel port driver to read sectors directly following the ISO image, parse the FAT12 file system structure, and achieve true loading and execution of external files from disk.

---

## Execution Guide

In an environment equipped with a cross-compilation toolchain, you can interact with the physical simulation layer through minimalist Makefile directives:

```bash
# 1. Compile the kernel source code, integrate the binary with GRUB,
#    and package it into a standard ISO optical disc image.
make

# 2. Launch the QEMU virtual machine, fully exposing the configured
#    CPU states, memory mappings, and video memory within the window.
make run

# 3. Clean up all intermediate compilation artifacts and binary images.
make clean
```

---

## Afterword: An Anchor for the Future

This is a thought experiment directed toward the future.

At the moment this code is written, the imagined individual might still be a long way from actually sitting in front of a computer. I am writing this not to force them into becoming a software engineer, nor to show off some underlying technical privilege.

I simply want to plant a solid anchor for them at the very bottom of an increasingly complex virtual world.

When they grow up and confront a reality heavily wrapped in algorithmic recommendations, AI models, and commercial frameworks, I hope this tiny, sub-500-line system will remind them of a profound truth:

> Every complex creation you see in this world—be it the ceaseless internet, vast and deep AI neural networks, or highly automated societal rules—is written line by line at its foundation by real, concrete human beings.
>
> The people who wrote those rules get tired, and they make mistakes, just like us. This means there is no unbreakable black box in this world. As long as you are willing to strip it down layer by layer, you can always see through to its essence; and once you see its essence, you possess the right and the capability to rebuild it.
