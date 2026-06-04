---
title: Thoughts Behind This Space
permalink: /thoughts-behind-this-space/
listed: true
---

This webpage features no starry backgrounds from the Geocities era, nor does it indulge in the magical dynamic illusions of marquee tags. Its ambition is to regress directly to the primordial physical state of the World Wide Web at its inception—becoming a pure document embedded with hyperlinks. This deliberate rollback spans critical milestones in the evolution of the Web. Tim Berners-Lee submitted his proposal for the World Wide Web to CERN in 1989, and shortly after, in December 1990, he placed the world's first website onto the info.cern.ch server. By April 1993, with the release of NCSA Mosaic 1.0, humanity embedded images into body text for the very first time. Only after that, in 1994, was Cascading Style Sheets (CSS) proposed, while JavaScript—hastily whipped up by Brendan Eich in just ten days—had to wait until 1995. During this brief interregnum, webpages consisted of nothing but text, links, and minimal formatting. They were incredibly lightweight, and they were blazing fast.

<figure>
<img src="/assets/images/mosaic-1993.png" alt="Screenshot of the NCSA Mosaic browser window displaying an early web page">
<figcaption>The user interface of NCSA Mosaic 1.0, released in April 1993. The moment images were embedded into body text, the web's Gravity began to irreversibly increase. Screenshot of the Mosaic interface; public domain (CC0).</figcaption>
</figure>

Below is the underlying logic behind my infatuation with this primitive style, along with its aesthetic rationale in a modern context.

## I. An Austere Selection Mechanism

In 1910, Adolf Loos delivered his famous lecture *Ornament and Crime* (*Ornament und Verbrechen*) in Vienna, bluntly equating redundant ornamentation with the degradation of civilization. He subsequently designed and constructed the Looshaus, a commercial and residential building completely devoid of embellishment, standing naked before the Habsburg Hofburg Palace. At the time, the public derided the building as the "house without eyebrows," and even the Emperor refused to draw his curtains to look at it. Yet, over a century later, it stands there still.

This obsession with the essential actually forms part of a sprawling aesthetic lineage. Dieter Rams emphasized "Less, but better" (*Weniger, aber besser*) in his Braun design principles; Mies van der Rohe left us the famous maxim "Less is more"; Jan Tschichold returned to classical grids in his later years; and Massimo Vignelli steadfastly believed that a designer's life is a continuous fight against ugliness. The core of these manifestos is not a blind exercise in subtraction, but rather a ruthless process of selection. When you retain an element on a page, you must be able to independently justify why it deserves to occupy the reader's field of vision.

In his 1983 seminal work, *The Visual Display of Quantitative Information*, Edward Tufte quantified this intuition as the **Data-Ink Ratio**. He argued that every drop of ink in a chart must carry effective information, and that all unnecessary decorative ink (Chartjunk) should be relentlessly expunged. On this website, I have simply replaced ink with bytes.

## II. The Fiduciary Duty of Attention

Simone Weil once wrote that attention is the rarest and purest form of generosity. Although she was speaking of prayer and scholarship at the time, this proposition translates directly into the information age. **When you open this page, you have ceded a small portion of your life's equity—your attention—to me. As a creator, I owe you a Fiduciary Duty not to squander it.**

Yet, the modern web ecosystem is collectively moving in the exact opposite direction. Byung-Chul Han's critique in *The Burnout Society* is even more scathing: he argues that excessive stimulation itself constitutes a form of violence. Massive hero images, ubiquitous Cookie consent pop-ups, and interactive interfaces that are dynamic purely for the sake of being dynamic—analyzed in isolation, these designs might seem justifiable. But when stacked together, the modern webpage mutates into an adversarial environment saturated with cognitive noise. To extract a few hundred words of information, readers must parry visual distractions like soldiers in combat.

In *Amusing Ourselves to Death*, Neil Postman pointed out with surgical precision that the form of a medium tames and shapes the structure of its content. When text is plunged into a deep ocean of noise, the text itself degrades into noise. Once a creator begins to evaluate this predatory hijacking of attention from an ethical standpoint, those so-called visual embellishments can never be added back.

## III. The Lost Primordial Compact of the Web

In the early days, Tim Berners-Lee consistently championed a principle known as **Universality**. This dictated that a webpage must be accessible without barriers on any device, across any network bandwidth, and under any physical condition. This is the ontology of the webpage—meaning that **a webpage is, first and foremost, a document that can be read by anyone**; everything else is merely derivative.

<figure>
<img src="/assets/images/first-web-server.jpg" alt="The NeXTcube computer that served the first website, with a handwritten red warning label, at CERN">
<figcaption>The world's first World Wide Web server, running at CERN. This NeXTcube computer bears a red, handwritten label warning maintenance staff: "This machine is a server. DO NOT POWER IT DOWN!!" This was the foundational capital of the entire digital era. Photo: Coolcaesar, CC BY-SA 3.0.</figcaption>
</figure>

Today's webpages routinely breach this primordial compact. A standard blog post is often wrapped inside a massive JavaScript bundle, causing it to crash outright under high latency in poor network environments or on legacy hardware. This Website Obesity Crisis essentially represents developers taking technical shortcuts—transferring maintenance costs and architectural complexity onto the reader's bandwidth and battery life.

