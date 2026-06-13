---
title: "Mud, Silence, and the Architecture of Common Knowledge"
permalink: /mud-silence-and-the-architecture-of-common-knowledge/
listed: true
math: true
---

# Mud, Silence, and the Architecture of Common Knowledge: The Muddy Children Puzzle from Hard to Soft Information

> **Provenance.** This essay grew out of a final project I wrote for an epistemic logic course in the Department of Philosophy at Tsinghua University. The original analyzed the muddy children puzzle in Public Announcement Logic and sketched a soft-information variant via radical upgrade. For publication I have rebuilt it: the thesis is sharper, several technical claims in the original were wrong and are corrected here, the literature is properly engaged, and every formal claim in this version has been machine-checked by a small model checker whose source accompanies the post (Appendix B).

**Abstract.** The muddy children puzzle is usually presented as a charming exercise in iterated reasoning. Read carefully, it is something better: a minimal laboratory in which the central distinctions of the logic of information come apart and can be measured. This essay uses the puzzle to make one argument in two movements. First, in the *hard-information* regime of Public Announcement Logic, the puzzle is a theorem about common knowledge: the father's announcement adds no first-order information whenever at least two children are muddy, yet it alone makes the inductive cascade possible, and the final round of "I do not know" is a sentence that destroys itself by being uttered. Second, in the *soft-information* regime of plausibility models and lexicographic upgrade, the same protocol reproduces the same round structure at the level of belief, with one decisive difference: when the source errs, hard update deletes reality from the model and no announcement can bring it back, while soft upgrade misleads briefly and recovers in a single step. Certainty and revisability are purchased with the same currency, and the puzzle prices the trade. Seven numbered results carry the argument; together with their supporting claims they compile to fourteen machine checks, all of which pass by exhaustive model checking for up to five children.

## 1. A Puzzle That Is Really a Theorem About Silence

The story is old. J. E. Littlewood opens *A Mathematician's Miscellany* (1953) with a version about three ladies in a railway carriage, each with a smudged face, each laughing at the others, until one of them reasons her way to the realization that she must be laughable too: if my own face were clean, the second lady would see nothing funny about herself reflected in the third lady's behavior, and would have stopped laughing already. George Gamow and Marvin Stern retold it in *Puzzle-Math* (1958) as the tale of forty unfaithful wives and a sultan's proclamation. Computer scientists adopted it in the 1980s, when Jon Barwise (1981) and then Joseph Halpern and Yoram Moses (1990) recognized that the puzzle is not a curiosity but a compressed specification of what *common knowledge* is and what it costs to obtain. Moses, Dolev, and Halpern (1986) spun an entire paper of variants out of it, with a title, "Cheating Husbands and Other Stories," that remains the field's best, and the puzzle entered the canon as the opening example of the standard textbook (Fagin, Halpern, Moses, and Vardi 1995). The version below is the one that stuck, essentially Barwise's.

> A group of $$n$$ children has been playing outside. Exactly $$k \geq 1$$ of them have mud on their foreheads. Each child sees every forehead except their own. Their father arrives and says, publicly: **"At least one of you has mud on your forehead."** He then asks, repeatedly: **"Do you know whether you are muddy? If so, step forward."** The children are honest, perceptive, perfect reasoners, and all of this is common knowledge. Nothing happens for a while. Then, at the $$k$$-th asking, all $$k$$ muddy children step forward at once.

The solution by induction is well known and I will formalize it in Section 3. What the formalization rewards is attention to three riddles buried in the story, and they organize this essay.

**Riddle 1: the uninformative announcement that changes everything.** If $$k \geq 2$$, every child can already see a muddy forehead. Each child therefore already knows the content of the father's announcement before he speaks. Yet the protocol provably goes nowhere without him (Proposition 3). Whatever the announcement contributes, it is not first-order information about the world. Section 2 measures exactly what it contributes: a climb from the $$(k-1)$$-th level of the "everyone knows that everyone knows" hierarchy to the top of it.

**Riddle 2: the silence that speaks.** No child transmits a single bit about any forehead. The only signals are rounds of "I do not know," that is, public records of ignorance. In Public Announcement Logic these silences are themselves announcements, and the last of them has a property that ordinary assertions lack: it is true at the moment it is made and false the moment it has been made. The children talk themselves out of ignorance by truthfully reporting it (Proposition 2). Section 4 places this inside the theory of *unsuccessful formulas*.

**Riddle 3: the trust that is doing all the work.** The protocol assumes the father is certainly truthful, perception is certainly accurate, and the rounds are certainly synchronized. Each "certainly" is load-bearing. Sections 6 and 7 replace certainty with mere trust, using plausibility models and the *radical upgrade* operator, and ask what survives. The answer is precise and, I think, the deepest thing the puzzle has to teach: the entire round-by-round structure survives at the level of belief (Theorem 2), and what changes is the failure mode. A false hard announcement deletes the actual world from the model, after which a further *true* announcement annihilates the model entirely; a false soft upgrade produces a wrong belief that one further truthful upgrade repairs (Proposition 5). Hard information buys certainty at the price of irreversibility. That is not a metaphor. It is a theorem about which worlds remain available to be believed in.

A note on method before we begin. Every formal claim below that is decidable on small models has been verified by exhaustive model checking, for all configurations of up to five children in the hard regime and four in the soft regime; the fourteen checks, labeled V1 through V13 with a two-part ninth, are catalogued in Appendix B alongside the verification script. Where I report a numbered Proposition or Theorem, the general statement is proved in Appendix A and the machine has confirmed every instance it can reach. The intended reader has seen propositional logic and is comfortable with notation, but I assume no prior exposure to modal or epistemic logic; everything needed is defined on the way.

## 2. The Static Picture: A Cube of Possible Worlds

Fix the set of children $$A = \{1, \dots, n\}$$ and one atomic proposition $$m_i$$ per child, read "child $$i$$ is muddy." A *possible world* is a complete settlement of these facts, so the world space is the set of bitstrings

$$
W \;=\; \{0,1\}^n,
$$

and I will write worlds as strings, $$110$$ for "children 1 and 2 muddy, child 3 clean," with $$\mathrm{wt}(w)$$ for the number of ones in $$w$$ (the Hamming weight, that is, how many children are muddy at $$w$$). Geometrically $$W$$ is the vertex set of the $$n$$-dimensional hypercube, and this geometry will do real work in a moment.

What a child knows is captured not by a list of facts but by a partition of $$W$$: the worlds the child cannot tell apart given what they see. Child $$i$$ sees every forehead except their own, so

$$
w \sim_i v \quad\text{iff}\quad w_j = v_j \ \text{for all } j \neq i .
$$

Each $$\sim_i$$-cell has exactly two elements, a world and its $$i$$-th bit-flip; on the cube, $$\sim_i$$ is the set of edges in direction $$i$$. The pair $$\mathcal{M}_0 = (W, \{\sim_i\}_{i \in A}, V)$$, with $$V$$ the obvious valuation, is the initial *epistemic model*. Because the relations are equivalence relations, the knowledge this model encodes is the standard S5 kind: truthful, introspective, closed under deduction. These idealizations are exactly the "perfect reasoners" clause of the story.

Truth at a world is defined as usual for the Boolean connectives, and knowledge quantifies over the cell:

$$
\mathcal{M}, w \models K_i \varphi \quad\text{iff}\quad \mathcal{M}, v \models \varphi \ \text{for every } v \sim_i w .
$$

Three group-level operators sit on top of $$K_i$$. *Everyone knows*: $$E\varphi = \bigwedge_{i \in A} K_i \varphi$$. Its iterates: $$E^0\varphi = \varphi$$ and $$E^{j+1}\varphi = E(E^j\varphi)$$, the hierarchy of "everyone knows that everyone knows that ... $$\varphi$$." And *common knowledge* $$C\varphi$$, which semantically says that $$\varphi$$ holds at every world reachable from the current one by any finite chain of $$\sim_i$$-steps, agents mixed freely. On finite models $$C\varphi$$ is the limit of the $$E^j\varphi$$ hierarchy; it is the fixed point the hierarchy is climbing toward, $$C\varphi \leftrightarrow E(\varphi \wedge C\varphi)$$.

On the cube these operators become geometry. A single $$K_i$$-step moves along one edge, so the worlds reachable in at most $$j$$ mixed steps form the Hamming ball of radius $$j$$: every world differing from the current one in at most $$j$$ coordinates. Hence

$$
\mathcal{M}_0, w \models E^j \varphi \quad\text{iff}\quad \varphi \ \text{holds throughout the Hamming ball of radius } j \ \text{around } w .
$$

Now let $$\varphi_0 = \bigvee_{i \in A} m_i$$ be the father's sentence, "at least one of you is muddy." In $$\mathcal{M}_0$$, $$\varphi_0$$ fails at exactly one vertex, the all-clean corner $$00\cdots0$$, and the distance from any world $$w$$ to that corner is $$\mathrm{wt}(w)$$. The entire higher-order structure of the puzzle's starting position falls out of that one observation.

**Proposition 1 (the announcement as a ladder).** *Let the actual world have weight $$k \geq 1$$. In $$\mathcal{M}_0$$: (i) $$E^j \varphi_0$$ holds at the actual world if and only if $$j \leq k - 1$$; (ii) $$C\varphi_0$$ fails; (iii) in the model obtained by publicly announcing $$\varphi_0$$, $$C\varphi_0$$ holds.* (Machine checks V2, V3; proof in Appendix A.)

Part (i) is the precise version of Riddle 1. With $$k$$ muddy children, the group already possesses the father's content to mutual depth $$k-1$$: everyone knows it as soon as $$k \geq 2$$, everyone knows that everyone knows it as soon as $$k \geq 3$$, and so on. What the group lacks is the $$k$$-th rung, because $$k$$ coordinated flips of the imagination suffice to reach the all-clean corner where the sentence fails. Each child can entertain a counterfactual self, who can entertain a counterfactual self, and $$k$$ nested counterfactuals deep there sits a possible world in which nobody is muddy and the sentence is unknown. The induction in Section 3 consumes exactly one rung of this ladder per round, which is why the protocol needs $$k$$ rungs and the group starts one short.

Part (iii) is what the father actually sells. His announcement deletes the single vertex $$00\cdots0$$, and with it every chain of nested doubts, of any depth, that bottomed out there. The sentence each child "already knew" becomes common knowledge, the whole infinite tower at once. This is why the announcement is simultaneously redundant at the first order and transformative at the higher orders: it adds no information about foreheads and maximal information about the group's information. Common knowledge here is not a rhetorical flourish but a measurable resource, and the father's one sentence is worth exactly the infinitely many levels above $$E^{k-1}$$.


## 3. Hard Information: Announcement as Model Surgery

Public Announcement Logic, introduced by Plaza (1989) and independently by Gerbrandy and Groeneveld (1997), treats a public, truthful, completely trusted announcement as an operation on models.[^pal-history] Announcing $$\varphi$$ in $$\mathcal{M}$$ produces the relativized model

$$
\mathcal{M}|_{\varphi} \;=\; \bigl(\, \{w \in W : \mathcal{M}, w \models \varphi\},\ \{\sim_i \cap\, (W_\varphi \times W_\varphi)\}_{i \in A},\ V|_{W_\varphi} \bigr),
$$

the original model with every $$\neg\varphi$$-world cut away. This is *hard* information: the excluded worlds are not demoted or doubted, they are gone, and nothing later in the logic can bring them back. The language adds a dynamic operator to match, $$[!\varphi]\psi$$, read "after a truthful public announcement of $$\varphi$$, $$\psi$$ holds," with semantics

$$
\mathcal{M}, w \models [!\varphi]\psi \quad\text{iff}\quad \mathcal{M}, w \models \varphi \ \text{implies}\ \mathcal{M}|_{\varphi}, w \models \psi .
$$

The conditional form encodes the truthfulness precondition: announcements of falsehoods are vacuously satisfied because they cannot lawfully occur. Keep an eye on that clause; Section 7 is about what happens when the world ignores it.

What makes PAL more than notation is that the dynamic operator can be compiled away. The *reduction axioms* push $$[!\varphi]$$ inward through every connective, the crucial one being the knowledge clause:

$$
[!\varphi] K_i \psi \;\leftrightarrow\; \bigl(\varphi \rightarrow K_i\, [!\varphi] \psi\bigr).
$$

Read aloud: knowing $$\psi$$ after the announcement is the same as knowing, conditionally on the announcement's truth, what the announcement will make true. Post-announcement knowledge is pre-encodable. Applied recursively, the axioms translate any PAL formula into a static epistemic one, so PAL is expressively equivalent to its base logic; the dynamics earn their keep in economy rather than reach. Lutz (2006) made the economy precise: PAL formulas can be exponentially more succinct than their static translations, yet satisfiability is no harder (PSPACE-complete with multiple agents). The balance changes once common knowledge enters the language: PAL with $$C$$ is strictly more expressive than epistemic logic with $$C$$, the reduction now runs through *relativized* common knowledge (van Benthem, van Eijck, and Kooi 2006), and satisfiability climbs to EXPTIME-complete (Lutz 2006). Since the muddy children are a story about common knowledge, the puzzle lives in the expensive fragment, which is part of why it feels deeper than its size.

### 3.1 The Protocol as a Sequence of Announcements

Two formulas drive the whole protocol. The father's seed:

$$
\varphi_0 \;=\; \bigvee_{i \in A} m_i ,
$$

and the round formula. When the father asks and nobody steps forward, the children jointly and publicly reveal their ignorance; under the story's common-knowledge-of-honesty assumptions, the silence is itself a truthful public announcement of

$$
\theta \;=\; \bigwedge_{i \in A} \bigl(\neg K_i m_i \,\wedge\, \neg K_i \neg m_i\bigr),
$$

"nobody knows whether they are muddy." No new channel is needed: in a synchronized round, the *absence* of a signal is a signal, fully public and fully informative. The run is then

$$
\mathcal{M}_1 = \mathcal{M}_0|_{\varphi_0}, \qquad \mathcal{M}_{j+1} = \mathcal{M}_j|_{\theta} \quad \text{for as long as } \theta \text{ is true at the actual world.}
$$

**Theorem 1 (layer dynamics and round counting).** *Let the actual world have weight $$k \geq 1$$. Then for $$1 \leq j \leq k$$,*

$$
\mathcal{M}_j \;=\; \{\, w \in W : \mathrm{wt}(w) \geq j \,\},
$$

*each ignorance announcement shaving off exactly one layer of the cube. The formula $$\theta$$ is true at the actual world in $$\mathcal{M}_1, \dots, \mathcal{M}_{k-1}$$ and false in $$\mathcal{M}_k$$, so exactly $$k-1$$ ignorance rounds occur after the father speaks. In $$\mathcal{M}_k$$ every muddy child knows they are muddy, $$K_i m_i$$, and they are the first to know anything about themselves; at the actual world, no child knows their own status in any earlier model.* (Machine check V1, all $$1 \leq k \leq n \leq 5$$; proof in Appendix A.)

The round arithmetic matches the story exactly. The father's question at asking $$j$$ finds the group in $$\mathcal{M}_j$$; for $$j < k$$ the answer is silence, announcing $$\theta$$ and producing $$\mathcal{M}_{j+1}$$; at asking $$k$$ the muddy children step forward. The mechanism is the one from Proposition 1 in motion: in $$\mathcal{M}_j$$ the lightest surviving worlds have weight $$j$$, and a muddy child at such a world sees only $$j-1$$ muddy faces, deduces from the model that their own forehead must carry the missing mud, and would know. When no one knows, every weight-$$j$$ world is refuted, and the boundary of ignorance advances one layer. Common knowledge of $$\varphi_0$$ set the floor; each public silence raises it by one.

A worked instance keeps this honest. Take $$n = 3$$, $$k = 2$$, actual world $$110$$ (children 1 and 2 muddy). The machine-generated trace (check V1, Table A of the verification script):

| Stage | Worlds remaining | $$\theta$$ at $$110$$ | Who knows their own status |
|---|---|---|---|
| $$\mathcal{M}_0$$ | $$000, 001, 010, 011, 100, 101, 110, 111$$ | true | nobody |
| $$\mathcal{M}_1 = \mathcal{M}_0\vert_{\varphi_0}$$ | $$001, 010, 011, 100, 101, 110, 111$$ | true | nobody |
| $$\mathcal{M}_2 = \mathcal{M}_1\vert_{\theta}$$ | $$011, 101, 110, 111$$ | false | children 1 and 2: $$K_i m_i$$ |

Follow child 1 through it. In $$\mathcal{M}_1$$ she sees mud on 2 and a clean 3, so her cell is $$\{110, 010\}$$: she might be clean. But in the hypothetical world $$010$$, child 2 would see two clean faces, and the father's now-common announcement would force child 2 to conclude $$m_2$$ on the spot. Child 2 stays silent through round 1; silence announces $$\theta$$; $$\theta$$ is false at $$010$$; the world $$010$$ is surgically removed. In $$\mathcal{M}_2$$ child 1's cell is $$\{110, 111\}$$, and $$m_1$$ holds in both. She knows. The reasoning is symmetric for child 2, and the two step forward together at asking 2.