Maciej Cegłowski made a highly satirical comparison in 2015: the plain text of a novella takes up roughly 400 KB, yet countless technical blogs today consume more resources to load a few hundred words of text than Leo Tolstoy's entire *War and Peace*. It is a webpage in name only; in reality, it is a Single Page Application (SPA) masquerading as a webpage, executing remotely on the user's client. My choice is to retreat to the terms of the original contract: utilizing static HTML coupled with a modicum of Markdown, flattened directly by Jekyll during local compilation. The server delivers the file, the browser renders the file, and the interaction ends there.

## IV. The Engineering Will to Control Complexity

In 1995, Turing Award laureate Niklaus Wirth proposed what is now famously known as Wirth's Law: software is slowing down faster than hardware is accelerating. This occurs because the complexity of software systems naturally expands until it consumes every bit of breathing room provided by hardware advancements. To counter this, the pioneers of computer science arrived at a profound consensus. Edsger W. Dijkstra maintained that simplicity is a prerequisite for reliability; Brian Kernighan pointed out that controlling complexity is the very essence of computer programming; and the Unix philosophy advocates doing only one thing and doing it well.

This represents the optimism of classical engineers: through disciplined selection, a sufficiently simple system can simultaneously deliver extreme speed, deterministic reliability, and a significantly longer lifespan. This website's style sheet clocks in at under 60 lines, inlined directly within the `<head>`. It features zero third-party fonts, zero external scripts, and zero user tracking (Telemetry). Its speed involves no technical black magic; it is fast simply because, physically, there is almost nothing to load.

In *Tools for Conviviality*, Ivan Illich warned that tools ought to be mastered by their users, rather than the other way around. A bloated website heavily dependent on third-party cloud services is heading toward the ultimate fate of being subjugated by its tools. A plain text file, conversely, stands resolutely in the opposite direction.

## V. Files as Self-Sustaining Time Capsules

Here, I have reserved an exceptional architecture for myself. A select few articles require complex prototype demonstrations or interactivity; these exist as independent, self-contained single-file HTMLs complete with their own interactive logic and inlined styles. They bypass any global templates and sit autonomously within specific directories.

This remains aligned with the vision of the Memex outlined by Vannevar Bush in his seminal 1945 article *As We May Think*. The Memex was conceived as the ultimate information carrier, capable of fully encapsulating everything an individual reads, annotates, and links throughout their lifetime. Ted Nelson pushed this intuition to its extreme in the 1960s by founding Project Xanadu, dedicating his life to the permanence and immutable traceability of documents.

<figure>
<img src="/assets/images/memex-1945.jpg" alt="1945 LIFE magazine illustration of a future scientist wearing a head-mounted camera, headlined 'As We May Think'">
<figcaption>The opening illustration of Vannevar Bush's <em>As We May Think</em>, as reprinted in <em>LIFE</em> on September 10, 1945 and drawn by Alfred D. Crimi: a scientist of the future recording what he observes through a head-mounted camera. The same essay imagined the Memex—a desk meant to encapsulate everything one reads, annotates, and links across a lifetime. Public domain.</figcaption>
</figure>

My ambition is far less grand. I pursue only a baseline requirement: **if you download this file locally and disconnect from the network, double-clicking it twenty years from now will still render it perfectly in any browser.** It requires no build tool configurations, no node package (`npm install`) dependencies, and relies on no cloud services that could go offline at any moment. An HTML file is a complete, self-sustaining time capsule. On this scale, the lifespan of a text file far outlasts the vast majority of commercial online services on the market today.

This decoupled architecture governs the entire operation of the website: Markdown handles high-density daily reflections and textual output, while single-file HTML accommodates any personalized expressions requiring specific visual and interactive designs. There are no frameworks in between, no massive component trees, and no backend services that require constant maintenance. Both ends consist entirely of native files.

## VI. An Honest Scrutiny After Media Dehydration

This extreme minimalism brings a brutal side effect: if the writing is poor, the mediocrity of thought is exposed completely bare.

Marshall McLuhan's famous aphorism, *The medium is the message*, reveals another facet of its meaning here. When the thickness of the medium is compressed down to near zero, the message must carry its entire gravitational weight alone. When you strip away elegant typography, sophisticated gradient color schemes, and silky smooth transitions, the page is reduced strictly to the text itself. The writer is left with no visual magic tricks to conceal mediocre ideas. For the reader, this offers a highly efficient information-gathering experience; for the writer, it serves as a rigorous discipline of cognitive rigor and honesty. Design steps completely out of the way; now, it is entirely about what you have actually written.

## Closing

In his 1880 lecture *The Beauty of Life*, William Morris left behind a highly critical maxim:

> Have nothing in your houses that you do not know to be useful, or believe to be beautiful.

This website simply executes that command to its absolute limit within digital space. Every single byte retained is either transmitting information efficiently or embodying the classical beauty of the early World Wide Web. And within the unique medium of a webpage, **the only thing capable of perfectly uniting both utility and beauty is the text itself.**