Two refinements that the formalization surfaces and the folklore version blurs. First, the ignorance formula could be read more weakly as "nobody knows that they are muddy," $$\bigwedge_i \neg K_i m_i$$, dropping the "whether." Along this protocol the two readings generate identical model sequences, because no child ever comes to know they are *clean* at any world of any model in the run (check V5); the asymmetry is built into the geometry, where announcements only ever shave the cube from below, and a child learns cleanliness only if their muddy twin is deleted, which layer-by-layer shaving never does before the run ends. Second, the story traditionally ends when the muddy children step forward, but at that moment the clean children still do not know their own status; in $$\mathcal{M}_k$$ a clean child's cell still contains a heavier twin. Their knowledge arrives one beat later, when the muddy children's public "I know" (and the others' continued silence) is itself processed as an announcement, after which every clean child knows they are clean (check V7). The protocol does not merely identify the muddy; run one round past the famous ending and it classifies everyone.

[^pal-history]: Gerbrandy's (1999) dissertation is the fullest early development of the announcement idea. The modern, fully general framework, with announcements as one instance of arbitrary epistemic *actions* (private messages, suspicions, lies), is due to Baltag, Moss, and Solecki (1998) and Baltag and Moss (2004); the textbook treatment is van Ditmarsch, van der Hoek, and Kooi (2008). This essay needs only the public fragment.


## 4. The Sentence That Refutes Itself

Riddle 2 deserves its own section because it marks the spot where PAL stops being a bookkeeping device and starts being philosophy. In ordinary logic, learning that $$\varphi$$ leaves $$\varphi$$ true; information is information *about* a world that sits still. Epistemic facts do not sit still. The act of announcing them is an event in the very domain they describe, and some true sentences cannot survive their own publication.

The classic specimen is the Moore sentence, $$p \wedge \neg K_i p$$: "it is raining and you do not know it." Said to the right person at the right time it is true, yet the moment it lands, the hearer knows about the rain and the second conjunct dies. PAL turns this from a curiosity into a classification. Call $$\varphi$$ a *successful formula* when $$[!\varphi]\varphi$$ is valid, that is, when announcing it always leaves it true, and *unsuccessful* otherwise (van Ditmarsch and Kooi 2006). Purely factual sentences are successful; so is everything in the *positive fragment*, formulas built from literals, conjunction, disjunction, $$K_i$$, and $$C$$ without negations wrapping knowledge. The father's $$\varphi_0$$ is positive, and accordingly survives: after his announcement, $$\varphi_0$$ is not merely true but common knowledge, permanently (check V6, second half). Unsuccessful formulas are the interesting residue, and Moore sentences are their simplest generators.

The muddy children's final silence is precisely such a residue, in group form.

**Proposition 2 (the last silence destroys itself).** *Let $$k \geq 2$$. Along the run of Theorem 1, the ignorance formula $$\theta$$ is true at the actual world when announced in each of $$\mathcal{M}_1, \dots, \mathcal{M}_{k-1}$$, and its final announcement makes it false: $$\mathcal{M}_{k-1} \models_{\text{actual}} \theta$$ while $$\mathcal{M}_k \models_{\text{actual}} \neg\theta$$. Equivalently, $$\langle !\theta\rangle \neg\theta$$ holds at the actual world of $$\mathcal{M}_{k-1}$$.* (Machine check V6.)

There is something almost thermodynamic about it. Each round, the children truthfully pool their ignorance, and the pooled ignorance is consumed as fuel: the announcement that nobody knows is exactly what makes somebody know. The protocol terminates not because the information runs out but because the *meta*-information runs out, the last truthful utterance of $$\theta$$ being the one that renders $$\theta$$ unutterable. Notice the fine structure: announced in $$\mathcal{M}_1$$ through $$\mathcal{M}_{k-2}$$, $$\theta$$ is still true afterward, so the very same sentence yields a *successful update* in the early rounds and an unsuccessful one only at the boundary, an observation van Ditmarsch and Kooi (2006) make about exactly this puzzle. The formula $$\theta$$ is unsuccessful as a formula, since one announcement of it can falsify it; whether a given utterance of it succeeds is an interaction between the sentence and the epistemic state it strikes.

Two pointers for the reader who wants the general theory. Holliday and Icard (2010) characterize exactly which single-agent S5 formulas are successful, a question that stayed open for two decades after Plaza posed the logic. And the dual question, which truths *can* be known after some announcement, connects this nursery puzzle to Fitch's paradox of knowability; Balbiani et al. (2008) develop the logic in which "knowable" literally means "known after an announcement." The muddy children sit at the friendly end of a genuinely deep corridor: the puzzle's charm is that a children's story walks you, in $$k$$ steps, into the part of logic where saying and knowing interfere.


## 5. What the Protocol Is Silently Assuming

The clean machinery of Sections 2 through 4 runs on assumptions that the story smuggles in as atmosphere. Making them explicit is not pedantry; each one, removed, breaks the protocol in a characteristic way, and the breakage patterns are the bridge to the second half of this essay.

**The seed is necessary.** Riddle 1 promised a proof that the father is indispensable, and it is one line long.

**Proposition 3 (no seed, no progress).** *In $$\mathcal{M}_0$$, the ignorance formula $$\theta$$ is true at every world. Announcing it therefore removes nothing: $$\mathcal{M}_0\vert_{\theta} = \mathcal{M}_0$$, and the same holds for every iterate. Without the father's announcement, the children can broadcast their ignorance forever and the model never moves.* (Machine check V4.)

The point generalizes into a slogan: iterated announcements need an asymmetry to amplify. In the pristine cube every child's ignorance is consistent with every world, so the public record of that ignorance excludes nothing; the father's deletion of one corner is what first makes some ignorance *informative*, by creating worlds (the weight-one layer) at which somebody would no longer be ignorant. Every subsequent round amplifies the asymmetry one layer further. The announcement is a symmetry-breaking event, and the cascade is the asymmetry propagating.

**Synchrony and simultaneity.** The silence-as-announcement reading requires rounds: a commonly known clock such that "nobody has stepped forward *by now*" is well defined and public. If answers dribble out asynchronously, or if a child can answer late, the formula announced by silence is no longer $$\theta$$ and the layer dynamics derail. Moses, Dolev, and Halpern (1986) built a small genre out of such failure modes, with synchronous and asynchronous wives, faulty messengers, and protocols that work only on Sundays; the uncomfortably durable lesson of "Cheating Husbands and Other Stories" is that the puzzle's solution is a property of the *communication regime*, not of the participants' intelligence. Perfect reasoners with a slightly wrong protocol step forward on the wrong day, in provably wrong ways.

**Truthfulness, perception, and the protocol itself must be common knowledge.** It is not enough that everyone is honest and sharp-eyed; everyone must know this, and know that everyone knows it, to every depth, or the nested counterfactuals that drive Theorem 1's induction lose their footing. A child who merely suspects that another child might miscount foreheads cannot run the argument "if I were clean, she would have known by now." The S5 idealization quietly carries all of this.

It is worth pausing on how expensive these assumptions are outside the nursery, because their price is a celebrated theorem. Halpern and Moses (1990) proved that common knowledge of a new fact cannot be attained over a communication channel that can lose or delay messages, however many acknowledgments are exchanged; this is the epistemic content of the coordinated attack problem, two generals on two hills forever one confirmation short of certainty. Rubinstein (1989) sharpened the point from the economic side: in his electronic mail game, players who have exchanged a large but finite number of acknowledgments, achieving $$E^{j}$$ for enormous $$j$$ but not $$C$$, behave like players who share no information at all, so "almost common knowledge" is behaviorally discontinuous from the real thing. And Aumann (1976) had already shown the strange power of the genuine article, with common priors and common knowledge of posteriors forcing agreement. Against this backdrop, the father is revealed as an exotic piece of infrastructure: a zero-noise broadcast channel with built-in common knowledge of its own reliability. The puzzle works because the story grants, for free, exactly the resource that the theorems say is unobtainable under realistic communication.

So the natural next question is not a variant but an inversion. Keep the protocol; weaken the channel. What survives if the children do not *know* the father is right, but merely *trust* him, and trust each other's reports, as defeasible evidence? That question needs a logic in which information can be strong without being irrevocable, and that is where the original course paper, and this essay, turn to soft information.


## 6. Soft Information: When Trust Replaces Certainty

Hard information eliminates; soft information *reorders*. The semantic home for the latter is the epistemic plausibility model of Baltag and Smets (2008), which dresses the epistemic model of Section 2 with one extra piece of structure:

$$
\mathcal{P} \;=\; \bigl(W,\ \{\sim_i\}_{i \in A},\ \leq,\ V\bigr),
$$

where $$\leq$$ is a total preorder on $$W$$, read "$$w \leq v$$ iff $$w$$ is at least as plausible as $$v$$." I will present $$\leq$$ through a rank function $$\kappa: W \to \mathbb{N}$$, with $$\kappa(w) = 0$$ for the most plausible worlds and higher ranks for the more far-fetched, so $$w \leq v$$ iff $$\kappa(w) \leq \kappa(v)$$. One modeling choice deserves flagging: I use a single plausibility order shared by all agents, rather than one order per agent. For this puzzle nothing is lost, because every signal in the protocol is public and strikes all agents identically, so their plausibility orders, if initially common, remain common; the agents differ only in their hard partitions $$\sim_i$$.[^common-prior]

The hard notions survive unchanged: $$K_i \varphi$$ still quantifies over the whole cell $$[w]_{\sim_i}$$, and is *irrevocable*, immune to anything that merely reorders. The new notion is graded. An agent *believes* what holds in the most plausible candidates among their hard possibilities:

$$
\mathcal{P}, w \models B_i \varphi \quad\text{iff}\quad \varphi \ \text{holds at every } \leq\text{-minimal world of } [w]_{\sim_i}.
$$

Belief, unlike knowledge, can be false: nothing forces the actual world to be among the minimal ones. Between fallible belief and irrevocable knowledge, two intermediate attitudes will matter at the punchline. Agent $$i$$ has *safe belief* in $$\varphi$$ at $$w$$ when $$\varphi$$ holds at every world of $$[w]_{\sim_i}$$ that is at least as plausible as $$w$$ itself (Stalnaker 2006; Baltag and Smets 2008): belief that would survive any truthful new evidence, since truthful inputs never demote the actual world below worlds it already dominates. And $$i$$ has *strong belief* in $$\varphi$$ when $$\varphi$$ is consistent with $$i$$'s hard information and every $$\varphi$$-world in the cell is strictly more plausible than every $$\neg\varphi$$-world: belief held with maximal entrenchment, surrendered only if the evidence contradicts $$\varphi$$ outright. Knowledge implies both; both imply belief; neither implies the other in general. The ladder gives us a vocabulary for *how* an agent holds a conviction, which hard semantics, with its binary know-or-not, cannot articulate.

Soft announcements act on $$\kappa$$ and leave $$W$$ alone. The operator the original paper invoked is the *radical upgrade* (also called lexicographic upgrade) of van Benthem (2007):

$$
\Uparrow\!\varphi: \quad \text{all } \varphi\text{-worlds become strictly more plausible than all } \neg\varphi\text{-worlds; within each zone, the old order is kept.}
$$

In rank form: sort worlds by the pair (does $$w$$ falsify $$\varphi$$?, old rank) and re-rank densely. The definition is worth stating with care because it is easy to mangle into circularity, defining the new order by cases that mention the new order; the original version of this essay did exactly that, and the zone formulation above is the repair. A gentler cousin, the *conservative upgrade* $$\uparrow\!\varphi$$, promotes only the *best* $$\varphi$$-worlds to the top and leaves all other comparisons untouched. Radical upgrade is the policy of an agent who treats the source as strongly trustworthy though not infallible; conservative upgrade, barely-trusting acceptance. Hard announcement $$!\varphi$$ sits at the limit of the scale: trust so total that disconfirming worlds are not demoted but destroyed.

### 6.1 The Soft Muddy Children

Now replay the protocol with trust in place of certainty. The father is regarded as highly reliable but not as an oracle: his announcement triggers $$\Uparrow\!\varphi_0$$. The children's round signals are likewise soft, and honesty about one's own state now means honesty about *belief*, so the silence of a round announces the doxastic ignorance formula

$$
\theta^B \;=\; \bigwedge_{i \in A}\bigl(\neg B_i m_i \,\wedge\, \neg B_i \neg m_i\bigr),
$$

"nobody has yet formed an opinion about their own forehead," and is processed as $$\Uparrow\!\theta^B$$. Start from the flat prior $$\kappa_0 \equiv 0$$ on the full cube, run $$\Uparrow\!\varphi_0$$, then $$\Uparrow\!\theta^B$$ for as long as $$\theta^B$$ remains true at the actual world. The dynamics admit a closed form.

**Theorem 2 (the soft mirror).** *Let the actual world have weight $$k \geq 1$$, and let $$\kappa_s$$ denote the rank function after stage $$s$$ (stage 1 being the father's upgrade, stage $$s+1$$ the $$s$$-th ignorance upgrade). Then for every world $$w$$ and every stage $$s \leq k$$,*

$$
\kappa_s(w) \;=\; \max\bigl(0,\ s - \mathrm{wt}(w)\bigr),
$$

*the run lasts exactly as long as the hard run, with $$k-1$$ ignorance upgrades, and at stage $$k$$ every muddy child $$i$$ truly believes they are muddy, $$B_i m_i$$, indeed with strong belief and with safe belief, while still lacking knowledge: $$\neg K_i m_i$$. No clean child ever believes they are muddy at any stage.* (Machine checks V9 and V9b; proof in Appendix A.)

Read the rank formula geometrically and the hard run reappears inside it: the set $$\{w : \kappa_s(w) = 0\}$$ of maximally plausible worlds is exactly $$\{w : \mathrm{wt}(w) \geq s\}$$, the surviving model $$\mathcal{M}_s$$ of Theorem 1. Soft dynamics do not delete the lower layers of the cube; they let them sink, one rank per round, preserving the full record of how implausible each world has become. The concrete trace for $$n = k = 3$$ (machine output, Table B of the script):

| World(s) | $$\mathrm{wt}$$ | $$\kappa_0$$ | $$\kappa_1$$ | $$\kappa_2$$ | $$\kappa_3$$ |
|---|---|---|---|---|---|
| $$111$$ | 3 | 0 | 0 | 0 | 0 |
| $$011, 101, 110$$ | 2 | 0 | 0 | 0 | 1 |
| $$001, 010, 100$$ | 1 | 0 | 0 | 1 | 2 |
| $$000$$ | 0 | 0 | 1 | 2 | 3 |

At stage 3, child 1's cell at the actual world $$111$$ is $$\{111, 011\}$$, with ranks $$0$$ and $$1$$: the unique most plausible candidate says she is muddy, so $$B_1 m_1$$, and since the $$m_1$$-world strictly dominates the $$\neg m_1$$-world in her cell, the belief is strong, and since it holds at every world at least as plausible as the actual one, it is safe. What she does not have is $$K_1 m_1$$: the world $$011$$ remains epistemically possible, merely discredited. Here the original course paper both erred and saw something true. Its error was the claim that *every* child ends up believing themselves muddy, which is false and would be disastrous if true, since clean children would then hold false beliefs under a truthful protocol; the machine check that killed this claim took milliseconds, and the correct statement is the asymmetric one above. What it got right, better than it knew, was the phrase "strong beliefs": the terminal attitude of the muddy children is strong belief in the exact technical sense of Baltag and Smets, and safe belief in the exact technical sense of Stalnaker, the two most robust doxastic attitudes short of knowledge itself. The protocol delivers, so to speak, everything that trust can deliver: a conviction that no future truthful evidence can dislodge, resting one grade below certainty.

The clean children, as in the hard run, are classified one beat later: when the muddy children publicly report their belief and the clean ones their continued agnosticism, one further upgrade $$\Uparrow$$(reports) gives every clean child the true belief $$B_j \neg m_j$$ (check V10).

One more structural fact falls out of the rank formula, answering a question the hard semantics cannot even pose: does it matter *how much* the children trust each other's silences?

**Proposition 4 (trust intensity is irrelevant here).** *Along the soft muddy run, radical and conservative upgrades generate identical rank sequences: replacing every $$\Uparrow$$ by $$\uparrow$$ changes nothing.* (Machine check V12; proof in Appendix A.)

The reason is visible in the table: at every stage, the formula being upgraded is true exactly on the current rank-zero zone's upper part, in fact on an up-set of worlds all already tied at rank zero, so "promote all $$\varphi$$-worlds above everything" and "promote the best $$\varphi$$-worlds" pick out the same move. The protocol is self-calibrating: its announcements always arrive pre-sorted, targeting worlds already at the top of the plausibility order. This is a luxury of the puzzle's pristine information flow, and the next section is about losing it.

[^common-prior]: The general framework with agent-indexed plausibility orders, conditional belief operators $$B_i^{\psi}$$, and the full dynamic logic of upgrades is developed in Baltag and Smets (2008) and van Benthem (2007, 2011, ch. 7). The soft-information reading of the muddy children, with announcements as upgrades rather than eliminations, is treated by Baltag and Smets (2009), which is the natural companion to this section.


## 7. Error and Recovery: What Certainty Costs

Everything so far assumed the announcements were true. The deepest difference between hard and soft information only shows when that assumption fails, and the puzzle furnishes a brutally clean test case: let nobody be muddy, actual world $$00\cdots0$$, and let the father, misreading the situation or testing his children, announce $$\varphi_0$$ anyway.

**Proposition 5 (graceful degradation versus epistemic bankruptcy).** *Take $$n = 3$$ and actual world $$000$$. (i) Hard regime: announcing $$\varphi_0$$ deletes the actual world from the model; if the children subsequently receive the truthful announcement "nobody is muddy," the model becomes empty, and no further announcement of any kind is defined on it. (ii) Soft regime: $$\Uparrow\!\varphi_0$$ leads every child to the false belief $$B_i m_i$$; a single truthful upgrade $$\Uparrow$$"nobody is muddy" restores the true beliefs $$B_i \neg m_i$$ for all $$i$$.* (Machine checks V8 and V11.)

The machine trace for the soft branch (Table C of the script):

| Step | Rank state | Beliefs at the actual world $$000$$ |
|---|---|---|
| start | all worlds rank $$0$$ | none |
| after $$\Uparrow\!\varphi_0$$ (false input) | $$000$$ demoted to rank $$1$$ | $$B_1 m_1$$, $$B_2 m_2$$, $$B_3 m_3$$ |
| after $$\Uparrow$$"nobody is muddy" (true input) | $$000$$ back to rank $$0$$ | $$B_1 \neg m_1$$, $$B_2 \neg m_2$$, $$B_3 \neg m_3$$ |

The middle row repays a careful look, because the error it records is not noise but *reasoning*, executed flawlessly on a corrupted premise. After the father's false announcement, each child surveys the others, sees no mud anywhere, and runs the base case of the famous induction: someone is muddy, it is nobody I can see, therefore it is me. All three step forward at the first asking, in perfect synchrony, each privately certain, all wrong. The puzzle's celebrated inference engine has no integrity check on its inputs; feed it a false seed and it cascades to false conclusions with exactly the elegance it brings to true ones. What the soft regime buys is not immunity from this, nothing buys that, but *reversibility*: the actual world was demoted, not destroyed, so it is still present in the model to be re-promoted when better evidence arrives, and one truthful upgrade suffices.

The hard branch of Proposition 5 is the same story with the safety removed, and it is worth dwelling on what "the model becomes empty" means. After the false $$!\varphi_0$$, the actual world is gone; the children's representable possibilities no longer include reality. They are not yet incoherent, their model still supports beliefs, all of them false, but they are now structurally incapable of being corrected, because the correction is a sentence true only at a world they have eliminated. When the truthful "nobody is muddy" arrives, it intersects an actuality-free model with a set of worlds disjoint from it, and the result is the empty model, on which knowledge, belief, and announcement are all undefined. Two announcements, one false and one true, and the agents have reasoned themselves out of existence. PAL's truthfulness precondition, the innocuous-looking $$\varphi \rightarrow$$ clause of Section 3, is revealed as load-bearing infrastructure: hard update is sound only inside a system that *guarantees* its inputs, and the guarantee is not a formality but the entire warrant for the irreversible surgery. Eliminativity is what made knowledge, rather than mere belief, achievable in Theorem 1; eliminativity is what makes a single false input unrecoverable here. One mechanism, both edges. Certainty and fragility are not two properties that happen to co-occur in the hard regime; they are the same property, described from the inside and from the outside.

### 7.1 Does Soft Iteration Always Settle?

One last honesty check before the comparison is allowed to stand. Hard iteration is guaranteed to stabilize: each announcement weakly shrinks a finite model, so repetition reaches a fixed point, a fact van Benthem (2011) develops into a small theory of self-fulfilling and self-refuting statements. Soft iteration enjoys no such guarantee, because reordering, unlike deletion, is not monotone. The verification script contains a minimal demonstration (check V13): one agent, two indistinguishable worlds $$\{w_p, w_{\bar p}\}$$, and the doxastic Moore input $$\chi = (p \wedge \neg B p) \vee (\neg p \wedge B p)$$, "I am wrong about $$p$$." Iterating $$\Uparrow\!\chi$$ from the flat order makes the rank state cycle with period two, forever: each upgrade makes the agent believe whichever world the formula just endorsed, which flips the formula's extension, which flips it back. In our toy the truth of $$\chi$$ at the actual world alternates, so a *truthful* protocol halts after one step; but Baltag and Smets (2009) construct genuinely truthful iterated upgrades that oscillate forever, map the general landscape of fixed points and cycles of joint upgrades, and in companion work (Baltag and Smets 2011) give conditions under which iterated truthful soft announcements are guaranteed to converge to true belief. Against that landscape, Theorem 2 carries a quiet extra claim: the soft muddy protocol's termination at stage $$k$$ is not a courtesy of the genre but a theorem about this particular formula on this particular cube. Good behavior under iteration is something soft dynamics must *prove*, case by case, where hard dynamics gets it free, and the muddy children pass the test.


## 8. Coda: From the Nursery to the Protocol Stack

Strip the mud off and the puzzle is a specification problem: a group must reach coordinated, justified conclusions using only public signals over a channel with known properties, and the question is what epistemic state each channel can support. That problem is permanent, and the puzzle's two regimes are its two canonical answers.

Distributed computing learned this in the puzzle's own vocabulary. Halpern and Moses (1990) showed that protocols requiring simultaneous coordinated action require common knowledge, that common knowledge is unattainable over channels that can lose or delay messages, and that system designers therefore face a structural choice: engineer a channel strong enough to behave like the father, a synchronous trusted broadcast, or weaken the epistemic target to something attainable, one of the approximations of common knowledge their paper catalogues. Reading their theorem next to Theorem 1 and Proposition 5 sharpens it into a procurement decision. A hard channel delivers knowledge in $$k$$ rounds and deletes reality on its first false input; it should be bought only with a correctness guarantee attached. A soft channel delivers, in the same $$k$$ rounds, strong and safe belief, the best attitudes short of knowledge, and repairs a false input in one round. The puzzle does not tell you which to choose. It tells you the exact price of each, which is better.

The same ledger reads directly onto multi-agent AI systems, and I will keep this paragraph to commentary rather than citation, since the engineering folklore is moving faster than its literature. A team of model-based agents coordinating through a shared transcript is running a public announcement protocol: the shared context is the father's channel, and whatever enters it is, by default, hard, eliminated alternatives do not return. The muddy children analysis says that this default is a design decision with a failure mode attached, and that the decision should be made per channel, not globally. Verified tool outputs, cryptographic attestations, compiler errors: these have the correctness guarantee that licenses hard update. Another agent's summary, a retrieved document, a model's own chain of reasoning: these are testimony, and testimony earns at most a radical upgrade, however confident its tone. An architecture that treats testimony as hard will be fast, decisive, and one hallucinated premise away from a cascade it cannot revise, all three children stepping forward at once, certain and wrong, with the actual world no longer represented anywhere in the system. The fix is not less trust but typed trust: keep the worlds, sink them.

I will end on the method rather than the moral. The original course paper contained a claim, that every child ends up believing themselves muddy, that reads plausibly, sat unchallenged through grading, and is false; a model checker of a few hundred lines refuted it in milliseconds and supplied the correct asymmetric statement, which turned out to be more interesting than the error. Epistemic logic is unusually friendly to this discipline, since its small models are exhaustively checkable, but the lesson is not local to logic. Claims about systems should be run, not just written. The muddy children would approve: they are, after all, the original demonstration that the cheapest way to find out the truth about yourself is to let your reasoning be checked in public.


---

## Appendix A. Proofs

**Proposition 1.** Unfolding the semantics, $$E^j\varphi$$ holds at $$w$$ if and only if $$\varphi$$ holds at every world reachable from $$w$$ by at most $$j$$ steps, each step staying inside some agent's $$\sim_i$$-cell. In $$\mathcal{M}_0$$ a $$\sim_i$$-step either stays put or flips coordinate $$i$$, so the reachable set in at most $$j$$ steps is exactly the Hamming ball of radius $$j$$ around $$w$$. The formula $$\varphi_0$$ fails at the single world $$00\cdots0$$, whose Hamming distance from $$w$$ is $$\mathrm{wt}(w) = k$$. Hence $$E^j\varphi_0$$ holds at the actual world iff $$k > j$$, which is (i). For (ii), the union of the relations connects the whole cube, so the $$C$$-reachable set from any world contains $$00\cdots0$$, where $$\varphi_0$$ fails. For (iii), in $$\mathcal{M}_1 = \mathcal{M}_0\vert_{\varphi_0}$$ the formula $$\varphi_0$$ holds at every world, hence throughout every reachable set. $$\blacksquare$$

**Theorem 1.** By induction on $$j$$ we show $$\mathcal{M}_j = \{w : \mathrm{wt}(w) \geq j\}$$ for $$1 \leq j \leq k$$. Base: $$\mathcal{M}_1$$ is the cube minus the unique weight-$$0$$ world. Step: assume the claim for $$j < k$$ and evaluate $$\theta$$ at $$w \in \mathcal{M}_j$$. Child $$i$$'s cell at $$w$$ in $$\mathcal{M}_j$$ is $$\{w, w^{(i)}\} \cap \mathcal{M}_j$$, where $$w^{(i)}$$ is $$w$$ with bit $$i$$ flipped. If $$\mathrm{wt}(w) = j$$, pick a muddy child $$i$$ at $$w$$ (one exists, $$j \geq 1$$): the twin $$w^{(i)}$$ has weight $$j-1$$ and has been deleted, the cell collapses to $$\{w\}$$, and $$K_i m_i$$ holds, so $$\theta$$ fails at $$w$$. If $$\mathrm{wt}(w) > j$$, then for every child the twin survives, since flipping changes weight by one and both $$\mathrm{wt}(w)$$, $$\mathrm{wt}(w) \pm 1 \geq j$$; every cell is a two-element set whose members disagree on $$m_i$$, so no child knows their own status and $$\theta$$ holds at $$w$$. Thus $$\theta$$ fails exactly on the weight-$$j$$ layer, and $$\mathcal{M}_{j+1} = \{w : \mathrm{wt}(w) \geq j+1\}$$. The actual world has weight $$k$$, so $$\theta$$ is true there in $$\mathcal{M}_1, \dots, \mathcal{M}_{k-1}$$ and, by the layer-$$k$$ case of the computation just made, false in $$\mathcal{M}_k$$: exactly $$k-1$$ ignorance rounds occur. In $$\mathcal{M}_k$$ the actual world lies on the lightest layer, so every muddy child's cell is a singleton, giving $$K_i m_i$$, while every clean child's heavier twin survives, so the clean still do not know. Finally, no child ever knows they are clean at any world of any $$\mathcal{M}_j$$: that would require the deletion of the heavier muddy twin, and the run deletes only from below. $$\blacksquare$$

**Theorem 2.** By induction on the stage $$s$$ we show $$\kappa_s(w) = \max(0, s - \mathrm{wt}(w))$$. The flat start is the case $$s = 0$$. For the father's stage, the extension of $$\varphi_0$$ is $$\{w : \mathrm{wt}(w) \geq 1\}$$, all worlds are at rank $$0$$, and $$\Uparrow$$ leaves the extension at rank $$0$$ while demoting the single weight-$$0$$ world to rank $$1$$, which is $$\max(0, 1 - \mathrm{wt})$$. For the inductive step, assume the formula at stage $$s$$ with $$1 \leq s < k$$ and compute beliefs in $$\kappa_s$$. Child $$i$$'s cell at $$w$$ is the full pair $$\{w, w^{(i)}\}$$, soft dynamics deleting nothing. If $$w_i = 1$$: the twin is one weight lighter, so $$\kappa_s(w^{(i)}) = \max(0, s - \mathrm{wt}(w) + 1)$$, which strictly exceeds $$\kappa_s(w)$$ exactly when $$\mathrm{wt}(w) \leq s$$; in that case the unique most plausible world of the cell is $$w$$ and $$B_i m_i$$ holds at $$w$$; otherwise the cell is tied and $$i$$ has no opinion. If $$w_i = 0$$: the twin is one weight heavier, and a strict comparison, now favoring the muddy twin, occurs exactly when $$\mathrm{wt}(w) \leq s - 1$$, in which case $$B_i m_i$$ holds at $$w$$; otherwise no opinion. Collecting cases, some child holds an opinion at $$w$$ iff $$\mathrm{wt}(w) \leq s$$, so the extension of $$\theta^B$$ at stage $$s$$ is $$\{w : \mathrm{wt}(w) \geq s + 1\}$$, a set lying entirely at rank $$0$$. Applying $$\Uparrow$$: the extension stays at rank $$0$$; the complement, whose stage-$$s$$ ranks were $$s - \mathrm{wt}(w) \in \{0, \dots, s\}$$, is demoted en bloc with its internal order preserved, giving $$\kappa_{s+1}(w) = (s - \mathrm{wt}(w)) + 1 = \max(0, s + 1 - \mathrm{wt}(w))$$ there. The closed form propagates. The formula $$\theta^B$$ is true at the actual world (weight $$k$$) iff $$k \geq s + 1$$, so the upgrades run through stage $$k$$ and halt, with $$k - 1$$ ignorance upgrades, matching the hard count. At stage $$k$$, a muddy child $$i$$'s cell at the actual world is $$\{a, a^{(i)}\}$$ with ranks $$0$$ and $$1$$: belief in $$m_i$$, strong because the unique $$m_i$$-world of the cell strictly dominates the unique $$\neg m_i$$-world, safe because the only cell-world at least as plausible as $$a$$ is $$a$$ itself, and not knowledge because $$a^{(i)}$$ remains in the cell. A clean child $$j$$'s twin has weight $$k + 1$$, hence rank $$0$$ at every stage $$s \leq k$$; the cell stays tied and $$j$$ never forms a belief about their own forehead, in particular never the false belief $$B_j m_j$$. $$\blacksquare$$

**Proposition 4.** The proof of Theorem 2 shows that at every stage the upgraded formula's extension consists exclusively of worlds at the current minimal rank. The conservative upgrade promotes the most plausible worlds of the extension; when the whole extension is already tied at the minimum, that is the whole extension, and $$\uparrow$$ performs the identical reordering to $$\Uparrow$$. This holds at the father's stage and at every ignorance stage, so the two rank sequences coincide. $$\blacksquare$$

**Propositions 2, 3, 5.** These are finite computations contained in, or directly adjacent to, the proofs above. For Proposition 2: by Theorem 1, $$\theta$$ holds at the actual world in $$\mathcal{M}_{k-1}$$ and fails on the weight-$$k$$ layer of $$\mathcal{M}_k$$, which contains the actual world. For Proposition 3: in $$\mathcal{M}_0$$ every cell of every child is a two-element pair disagreeing on that child's atom, so $$\theta$$ holds universally and relativization is the identity. For Proposition 5: the two-step traces are printed by the verification script and reproduced as Table C; the hard branch empties the model because the worlds satisfying "nobody is muddy" and the worlds surviving $$!\varphi_0$$ are disjoint sets. $$\blacksquare$$


## Appendix B. The Verification Catalog

Every checkable claim in this essay is exercised by the companion script `muddy_del_verify.py` (about 400 lines of dependency-free Python). It implements S5 models over $$\{0,1\}^n$$ with PAL update, $$E^j$$ and $$C$$ checking by reachability, and epistemic plausibility models with joint radical and conservative upgrades; belief is evaluated as truth at the most plausible worlds of the agent's cell. Hard-regime claims are checked exhaustively for all $$1 \leq k \leq n \leq 5$$, soft-regime claims for all $$1 \leq k \leq n \leq 4$$. Running `python3 muddy_del_verify.py` prints the table data used in Sections 3, 6, and 7 and exits with status 0 only if every check passes. The fourteen checks:

| Check | Claim verified | Used in |
|---|---|---|
| V1 | $$\mathcal{M}_j = \{\mathrm{wt} \geq j\}$$; muddy children first satisfy $$K_i m_i$$ at stage $$k$$; $$k-1$$ ignorance rounds | Theorem 1 |
| V2 | In $$\mathcal{M}_0$$: $$E^j\varphi_0$$ at the actual world iff $$j \leq k-1$$; $$C\varphi_0$$ fails; $$C\varphi_0$$ holds in $$\mathcal{M}_1$$ | Proposition 1 |
| V3 | $$E\varphi_0$$ in $$\mathcal{M}_0$$ iff $$k \geq 2$$: the announcement is first-order uninformative | Riddle 1, Proposition 1 |
| V4 | Without the seed, $$\theta$$ is universal and $$\mathcal{M}_0\vert_\theta = \mathcal{M}_0$$ | Proposition 3 |
| V5 | $$K_i\neg m_i$$ never holds along the run; "know that" and "know whether" ignorance give identical model sequences | Section 3.1 |
| V6 | $$\langle!\theta\rangle\neg\theta$$ at the last round; the father's $$\varphi_0$$ is successful | Proposition 2 |
| V7 | After the muddy children's public "I know," every clean child knows they are clean | Section 3.1 |
| V8 | A false hard announcement eliminates the actual world | Proposition 5 |
| V9 | Soft mirror: $$\kappa_s(w) = \max(0, s - \mathrm{wt}(w))$$; same round count; muddy children reach $$B_i m_i$$, not $$K_i m_i$$; clean children never believe themselves muddy | Theorem 2 |
| V9b | The terminal muddy attitude is strong belief and safe belief, still short of knowledge | Theorem 2 |
| V10 | A soft report round gives every clean child the true belief $$B_j \neg m_j$$ | Section 6.1 |
| V11 | Wrong father, soft: all believe muddy, one truthful upgrade restores true beliefs; hard: the same two announcements empty the model | Proposition 5 |
| V12 | Radical and conservative upgrades coincide along the muddy run | Proposition 4 |
| V13 | Iterated $$\Uparrow$$ of a doxastic Moore formula cycles with period two | Section 7.1 |

The engine is small enough to read in one sitting; its three load-bearing definitions, lightly condensed here, are the ones this essay is about:

```
"""
muddy_del_verify.py — Machine verification for
"Mud, Silence, and the Architecture of Common Knowledge"

Implements:
  * S5 epistemic models over the muddy-children hypercube {0,1}^n
  * Public Announcement Logic (PAL) update (world elimination)
  * E^k / common-knowledge checking (reachability fixed point)
  * Epistemic plausibility models with joint radical (⇑) and
    conservative (↑) upgrades; belief = truth in the most plausible
    worlds of the agent's information cell
Every numbered check V1..V13 corresponds to a claim made in the essay.
Exit code 0 iff all checks pass.
"""

from itertools import product

# ----------------------------------------------------------------------
# Hard-information layer: S5 models and PAL
# ----------------------------------------------------------------------

def all_worlds(n):
    return [tuple(bits) for bits in product((0, 1), repeat=n)]

def weight(w):
    return sum(w)

def cell(i, w, worlds):
    """Agent i's information cell at w within the current model:
    worlds agreeing with w on every coordinate except possibly i."""
    return [v for v in worlds
            if all(v[j] == w[j] for j in range(len(w)) if j != i)]

def K(i, prop, w, worlds):
    """K_i prop at w: prop holds throughout i's cell."""
    return all(prop(v, worlds) for v in cell(i, w, worlds))

def knows_muddy(i):
    return lambda w, ws: K(i, lambda v, _: v[i] == 1, w, ws)

def knows_clean(i):
    return lambda w, ws: K(i, lambda v, _: v[i] == 0, w, ws)

def knows_own(i):
    return lambda w, ws: knows_muddy(i)(w, ws) or knows_clean(i)(w, ws)

def father(w, worlds):              # "at least one of you is muddy"
    return weight(w) >= 1

def theta(w, worlds):               # "nobody knows whether they are muddy"
    n = len(w)
    return all(not knows_own(i)(w, worlds) for i in range(n))

def theta_simple(w, worlds):        # "nobody knows that they are muddy"
    n = len(w)
    return all(not knows_muddy(i)(w, worlds) for i in range(n))

def announce(prop, worlds):
    """PAL update: restrict the model to the worlds where prop holds."""
    return [w for w in worlds if prop(w, worlds)]

def E(prop, w, worlds):
    n = len(w)
    return all(K(i, prop, w, worlds) for i in range(n))

def E_iter(prop, j, w, worlds):
    """E^j prop, with E^0 prop := prop."""
    f = prop
    for _ in range(j):
        g = f
        f = (lambda gg: lambda v, ws: E(gg, v, ws))(g)
    return f(w, worlds)

def common_knowledge(prop, w, worlds):
    """C prop at w: prop holds at every world reachable from w via the
    union of the agents' relations (reflexive-transitive closure)."""
    n = len(w)
    seen, frontier = {w}, [w]
    while frontier:
        u = frontier.pop()
        for i in range(n):
            for v in cell(i, u, worlds):
                if v not in seen:
                    seen.add(v)
                    frontier.append(v)
    return all(prop(v, worlds) for v in seen)

def hard_run(n, actual):
    """Father's announcement, then ignorance announcements while truthful.
    Returns the list of models [M0, M1, ..., M_k]."""
    models = [all_worlds(n)]
    models.append(announce(father, models[-1]))          # M1
    while theta(actual, models[-1]):                     # truthful only
        models.append(announce(theta, models[-1]))
    return models

# ----------------------------------------------------------------------
# Soft-information layer: plausibility models and upgrades
# ----------------------------------------------------------------------

def uniform_ranks(n):
    return {w: 0 for w in all_worlds(n)}

def dense(ranks_sorted_keys, key):
    """Re-rank densely according to a sort key."""
    ordered = sorted(ranks_sorted_keys, key=key)
    out, r, prev = {}, -1, None
    for w in ordered:
        if prev is None or key(w) != prev:
            r += 1
            prev = key(w)
        out[w] = r
    return out

def radical(prop, ranks):
    """Joint radical upgrade ⇑φ: all φ-worlds become strictly more
    plausible than all ¬φ-worlds; within zones the old order is kept."""
    ext = {w for w in ranks if prop(w, ranks)}
    return dense(ranks.keys(), lambda w: (w not in ext, ranks[w]))

def conservative(prop, ranks):
    """Joint conservative upgrade ↑φ: only the *best* φ-worlds become
    most plausible; everything else keeps its relative order."""
    ext = [w for w in ranks if prop(w, ranks)]
    if not ext:
        return dict(ranks)
    m = min(ranks[w] for w in ext)
    promoted = {w for w in ext if ranks[w] == m}
    return dense(ranks.keys(), lambda w: (w not in promoted, ranks[w]))

def B(i, prop, w, ranks):
    """B_i prop at w: prop holds at all most-plausible worlds of i's cell.
    Cells are computed over the full world set (soft info deletes nothing)."""
    ws = list(ranks.keys())
    c = cell(i, w, ws)
    m = min(ranks[v] for v in c)
    best = [v for v in c if ranks[v] == m]
    return all(prop(v, ranks) for v in best)

def believes_muddy(i):
    return lambda w, rk: B(i, lambda v, _: v[i] == 1, w, rk)

def believes_clean(i):
    return lambda w, rk: B(i, lambda v, _: v[i] == 0, w, rk)

def believes_own(i):
    return lambda w, rk: believes_muddy(i)(w, rk) or believes_clean(i)(w, rk)

def father_soft(w, ranks):
    return weight(w) >= 1

def theta_soft(w, ranks):           # "nobody has an opinion on their status"
    n = len(w)
    return all(not believes_own(i)(w, ranks) for i in range(n))

def soft_run(n, actual, upgrade=radical):
    """⇑father, then ⇑(doxastic ignorance) while truthful at the actual world."""
    rks = [uniform_ranks(n)]
    rks.append(upgrade(father_soft, rks[-1]))
    while theta_soft(actual, rks[-1]):
        rks.append(upgrade(theta_soft, rks[-1]))
    return rks

# ----------------------------------------------------------------------
# Checks
# ----------------------------------------------------------------------

RESULTS = []

def check(name, ok, detail=""):
    RESULTS.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))

def actual_world(n, k):
    return tuple([1] * k + [0] * (n - k))

# ---- V1: layer theorem + round counting (hard) ----
ok = True
for n in (3, 4, 5):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        ms = hard_run(n, a)
        # number of ignorance announcements actually made = k-1
        ok &= (len(ms) == k + 1)               # M0, M1, ..., M_k
        for j, M in enumerate(ms[1:], start=1):
            ok &= (set(M) == {w for w in all_worlds(n) if weight(w) >= j})
        # nobody knows-own before M_k; all muddy know (positively) at M_k
        for j in range(1, k):
            ok &= all(not knows_own(i)(a, ms[j]) for i in range(n))
        ok &= all(knows_muddy(i)(a, ms[k]) for i in range(k))
        ok &= all(not knows_own(i)(a, ms[k]) for i in range(k, n))
check("V1 hard run: M_j = {weight >= j}; muddy first know (K_i m_i) at stage k", ok)

# ---- V2: E^j hierarchy and common knowledge ----
ok = True
for n in (3, 4):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        M0 = all_worlds(n)
        for j in range(0, n + 1):
            ok &= (E_iter(father, j, a, M0) == (j <= k - 1))
        ok &= (not common_knowledge(father, a, M0))
        M1 = announce(father, M0)
        ok &= common_knowledge(father, a, M1)
check("V2 in M0: E^j(father) iff j <= k-1; C fails; C holds in M1", ok)

# ---- V3: for k>=2 the father's content is already known by everyone ----
ok = all(E_iter(father, 1, actual_world(n, k), all_worlds(n)) == (k >= 2)
         for n in (3, 4) for k in range(1, n + 1))
check("V3 E(father) in M0 iff k >= 2 (announcement first-order uninformative)", ok)

# ---- V4: without the father, ignorance announcements are vacuous ----
ok = True
for n in (3, 4):
    M0 = all_worlds(n)
    ok &= all(theta(w, M0) for w in M0)        # true everywhere
    ok &= (announce(theta, M0) == M0)          # update removes nothing
check("V4 no seed, no progress: M0 | theta = M0", ok)

# ---- V5: K_i(clean) never holds along the run; both ignorance readings agree ----
ok = True
for n in (3, 4):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        ms = hard_run(n, a)
        for M in ms:
            ok &= all(not knows_clean(i)(w, M) for w in M for i in range(n))
        # rerun with the weaker formula; same models stage by stage
        alt = [all_worlds(n), announce(father, all_worlds(n))]
        while theta_simple(a, alt[-1]):
            alt.append(announce(theta_simple, alt[-1]))
        ok &= all(set(x) == set(y) for x, y in zip(ms, alt)) and len(ms) == len(alt)
check("V5 'knows clean' never true; know-that vs know-whether runs coincide", ok)

# ---- V6: the last ignorance announcement refutes itself; father's is successful ----
ok = True
for n in (3, 4):
    for k in range(2, n + 1):
        a = actual_world(n, k)
        ms = hard_run(n, a)
        ok &= theta(a, ms[k - 1])                      # true when announced
        ok &= (not theta(a, ms[k]))                    # false afterwards
        M1 = ms[1]
        ok &= all(father(w, M1) for w in M1)           # father's formula survives
check("V6 [!theta]~theta at the last round; [!father]father (and C father)", ok)

# ---- V7: the 'I know' round teaches the clean children ----
ok = True
for n in (3, 4):
    for k in range(1, n):
        a = actual_world(n, k)
        Mk = hard_run(n, a)[-1]
        def reports(w, ws, k=k, n=n):
            r = all(knows_muddy(i)(w, ws) for i in range(k))
            r &= all(not knows_own(i)(w, ws) for i in range(k, n))
            return r
        Mfin = announce(reports, Mk)
        ok &= all(knows_clean(j)(a, Mfin) for j in range(k, n))
check("V7 after the muddy children's 'I know', clean children know they are clean", ok)

# ---- V8: hard update with a false announcement deletes reality ----
n = 3
a0 = (0, 0, 0)
M1_bad = announce(father, all_worlds(n))
check("V8 false hard announcement: the actual world is eliminated",
      a0 not in M1_bad, "PAL precondition fails; reality leaves the model")

# ---- V9: soft mirror — rank(w) = max(0, stage - weight(w)); same round count ----
ok = True
for n in (3, 4):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        rks = soft_run(n, a)
        ok &= (len(rks) == k + 1)
        for s, rk in enumerate(rks):
            ok &= all(rk[w] == max(0, s - weight(w)) for w in rk)
        final = rks[-1]
        ok &= all(believes_muddy(i)(a, final) for i in range(k))      # true belief
        ok &= all(not knows_muddy(i)(a, list(final.keys())) if False else
                  not K(i, lambda v, _: v[i] == 1, a, list(final.keys()))
                  for i in range(k))                                   # ...not knowledge
        for rk in rks:                                                 # clean kids:
            ok &= all(not believes_muddy(j)(a, rk) for j in range(k, n))
check("V9 soft run mirrors hard run: rank = max(0, stage - weight); "
      "muddy get B_i m_i (not K_i m_i) at stage k; clean never believe muddy", ok)

# ---- V9b: at stage k the muddy children's belief is STRONG and SAFE, not K ----
def strong_belief(i, prop, w, ranks):
    """All prop-worlds in i's cell strictly more plausible than all others,
    and prop holds somewhere in the cell (Baltag–Smets strong belief)."""
    ws = list(ranks.keys())
    c = cell(i, w, ws)
    pos = [v for v in c if prop(v, ranks)]
    neg = [v for v in c if not prop(v, ranks)]
    return bool(pos) and all(ranks[u] < ranks[v] for u in pos for v in neg)

def safe_belief(i, prop, w, ranks):
    """prop holds at every cell world at least as plausible as w (Stalnaker)."""
    ws = list(ranks.keys())
    return all(prop(v, ranks) for v in cell(i, w, ws) if ranks[v] <= ranks[w])

ok = True
for n in (3, 4):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        final = soft_run(n, a)[-1]
        muddy_prop = lambda i: (lambda v, _ : v[i] == 1)
        for i in range(k):
            ok &= strong_belief(i, muddy_prop(i), a, final)
            ok &= safe_belief(i, muddy_prop(i), a, final)
            ok &= not K(i, lambda v, _: v[i] == 1, a, list(final.keys()))
check("V9b muddy children end with strong AND safe belief in m_i, still without K_i m_i", ok)

# ---- V10: soft report round teaches the clean children (in belief) ----
ok = True
for n in (3, 4):
    for k in range(1, n):
        a = actual_world(n, k)
        final = soft_run(n, a)[-1]
        def reports_soft(w, rk, k=k, n=n):
            r = all(believes_muddy(i)(w, rk) for i in range(k))
            r &= all(not believes_own(i)(w, rk) for i in range(k, n))
            return r
        after = radical(reports_soft, final)
        ok &= all(believes_clean(j)(a, after) for j in range(k, n))
check("V10 soft 'I believe I'm muddy' round gives clean children B_j(clean)", ok)

# ---- V11: wrong father — soft degrades gracefully and is reversible ----
n = 3
a0 = (0, 0, 0)
rk1 = radical(father_soft, uniform_ranks(n))
all_wrong = all(believes_muddy(i)(a0, rk1) for i in range(n))
rk2 = radical(lambda w, r: weight(w) == 0, rk1)        # truthful correction
recovered = all(believes_clean(i)(a0, rk2) for i in range(n))
M_after_two_hard = announce(lambda w, ws: weight(w) == 0,
                            announce(father, all_worlds(n)))
check("V11 soft: false father => all wrongly believe muddy, yet correction restores "
      "true beliefs; hard: the same two announcements empty the model",
      all_wrong and recovered and len(M_after_two_hard) == 0)

# ---- V12: radical and conservative upgrades coincide on this protocol ----
ok = True
for n in (3, 4):
    for k in range(1, n + 1):
        a = actual_world(n, k)
        r1 = soft_run(n, a, upgrade=radical)
        r2 = soft_run(n, a, upgrade=conservative)
        ok &= (len(r1) == len(r2)) and all(x == y for x, y in zip(r1, r2))
check("V12 radical (⇑) and conservative (↑) upgrades coincide along the muddy run", ok)

# ---- V13: iterated radical upgrade can oscillate (doxastic Moore input) ----
wp, wq = ("p",), ("q",)             # one agent, two indistinguishable worlds
ranks = {wp: 0, wq: 0}
def chi(w, rk):                     # "I am wrong about p"
    ws = list(rk.keys())
    m = min(rk[v] for v in ws)
    best = [v for v in ws if rk[v] == m]
    bp = all(v == wp for v in best)
    return (w == wp and not bp) or (w == wq and bp)
seq, truth_at_wp = [], []
r = dict(ranks)
for _ in range(6):
    truth_at_wp.append(chi(wp, r))
    r = dense(r.keys(), lambda w: (not chi(w, r), r[w]))   # unconditional ⇑χ
    seq.append((r[wp], r[wq]))
osc = (seq[0] != seq[1] and seq[0] == seq[2] and seq[1] == seq[3]
       and seq[2] == seq[4] and seq[3] == seq[5])
check("V13 iterated ⇑ of a doxastic-Moore formula cycles with period 2",
      osc, f"rank trajectory {seq}; truth of input at actual {truth_at_wp}")

# ----------------------------------------------------------------------
# Tables for the essay
# ----------------------------------------------------------------------

def fmt(w):
    return "".join(map(str, w))

print("\n--- Table A: hard run, n = 3, k = 2, actual world 110 ---")
a = (1, 1, 0)
for j, M in enumerate(hard_run(3, a)):
    kn = [i + 1 for i in range(3) if knows_own(i)(a, M)]
    print(f"M{j}: worlds = {sorted(map(fmt, M))}; "
          f"theta@actual = {theta(a, M)}; children who know: {kn or '-'}")

print("\n--- Table B: soft run (radical), n = 3, k = 3, actual world 111 ---")
a = (1, 1, 1)
for s, rk in enumerate(soft_run(3, a)):
    by_rank = {}
    for w, r0 in rk.items():
        by_rank.setdefault(r0, []).append(fmt(w))
    desc = " | ".join(f"rank {r0}: {sorted(ws)}" for r0, ws in sorted(by_rank.items()))
    bel = [i + 1 for i in range(3) if believes_own(i)(a, rk)]
    print(f"stage {s}: {desc}; believers: {bel or '-'}")

print("\n--- Table C: wrong father, n = 3, actual 000 (soft) ---")
r0 = uniform_ranks(3)
r1 = radical(father_soft, r0)
r2 = radical(lambda w, r: weight(w) == 0, r1)
for tag, rk in (("start", r0), ("after ⇑father", r1), ("after ⇑'nobody muddy'", r2)):
    bels = ["B%d(muddy)" % (i + 1) for i in range(3) if believes_muddy(i)((0, 0, 0), rk)]
    bels += ["B%d(clean)" % (i + 1) for i in range(3) if believes_clean(i)((0, 0, 0), rk)]
    print(f"{tag}: beliefs at 000 = {bels or 'none'}")

# ----------------------------------------------------------------------
failed = [name for name, ok in RESULTS if not ok]
print(f"\n{'ALL ' + str(len(RESULTS)) + ' CHECKS PASSED' if not failed else 'FAILED: ' + str(failed)}")
raise SystemExit(0 if not failed else 1)

```

One line each for hard update, soft upgrade, and belief, and the entire essay is a commentary on the difference between the first two.

## References

Aumann, R. J. (1976). Agreeing to disagree. *The Annals of Statistics*, 4(6), 1236–1239.

Balbiani, P., Baltag, A., van Ditmarsch, H., Herzig, A., Hoshi, T., & de Lima, T. (2008). 'Knowable' as 'known after an announcement'. *The Review of Symbolic Logic*, 1(3), 305–334.

Baltag, A., & Moss, L. S. (2004). Logics for epistemic programs. *Synthese*, 139(2), 165–224.

Baltag, A., Moss, L. S., & Solecki, S. (1998). The logic of public announcements, common knowledge, and private suspicions. In *Proceedings of the 7th Conference on Theoretical Aspects of Rationality and Knowledge (TARK VII)*.

Baltag, A., & Smets, S. (2008). A qualitative theory of dynamic interactive belief revision. In G. Bonanno, W. van der Hoek, & M. Wooldridge (Eds.), *Logic and the Foundations of Game and Decision Theory (LOFT 7)*, Texts in Logic and Games 3 (pp. 9–58). Amsterdam University Press.

Baltag, A., & Smets, S. (2009). Group belief dynamics under iterated revision: Fixed points and cycles of joint upgrades. In *Proceedings of the 12th Conference on Theoretical Aspects of Rationality and Knowledge (TARK XII)* (pp. 41–50).

Baltag, A., & Smets, S. (2011). Keep changing your beliefs, aiming for the truth. *Erkenntnis*, 75(2), 255–270.

Barwise, J. (1981). Scenes and other situations. *The Journal of Philosophy*, 78(7), 369–397.

Fagin, R., Halpern, J. Y., Moses, Y., & Vardi, M. Y. (1995). *Reasoning About Knowledge*. MIT Press.

Gamow, G., & Stern, M. (1958). *Puzzle-Math*. Viking.

Gerbrandy, J. (1999). *Bisimulations on Planet Kripke*. PhD thesis, ILLC, University of Amsterdam.

Gerbrandy, J., & Groeneveld, W. (1997). Reasoning about information change. *Journal of Logic, Language and Information*, 6(2), 147–169.

Halpern, J. Y., & Moses, Y. (1990). Knowledge and common knowledge in a distributed environment. *Journal of the ACM*, 37(3), 549–587.

Holliday, W. H., & Icard, T. F. (2010). Moorean phenomena in epistemic logic. In *Advances in Modal Logic*, Vol. 8. College Publications.

Littlewood, J. E. (1953). *A Mathematician's Miscellany*. Methuen.

Lutz, C. (2006). Complexity and succinctness of public announcement logic. In *Proceedings of the 5th International Joint Conference on Autonomous Agents and Multiagent Systems (AAMAS '06)* (pp. 137–144).

Moses, Y., Dolev, D., & Halpern, J. Y. (1986). Cheating husbands and other stories: A case study of knowledge, action, and communication. *Distributed Computing*, 1(3), 167–176.

Plaza, J. (1989). Logics of public communications. In *Proceedings of the 4th International Symposium on Methodologies for Intelligent Systems* (pp. 201–216). Reprinted in *Synthese*, 158(2), 165–179 (2007).

Rubinstein, A. (1989). The electronic mail game: Strategic behavior under "almost common knowledge." *The American Economic Review*, 79(3), 385–391.

Stalnaker, R. (2006). On logics of knowledge and belief. *Philosophical Studies*, 128(1), 169–199.

van Benthem, J. (2007). Dynamic logic for belief revision. *Journal of Applied Non-Classical Logics*, 17(2), 129–155.

van Benthem, J. (2011). *Logical Dynamics of Information and Interaction*. Cambridge University Press.

van Benthem, J., van Eijck, J., & Kooi, B. (2006). Logics of communication and change. *Information and Computation*, 204(11), 1620–1662.

van Ditmarsch, H., & Kooi, B. (2006). The secret of my success. *Synthese*, 151(2), 201–232. Erratum: *Synthese*, 153, 339.

van Ditmarsch, H., van der Hoek, W., & Kooi, B. (2008). *Dynamic Epistemic Logic*. Synthese Library 337. Springer.

