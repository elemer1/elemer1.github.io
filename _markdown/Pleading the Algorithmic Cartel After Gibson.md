---
title: Pleading the Algorithmic Cartel After Gibson
permalink: /pleading-the-algorithmic-cartel-after-gibson/
listed: true
---

## Abstract

Algorithmic-pricing cases expose a mismatch between Sherman Act § 1 pleading doctrine and a form of coordination that is computational rather than conversational. After *Gibson v. Cendyn Group*, a complaint alleging that horizontal rivals adopted the same pricing intermediary can fail unless plaintiffs plead facts about data flows, objective functions, override rates, and monitoring architecture that are knowable only after discovery. This Note calls that mismatch the pleading-stage deadlock. It argues that the answer is not a new substantive rule of liability, a *per se* rule for pricing software, or artificial legal personhood for algorithms. The answer is a procedural calibration of plausibility doctrine: a Cartel-Manager Plausibility Framework, grounded in Hovenkamp and Leslie's cartel-manager account, under which a complaint should survive Rule 12(b)(6) when it plausibly alleges (1) competitively significant common adoption of a pricing intermediary by horizontal rivals, (2) nonpublic, forward-looking, competitively sensitive data inflow from those rivals into the intermediary's runtime operation, and (3) at least one alignment-predisposing design or use feature. Defendants may rebut at the pleading stage with specific factual showings, while *per se*, quick-look, and rule-of-reason analysis remain for the merits. The framework preserves *Twombly*'s screening function without converting technological opacity into § 1 immunity.

---

## Introduction

A guest paying for a Las Vegas Strip hotel room in 2023 may have paid a price no single hotel, acting alone, fully chose. Cendyn's GuestRev and GroupRev revenue-management tools, licensed to several large Strip operators, allegedly ingested hotel-specific occupancy and pricing data, demand forecasts, and competitor-rate information; processed those inputs through proprietary pricing logic; and returned recommended rates that Cendyn's own marketing materials described as accepted at high rates.[^pre1] When room rates rose across the Strip, hotel guests sued.[^pre2] The Ninth Circuit affirmed dismissal on August 15, 2025. The court treated the case as one involving common use of the same price-recommendation software, not a pleaded horizontal agreement among hotels.[^1] The Supreme Court denied certiorari on April 20, 2026.[^2] On those pleadings, the merits were never reached.

That procedural posture is the problem. Algorithmic-pricing litigation increasingly presents the same structure: horizontal rivals adopt a common pricing intermediary; each sends nonpublic, competitively sensitive data into the intermediary's runtime operation; the intermediary uses that information to generate pricing recommendations; the rivals predominantly accept those recommendations; prices rise; and no two rivals need to communicate directly. RealPage and Yardi litigation in multifamily housing, Cendyn litigation in casino-hotel markets, and early scholarship on algorithmic pricing in ride-sharing, retail, and labor markets all point to variants of this structure.[^pre3] The question is not whether every such system is illegal. It plainly is not. The question is what plaintiffs must allege before discovery to test whether the system is merely efficient pricing advice or the functional equivalent of an outsourced cartel manager.

The answer after *Gibson* is unstable. In the same period in which the Ninth Circuit affirmed *Gibson* and the Supreme Court denied review, trial-level decisions split over whether comparable complaints had pleaded a § 1 agreement,[^3] the Department of Justice built a three-part consent-decree record against RealPage, Greystar, and LivCor,[^4] and state and local governments enacted categorical bans, disclosure mandates, and targeted antitrust amendments aimed at algorithmic pricing.[^5] The substantive law of § 1 did not change. *Twombly* was not revisited. No appellate court adopted a new test for concerted action. Yet the doctrinal terrain moved because pleading doctrine became outcome-determinative.

This Note calls the resulting condition the pleading-stage deadlock. The deadlock arises because *Twombly* and *Iqbal* require plaintiffs to plead facts that plausibly suggest agreement rather than independent parallel conduct,[^7] while the facts that most directly distinguish coordination from independent adoption in algorithmic-intermediation cases are internal to the vendor's system: the objective function, the runtime data flows, the override rate, the monitoring architecture, and the design features that dampen undercutting.[^8] In the analog cartel cases, the key facts were hidden but externally legible: meetings, calls, letters, trade-association minutes, internal memoranda. In algorithmic-intermediation cases, the key facts are computationally situated. They exist inside a proprietary system plaintiffs cannot inspect before discovery. *Gibson* did not create that asymmetry, but it gave the asymmetry doctrinal force.

Existing doctrines do not solve the problem cleanly. Hub-and-spoke doctrine, from *Interstate Circuit* through *Toys "R" Us* and *Apple e-Books*,[^9] still looks for a rim of horizontal awareness that algorithmic intermediation can obscure. *Theatre Enterprises*[^10] and *Matsushita*[^11] make pure parallel conduct insufficient, but the plus factors most probative in this setting are often the same internal technical facts plaintiffs cannot plead. Service-contract or vertical-restraints framing either removes the challenged restraint from the relevant market or pushes the case into a rule-of-reason posture before the horizontal-coordination question has been answered.[^12] State legislation, including California's AB 325 and New York's S.7882,[^13] responds to under-enforcement, but often by sacrificing the Sherman Act's case-by-case calibration.

This Note proposes a federal, antitrust-internal answer: a **Cartel-Manager Plausibility Framework**. The framework creates a structured pleading-stage inference of § 1 plausibility, grounded in Herbert Hovenkamp and Christopher Leslie's account of the firm as cartel manager.[^14] A complaint should trigger the framework when it plausibly alleges three things: (1) competitively significant common adoption of a pricing intermediary among horizontal rivals in a properly pleaded relevant market; (2) nonpublic, forward-looking, competitively sensitive data flowing from those rivals into the intermediary's runtime operation; and (3) at least one alignment-predisposing design or use feature, such as autopilot defaults, override friction, vendor monitoring, vendor-organized user meetings, market-wide dashboards, anti-undercut design, or vendor marketing of high acceptance rates. Defendants may rebut with specific factual showings at the motion-to-dismiss stage. Merits review under *per se*, quick-look, or rule-of-reason doctrine remains for summary judgment and trial.

The framework makes four contributions. First, it reframes *Gibson* as a procedural decision with substantive consequences: the opinion does not hold that algorithmic intermediation is lawful, but its pleading posture can prevent courts from ever testing whether it is. Second, it operationalizes the Hovenkamp-Leslie cartel-manager account without pretending that the article itself created a freestanding doctrine. Third, it supplies a bounded trigger-and-rebuttal mechanism that preserves *Twombly*'s screening function while preventing defendants from turning proprietary opacity into pleading-stage immunity. Fourth, it offers a federalism-sensitive alternative to categorical state bans by giving federal courts a calibrated tool for discovery access in the cases that fit the cartel-manager pattern.

Two limits are essential. This Note does not argue that common adoption of pricing software is inherently anticompetitive, that algorithmic intermediation is a *per se* § 1 violation, or that an algorithm is a Sherman Act person. The agreement, when one is plausibly alleged, runs among the user firms. The vendor is the implementation mechanism, and in some cases a co-conspirator, through which the user-firm agreement operates. The proposal is procedural: it answers what plaintiffs must allege to be allowed to find out what the system actually does.

The roadmap is straightforward. Section II sets out the doctrinal background. Section III maps the 2023-2026 algorithmic-pricing cases, consent decrees, and legislative responses. Section IV diagnoses the pleading-stage deadlock. Section V develops the Cartel-Manager Plausibility Framework and applies it to *Gibson*, *Cornish-Adebiyi*, *Duffy*, *RealPage*, and *Mach*. Section VI addresses federalism. Section VII answers the strongest objections. Section VIII concludes with the live Third Circuit posture in *Cornish-Adebiyi v. Caesars Entertainment*, the next appellate opportunity to decide whether *Gibson* becomes the baseline or the outlier.[^15]

The right question is not whether the algorithm is a cartel manager. It is what plaintiffs must allege to be allowed to find out.

---

## II. The Doctrinal Setting

### II.A. *Twombly*, *Iqbal*, and the Pleading Architecture for § 1

The foundational architecture for any modern § 1 claim is the plausibility regime announced in *Bell Atlantic Corp. v. Twombly* and extended in *Ashcroft v. Iqbal*.[^17] *Twombly* itself was a § 1 case alleging parallel conduct by incumbent local exchange carriers in resisting competition from competitive local exchange carriers and in declining to enter each other's territories. The Court rejected the complaint, holding that an allegation of "parallel conduct" is consistent with conspiracy but "just as much in line with a wide swath of rational and competitive business strategy unilaterally prompted by common perceptions of the market."[^18] The complaint had to "raise a reasonable expectation that discovery will reveal evidence of illegal agreement."[^19] *Iqbal* generalized the standard across civil litigation and made clear that "a court considering a motion to dismiss can choose to begin by identifying pleadings that, because they are no more than conclusions, are not entitled to the assumption of truth."[^20]

The plausibility regime has three features that matter for this Note. *First*, plausibility is calibrated to discovery cost. *Twombly* was explicit that the Court's anxiety was the "potentially enormous expense of discovery"[^21] in antitrust cases — a concern the Court treated as a structural reason to demand more from the complaint, not as a separable equitable adjustment. *Second*, plausibility is asymmetric: a complaint must plead facts that "render plaintiffs' entitlement to relief plausible," but defendants need not affirmatively negate the inference of agreement.[^22] *Third*, plausibility is contextual. *Iqbal* tied plausibility to "judicial experience and common sense,"[^23] and the lower courts have unevenly translated this contextual instruction into doctrinal practice in technical fields where "common sense" is a poor substitute for technical expertise.

Each of these features matters in ways the Court did not anticipate when applied to algorithmic-pricing intermediation. Discovery cost cuts both ways: while *Twombly* was concerned about the strike-suit risk in mass conspiracy cases, the structure of algorithmic intermediation means that *no amount* of pre-discovery investigation by a plaintiff can produce the technical facts the post-*Gibson* case law treats as required. Asymmetry compounds the problem. And the "common sense" baseline that *Iqbal* invoked produces opposite intuitions for different readers in the algorithmic context — a consumer-side reader sees coordinated price hikes as *prima facie* suspicious; an industry-side reader sees common adoption of efficient yield-management software as the unremarkable competitive strategy *Twombly* protects.

The result is that the *Twombly* framework, applied without modification to algorithmic intermediation, systematically over-screens. This Note argues that the appropriate response is not to abandon plausibility — *Twombly* remains good law — but to articulate, within plausibility doctrine, a trigger-and-rebuttal structure that maps onto the actual evidentiary economics of algorithmic intermediation.

### II.B. *Theatre Enterprises*, Parallel Conduct, and Plus Factors

If *Twombly* is the procedural skeleton of modern § 1 pleading, *Theatre Enterprises, Inc. v. Paramount Film Distributing Corp.*[^24] is the substantive doctrine it formalizes. *Theatre Enterprises* held that "conscious parallelism" — parallel pricing or parallel conduct without more — is not by itself sufficient to establish concerted action.[^25] To survive, a plaintiff must allege "plus factors": circumstantial markers that move the inference from interdependent oligopoly behavior toward agreement.[^26] The classic plus-factor catalog includes (i) actions against unilateral self-interest absent an agreement; (ii) opportunity to conspire (industry meetings, shared trade associations); (iii) high level of inter-firm communication; (iv) abrupt changes in business practice; and (v) market structure conducive to coordination.[^27]

The plus-factor framework was developed against the analog backdrop of executive meetings, telephone calls, hotel-room handshakes, and the kind of correspondence that a discovery sweep could surface. Its limitations in the algorithmic context are not merely empirical but structural. Consider the canonical plus factors as they map onto algorithmic intermediation:

- **Action against unilateral self-interest.** It is not at all clear what counts as "unilateral self-interest" when each firm has voluntarily delegated its pricing decision to a vendor whose objective function the firm cannot fully audit. Each user firm's decision to accept the algorithm's recommendation can be characterized as either "rational acceptance of efficient pricing advice" (the defense narrative) or "knowing surrender of pricing discretion to a coordination mechanism" (the plaintiff narrative). Without discovery into the algorithm's objective function, the plus factor cannot be operationalized.

- **Opportunity to conspire.** The algorithmic vendor's user-group meetings, dashboards, and roadmap webinars are evidence of opportunity, but Ninth Circuit doctrine after *Gibson* treats them as evidence of vertical commercial relationships rather than horizontal coordination.[^28] The "opportunity" framing assumes the relevant agents are the user firms; if the relevant agent is the vendor, the framing breaks down.

- **High level of inter-firm communication.** The defining feature of algorithmic intermediation is that the coordination occurs *through* the intermediary, not between user firms directly. The plus factor demands the very pattern of communication the technology is designed to obviate.

- **Abrupt changes in business practice.** Adoption of a third-party pricing intermediary is a single, observable change. Subsequent price-trajectory shifts may be observable in market data. But the plus factor remains consistent with each firm independently optimizing its yield-management strategy, exactly the *Twombly* defense.

- **Market structure conducive to coordination.** This is the one plus factor algorithmic intermediation amplifies. The market-structure analysis after the introduction of common-algorithm intermediation is *more* conducive to coordination, not less, because the intermediary internalizes monitoring and enforcement costs that historically constrained tacit collusion. But the post-*Gibson* case law has not credited this amplification at the pleading stage.

The traditional plus-factor framework is, in short, designed for a world in which conspirators meet and talk. Algorithmic intermediation moves the locus of coordination outside the firm boundary into a third-party computational system. The plus factors do not disappear in this world, but they need to be re-specified with reference to the actual evidentiary economics of intermediated coordination. Section V's plus-factor list is one such re-specification.

### II.C. Hub-and-Spoke and the Rim Problem

The hub-and-spoke conspiracy doctrine is a closer fit to algorithmic intermediation than *Theatre Enterprises*' parallel-conduct framework, but it imposes its own limitation. The line of authority runs from *Interstate Circuit, Inc. v. United States*,[^29] in which the Supreme Court inferred horizontal agreement from a single demand letter sent by an exhibitor to multiple film distributors who each independently complied, through *Toys "R" Us, Inc. v. FTC*,[^30] in which the Seventh Circuit held that a single retailer's use of a "common purpose" condition with multiple toy manufacturers — paired with the manufacturers' awareness of each other's compliance — supported a horizontal-agreement finding, to *United States v. Apple, Inc.*,[^31] in which the Second Circuit upheld a finding that Apple had orchestrated a horizontal price-fixing agreement among five major book publishers through individually-negotiated agency agreements containing most-favored-nation provisions and pricing tiers.

The pattern across these cases is a "hub" actor (the exhibitor; Toys "R" Us; Apple) and "spoke" actors (the film distributors; the toy manufacturers; the publishers) who, although they did not communicate directly, took actions in awareness of each other's parallel conduct under the hub's coordination. The "rim" — the horizontal connection among spokes that distinguishes a true horizontal conspiracy from a series of parallel vertical agreements — is the doctrinal pinch point. *Apple* found the rim in the publishers' direct communications about the agency-pricing strategy.[^32] *Toys "R" Us* found it in evidence that each manufacturer's compliance was conditioned on the others' compliance.[^33] *Interstate Circuit* inferred it from the simultaneity and uniformity of the distributors' responses to a demand letter copied to all of them, combined with the obvious self-interest each had in not complying alone.[^34]

The rim is the question algorithmic-intermediation cases turn on. *Gibson*'s holding is fundamentally a rim-pessimism holding: the Ninth Circuit treated the absence of allegations that confidential information was *shared among hotel licensees* as dispositive of the rim question.[^35] The framing is that each hotel had its own bilateral licensing agreement with Cendyn; the algorithm processed each hotel's data; and absent an allegation that hotel A could see hotel B's data flowing into the system, the case was a series of parallel verticals, not a horizontal hub-and-spoke.

This Note's quarrel with *Gibson* is not that it misunderstood hub-and-spoke doctrine. It is that *Gibson* asked the rim question at the wrong level of abstraction. The rim in algorithmic intermediation does not run between user firms directly; it runs through the algorithm's objective function. If the algorithm optimizes for market-wide yield given knowledge of all users' nonpublic data — that is, if the algorithm internalizes the coordination function — then the rim is realized computationally rather than communicatively. The rim is "made of code." Conventional hub-and-spoke doctrine has no language for this, because the analog cases that built the doctrine had no such object to point to. The Note's framework is, in part, an effort to provide that language without rewriting hub-and-spoke doctrine substantively.

### II.D. The Hovenkamp–Leslie Cartel-Manager Account (Doctrinal Setting Only)

Hovenkamp and Leslie's 2011 *Vanderbilt Law Review* article *The Firm as Cartel Manager*[^36] supplies the theoretical account on which Section V of this Note builds. A brief setup at this stage of the doctrinal map serves to fix the article's location in the antitrust-scholarly architecture and to mark its differences from the analog § 1 doctrines surveyed in Sections II.A–C; the substantive recapitulation and operationalization are reserved for Section V.A.

Three points of doctrinal location matter for the Note's argument. *First*, the cartel-manager account is a *normative-theoretical* contribution, not a doctrinal claim about then-existing law. Hovenkamp and Leslie did not argue that any court had adopted a "cartel-manager doctrine"; they argued that existing § 1 doctrine, properly applied, already reaches the cartel manager and that the analytical category of cartel management is useful for organizing the cases in which the doctrine has so reached. The framework offered in Section V respects this distinction: it operationalizes the account, not imports it as if it were established doctrine.

*Second*, the cartel-manager account *complements rather than displaces* the analog § 1 doctrines surveyed in Sections II.A–C. The plus-factor framework continues to govern its proper domain (parallel-conduct cases without coordinating intermediaries); the hub-and-spoke doctrine continues to govern its proper domain (multi-firm coordination through a hub actor); the vertical-restraints frame continues to govern its proper domain (single-firm vertical relationships in input or distribution markets). The cartel-manager account is the theoretical articulation of the pattern across cases like *Interstate Circuit*, *Toys "R" Us*, and *Apple e-Books* — and across the trade-association line — in which a coordinating actor performs the structural work the analog frames have addressed unevenly. The framework offered in Section V occupies the same complementary role.

*Third*, the cartel-manager account is *function-focused rather than entity-focused*. Hovenkamp and Leslie identify the four functions (centralized pricing authority delegated by competing firms; information aggregation and price-recommendation distribution; monitoring of compliance; enforcement of discipline)[^37] as characteristic of cartel management whether the coordinating actor is a competitor, a non-competing trade association, a non-competing retailer, or some other entity. The function-focus is what permits the account to extend to algorithmic intermediation, where the coordinating actor is a software vendor whose corporate form and competitive position are doctrinally irrelevant if the four functions are jointly present. Section V.A unpacks the function-focus and its operational implications for the algorithmic-intermediation context.

Section II.D's role here is doctrinal-setting only. The substantive account, the function-by-function mapping to algorithmic intermediation, the disciplining counterexamples, and the operationalization into pleading triggers are all developed in Section V.A and the sections that follow.

### II.E. The Vertical-Restraints Frame: *Leegin*, *Marine Bancorporation*, *Steves & Sons*

A final piece of the doctrinal setting is the vertical-restraints framework that algorithmic-intermediation cases sometimes invoke as a defense. The argument runs: a software vendor's licensing agreements with its users are vertical agreements in a chain of distribution — input supplier to downstream firm — and after *Leegin Creative Leather Products, Inc. v. PSKS, Inc.*,[^38] vertical agreements (including resale price maintenance) are evaluated under the rule of reason, with no presumption of illegality. *In re RealPage* in the Middle District of Tennessee accepted a version of this argument, treating the "vertical aspects" of the alleged scheme as triggering rule-of-reason review.[^39]

The vertical framing is correct as far as it goes, but it does not resolve the question this Note addresses. The vertical-restraints frame governs the *substantive* standard of review (rule of reason rather than *per se*); it does not answer whether the facts the plaintiff has alleged plausibly constitute concerted action *at all*. A complaint alleging that ten hotel chains entrusted their pricing decisions to a single algorithmic intermediary that aggregates their nonpublic data and outputs uniform supracompetitive prices is, on its face, both a vertical pleading (each hotel chain has a vertical relationship with the vendor) and a horizontal pleading (the ten chains, taken together, have functionally pooled their pricing authority). The vertical framing is true but not exhaustive; the horizontal framing is what § 1 reaches; and the question is whether the horizontal framing has been plausibly pleaded.

Under existing doctrine, the answer turns on the rim question. Under the framework this Note proposes, the answer turns on the conjunction of three triggers and the supporting plus-factor list — and the rim question is reframed as whether the algorithm performs the cartel-manager functions Hovenkamp and Leslie identified. Whether the resulting horizontal conduct is then evaluated under *per se*, quick-look, or rule-of-reason review is a separate question that this Note brackets. The framework is procedural; the substantive question of merits review is left for later stages and for other pieces of scholarship.

The remaining course-relevant cases — *United States v. Marine Bancorporation*[^40] and *Steves & Sons, Inc. v. JELD-WEN, Inc.*[^41] — anchor adjacent doctrines (potential-competition merger doctrine and post-merger vertical foreclosure under § 7, respectively) that this Note will not develop in detail. They are flagged for completeness because the algorithmic-intermediation question is sometimes argued by analogy to the vertical-foreclosure cases in which a downstream firm acquires a key input supplier and is alleged to have used the acquired position to harm horizontal rivals. The analogy is imperfect — algorithmic intermediation typically involves licensing rather than acquisition, and the harm is alleged in the firm-firm horizontal market rather than in the upstream input market — but the analytical move (asking what the integrated firm does that the disaggregated firms could not) is a useful comparator for thinking about what the algorithmic intermediary does that the disaggregated user firms could not lawfully achieve through direct coordination.

---

## III. Algorithmic Pricing 2023–2026: A Doctrinal Map

The eighteen-month period from December 2023 through April 2026 produced several significant judicial opinions, three federal consent-decree tracks, and a wave of state and local legislation. This Section reads the cases against each other, identifies the live doctrinal disagreements, and lays the foundation for the procedural-deadlock claim developed in Section IV. The cases are presented in approximate doctrinal order — *Gibson* first because it now defines the law of the Ninth Circuit and the apparent baseline against which the other circuits are calibrating; *Cornish-Adebiyi* second because the Third Circuit appeal is the next appellate opportunity to revisit the issue; *In re RealPage* and *Duffy v. Yardi* third because they represent the alternative reading the Note argues should prevail; *Mach v. Yardi* and *NJ AG v. RealPage* fourth as data points on the boundaries; and the DOJ settlement stack last as evidence of the executive-branch articulation of the competitive concern.

### III.A. *Gibson v. Cendyn Group*

*Gibson v. Cendyn Group* concerned hotel-room pricing in the Las Vegas market. The plaintiffs — a putative class of hotel guests — alleged that several Las Vegas Strip hotel operators had each licensed Cendyn's "GuestRev" and "GroupRev" revenue-management software, and that the software, fed with each hotel's occupancy and pricing data and configured to recommend prices, had produced supracompetitive room rates across the Strip.[^42] The District of Nevada dismissed the complaint, and the Ninth Circuit affirmed.[^43] The Supreme Court denied certiorari on April 20, 2026.[^44]

The decision merits careful reading because it has been over-read. *Gibson* did not hold that algorithmic-pricing intermediation can never be horizontal coordination; it did not hold that common adoption of a vendor's software is *per se* lawful; and it did not adopt a rim test under which the only acceptable rim is direct communication among users. What *Gibson* held is narrower and, for that reason, more dangerous. The court treated the challenged contracts as a number of non-horizontal, non-vertical licensing agreements that, on the pleadings, did not restrain competition in the hotel-room market; it emphasized that plaintiffs had not alleged that Cendyn pooled, shared, or used one hotel licensee's confidential information to generate recommendations for another.[^45] The plaintiffs had abandoned a Count I direct-agreement theory at the appellate stage,[^46] which simplified the appeal but also narrowed the holding's controlling reasoning.

Three features of the *Gibson* opinion deserve attention.

*First*, the opinion's ordinary-service-contract framing is a doctrinal move with discrete intellectual content. The court did not deny that the hotel operators all used the same software, that the software processed their nonpublic data, or that the resulting prices were higher than they had been before adoption. The court instead recharacterized the structure of the alleged conduct: each hotel's relationship to Cendyn was a separate bilateral commercial transaction; the connection among hotels ran through Cendyn but did not, on the pleadings, run *to* the other hotels. This recharacterization is what this Note calls a "deadlock-formalizing" move. It is not implausible on the facts the plaintiffs pleaded, but it converts the absence of certain allegations (which the plaintiffs could not plead without discovery) into the absence of horizontal agreement (a substantive conclusion).

*Second*, the opinion's reading of the hub-and-spoke doctrine is restrictive. The court treated *Toys "R" Us* and *Apple e-Books* as available only where the rim consists of inter-spoke communication or contingent compliance — the spoke firms either talked to each other or each conditioned its compliance on the others' compliance.[^47] Algorithmic intermediation that does not involve inter-spoke communication and that proceeds through autonomous user-vendor relationships (without explicit contingent commitments among users) thus falls outside the hub-and-spoke frame as the *Gibson* court understood it. This reading is defensible but not compelled — *Interstate Circuit* itself inferred horizontal agreement without any direct inter-spoke communication.[^48] The narrowness is doing work.

*Third*, the opinion's silence on the cartel-manager account is significant. The Ninth Circuit did not engage Hovenkamp and Leslie's 2011 account substantively. The opinion proceeds as though the only question is whether the alleged conduct fits within the analog hub-and-spoke template, without acknowledging that the technological structure of the alleged conduct is different in kind from the analog cases the template was built to address. The unstated assumption is that the analog template is doctrinally adequate. This Note's central argument is that it is not.

### III.B. *Cornish-Adebiyi v. Caesars Entertainment*

*Cornish-Adebiyi v. Caesars Entertainment*[^50] is the live case. The District of New Jersey dismissed the complaint with prejudice on September 30, 2024, on grounds substantially similar to *Gibson*: the plaintiffs had failed to plead either parallel conduct of the requisite uniformity or pooled data inflows that would support a horizontal-agreement inference.[^51] Before dismissal, the Department of Justice and the Federal Trade Commission filed a Statement of Interest arguing that algorithmic price fixing should not escape § 1 merely because prices are recommended by software or not always followed.[^52] The plaintiffs appealed. On appeal, the American Antitrust Institute and the Open Markets Institute filed amicus briefs urging reversal.[^53] ICLE filed a brief defending the dismissal and urging the Third Circuit to apply conventional agreement doctrine to common software adoption.[^54] An amicus brief from a group of antitrust law and economics professors proposed a "price exchange" framing under which the relevant § 1 violation is the information-pooling itself, presumptively illegal under information-exchange doctrine.[^55]

The Third Circuit's decision in *Cornish-Adebiyi* is the most consequential pending algorithmic-pricing appeal. If the court adopts the cartel-manager framework or a structural variant, the circuit split with the Ninth Circuit becomes pointed and the case for Supreme Court review crystallizes. If the court follows *Gibson*, the pleading-stage deadlock the Note identifies hardens across two circuits and the case for legislative or rule-based response gains force. If the court reverses on narrower grounds — for example, by holding that the district court demanded too much specificity but without articulating an affirmative framework — the Third Circuit will have created room for further development at the district-court level without locking in a doctrine. This Note is principally addressed to the first possibility, but its diagnostic claims survive any of the three.

### III.C. *In re RealPage Antitrust Litigation*

The Multi-District Litigation in *In re RealPage Antitrust Litigation*,[^56] consolidated in the Middle District of Tennessee before Chief Judge Waverly D. Crenshaw, Jr., is the cleanest plaintiff-side counter-precedent. RealPage's "YieldStar" and "AI Revenue Management" products are marketed to multifamily-housing owners as price-recommendation engines that ingest each property's occupancy, lease-up, and pricing data along with broader market signals. The plaintiffs — a putative class of tenants — alleged that the property managers using RealPage had thereby effectively pooled their pricing decisions and that the resulting rents were supracompetitive. Chief Judge Crenshaw denied the motion to dismiss in December 2023, holding that the complaint had plausibly alleged a horizontal agreement and that the conduct should be evaluated under the rule of reason given the vertical aspects of the licensing structure.[^57]

The MDL's reasoning is doctrinally unstable in ways the Note's framework would clarify. The court characterized the alleged conduct as creating both vertical and horizontal aspects, accepted the rule-of-reason framing for the vertical aspects, and allowed the horizontal-agreement theory to survive the motion to dismiss without specifying which plus factors it had credited. The opinion is best read as a pre-doctrinal recognition that the structure of algorithmic intermediation cannot be neatly fit into either vertical or horizontal categories under existing law, paired with a procedural willingness to allow discovery to develop the facts. The Cartel-Manager Plausibility Framework is, in effect, the doctrinal explanation for why Chief Judge Crenshaw's procedural disposition was correct. Without an articulated framework, however, the *In re RealPage* approach is vulnerable to interlocutory appeal and to circuit-court reversal. The framework offered here would harden the disposition into doctrine.

### III.D. *Duffy v. Yardi*

*Duffy v. Yardi Systems, Inc.*[^58] is the most aggressive plaintiff-favorable pleading-stage decision in the algorithmic-pricing space. Judge Robert Lasnik in the Western District of Washington denied Yardi's motion to dismiss in December 2024, holding that the plaintiffs had plausibly alleged a horizontal agreement through Yardi's "RENTmaximizer" pricing software and — crucially — that the alleged conduct could be evaluated under the *per se* rule at the pleading stage.[^59]

*Duffy* matters for two reasons. *First*, the court engaged directly with the question whether the alleged conduct was "more like" horizontal price-fixing or "more like" a vertical licensing arrangement, and resolved the question in favor of the horizontal characterization at the pleadings — without deferring it to summary judgment or trial.[^60] *Second*, the court's *per se* posture is *not* an adjudication that *per se* liability has been proven; it is a holding that the alleged conduct, if proven, would constitute horizontal price-fixing rather than a vertical restraint subject to rule-of-reason review.[^61] The distinction matters because *Duffy* has been over-read by both sides — defense advocacy has characterized it as judicial overreach, plaintiff advocacy as a settled *per se* rule. Neither reading is right. *Duffy* is a pleading-stage characterization decision, no more and no less.

The *Duffy* approach is the closest existing analog to the Cartel-Manager Plausibility Framework proposed here, but it is not identical. *Duffy* operated through judicial discretion, untethered to articulated triggers; the framework this Note proposes would discipline that discretion through specified pleading triggers and a non-exclusive plus-factor list. The benefit of articulation is twofold: it constrains plaintiff-side over-reach (a complaint that does not satisfy the triggers cannot invoke the framework) and it gives defendants a template for rebuttal at the motion-to-dismiss stage.

### III.E. *Mach v. Yardi* (California State Court)

*Mach v. Yardi*,[^62] a Cartwright Act case in the Superior Court of California, granted summary judgment for Yardi on October 6, 2025. The court held that the plaintiffs had failed to produce evidence at the summary-judgment stage that Yardi's software actually used other clients' confidential pricing data in the generation of price recommendations — a factual finding that, if generalizable, would distinguish the *Duffy* and *In re RealPage* fact patterns.[^63] The case is a state-law adjudication and does not control § 1 analysis, but it is a useful data point for two reasons.

*First*, *Mach* illustrates that the conditions for the cartel-manager account to fit are not always present. If a vendor's software uses each user's own data to make a unilateral price recommendation, without aggregating across users, the cartel-manager analogy fails at trigger (B) (nonpublic competitive data inflow). The framework is not over-inclusive; it does not reach this case. *Second*, *Mach* highlights the importance of factual development: the question whether a vendor's software does in fact use rivals' confidential data is precisely the kind of question that cannot be resolved at the pleading stage but can be resolved at summary judgment after discovery. The Cartel-Manager Plausibility Framework is designed to preserve discovery on the data-inflow question; if discovery reveals that no rival data is used, defendants prevail on the merits. This is the framework working as intended.

### III.F. *NJ AG v. RealPage*

The Attorney General of New Jersey's parens patriae action against RealPage and several multifamily defendants[^64] is best treated, at this stage, as a posture-tracking data point rather than a doctrinal pillar. Public company filings indicate that on March 31, 2026, at least one defendant's motion was granted without prejudice as to federal and state antitrust claims and denied as to the state consumer-protection claim.[^65] That posture is too thin to carry the framework's affirmative argument. It does, however, reinforce the descriptive point that courts are sorting algorithmic-pricing complaints through claim-specific pleading screens rather than a settled algorithmic-collusion doctrine.

The Note's substantive engagement with *NJ AG v. RealPage* should therefore remain limited unless the public docket yields a published opinion or order suitable for citation. The doctrinal weight should stay with *Gibson*, *Cornish-Adebiyi*, *In re RealPage*, *Duffy*, and *Mach*.

### III.G. The DOJ Settlement Stack

Three federal consent-decree tracks deserve careful attention.

**Greystar.** The Department of Justice filed a proposed final judgment against Greystar Management Services LLC, the largest U.S. multifamily-property manager, on August 8, 2025; the court entered final judgment on March 2, 2026.[^66] The judgment prohibits Greystar from using nonpublic competitor data in its pricing decisions, prohibits Greystar from attending RealPage's user-group meetings during the consent period, and imposes a court-appointed monitor.[^67] State attorneys general also secured a separate civil settlement on parallel grounds.[^68] *Greystar* is not binding precedent, but it is a judicially entered antitrust consent judgment, not merely agency commentary.

**RealPage.** The DOJ's proposed final judgment against RealPage, filed November 24, 2025, is the most ambitious of the three.[^69] It prohibits RealPage from using current or historical unaffiliated-property nonpublic data in the runtime operation of covered revenue-management products, subject to narrow exceptions, and permits aged backward-looking unaffiliated data only for limited model-training uses.[^70] It requires removal or redesign of features that, in DOJ's characterization, deter price decreases or align prices among users.[^71] It requires RealPage to cease facilitating discussion of nonpublic data and pricing strategies at RealPage RMS meetings.[^72] It provides for a court-appointed monitor and for RealPage's cooperation with DOJ in its remaining cases against multifamily defendants.[^73] As of the May 10, 2026 public-source check, DOJ public materials continued to reflect a proposed-judgment/Tunney Act posture rather than a publicly posted entered final judgment.[^75]

**LivCor.** The proposed consent decree against LivCor (a Blackstone portfolio company) was filed on December 23, 2025, in the Middle District of North Carolina.[^76] Its terms substantially track the *Greystar* and *RealPage* templates, with optional monitor coverage for non-certified third-party software.[^77]

The settlement stack has two doctrinal uses for this Note. *First*, the consent decrees collectively articulate a coherent enforcement-line: nonpublic forward-looking data inflow, design features deterring decreases, vendor monitoring, and vendor-organized user meetings are red-flag features under the Antitrust Division's working theory. The triggers in Section V's Cartel-Manager Plausibility Framework track this articulation almost line-for-line. *Second*, the settlement stack is *evidence* of the executive-branch theory of competitive concern, but it is *not* law. None of the three settlements creates binding precedent on courts adjudicating private § 1 claims. The Note treats the settlement stack with the appropriate care: as a reference point for understanding which features the enforcement community treats as concerning, not as the doctrine itself.

### III.H. What the Case Pattern Can Show

This Note's case survey is qualitative, not a completed empirical study. The post-2023 opinions and consent decrees are still too few, too heterogeneous, and too procedurally uneven to support confident causal inference. Their value is narrower but still important: they identify recurring features that courts and enforcers already treat as legally salient. Common vendor adoption, nonpublic data inflow, acceptance-rate allegations, override friction, vendor monitoring, and user-group meetings recur in the cases that survive or settle on government-favorable terms; their absence or negation does real work in cases like *Gibson* and *Mach*. That pattern supports the framework as a doctrinal synthesis. A later empirical extension could code those features systematically, but the argument here does not depend on regression output.[^78]

---

## IV. The Procedural Deadlock After *Gibson*

This Section makes the descriptive procedural claim that organizes the Note's argument: *Gibson*'s now-final holding has produced a structural deadlock at the *Twombly* pleading threshold for § 1 challenges to algorithmic-pricing intermediation, and that none of the existing doctrinal vehicles can close the deadlock without either substantive over-reach (the *Duffy* approach without articulated triggers) or under-enforcement (the *Gibson* approach without a discovery-unlocking mechanism). The Section's contribution is reframing — making visible the procedural architecture inside which the substantive debate is occurring — rather than the affirmative proposal that follows in Section V.

### IV.A. The Architecture of the Deadlock

The deadlock has four moving parts.

*First*, the substantive law of § 1 requires plaintiffs to plead — at the *Twombly* threshold — facts that plausibly allege concerted action and that exclude the inference of independent parallel conduct.[^79] The plausibility requirement is not satisfied by allegations of parallel pricing changes or by inferences from market structure alone.[^80] Plaintiffs must allege something that distinguishes coordinated conduct from interdependent oligopoly behavior.

*Second*, in the analog cases that built the doctrine, the distinguishing facts were within plaintiffs' reach pre-discovery. Industry meetings could be observed. Trade-association communications could be subpoenaed at the state-action stage. Phone records could be obtained from common carriers. Internal memoranda surfaced in regulatory proceedings or in prior litigation. The information asymmetry between plaintiffs and defendants was meaningful but not categorical; *Twombly* itself was decided in a context in which the relevant facts (the incumbent local exchange carriers' coordination decisions) were difficult but not technically impossible to allege. Whatever else *Twombly* did, it did not contemplate a litigation environment in which the distinguishing facts were unavailable in principle without discovery.

*Third*, algorithmic intermediation produces precisely that environment. The objective function the algorithm optimizes is proprietary. The data that flow into the algorithm at runtime are the user firm's own private inputs and (depending on architecture) the vendor's accumulated cross-user data. The vendor's monitoring of user implementation occurs through internal vendor systems. The acceptance rate is a vendor metric. Each of these facts is dispositive of whether the cartel-manager account fits. None is observable to a plaintiff before discovery. The structural information asymmetry is not occasional but pervasive.

*Fourth*, the post-*Gibson* case law has, in effect, deemed the unavailable facts essential to plausibility. *Gibson*'s requirement that plaintiffs allege either inter-licensee data sharing or some equivalent rim is a requirement that plaintiffs allege facts they cannot observe. The court did not say that explicitly; it said only that the absence of such allegations doomed the complaint. But the operational consequence is that the unobservability of the dispositive facts has been promoted to dispositive in itself. This is the deadlock.

The deadlock does not occur in every § 1 case. In a traditional horizontal price-fixing case — agents from competing firms meeting at a hotel and agreeing on prices — the dispositive facts are, in principle, available pre-discovery from email records, witness reports, and the kind of circumstantial evidence that survived *Twombly* in conventional conspiracies. The deadlock is specific to algorithmic intermediation because the locus of coordination has been moved out of the firm boundary into a third-party computational system whose internal architecture is, by design, opaque to outsiders.

A calibrating point. The "deadlock" framing should be read with care. The post-*Gibson* environment is not a categorical bar on § 1 algorithmic-pricing cases — *Duffy v. Yardi* survived *Twombly* with detailed allegations about Yardi's user-group meetings, dashboard architecture, and override-friction features, and the *RealPage* MDL similarly survived under a rule-of-reason posture.[^calibration1] The case for the framework can be made, with similar force and arguably greater conservatism, as a *predictability and articulation* problem rather than a categorical deadlock: the existing doctrine produces unpredictable and inconsistent outcomes, with sufficient pleading specificity sometimes succeeding and sometimes failing, and the framework offered here is the articulated architecture that allows the pleading inquiry to be conducted predictably across cases. Either pitch — deadlock-breaking or predictability-enhancing — supports the framework. The substantive analysis that follows is the same; the rhetorical register is calibrable to the reader. This Note's prior framing has emphasized the deadlock-breaking pitch; the predictability-enhancing pitch is a friendly reformulation that survives the same diagnostic.

The distinction between *difficult-to-observe* facts and *structurally unobservable* facts is doctrinally critical and deserves to be drawn with care. *Twombly* and its progeny have always contemplated cases in which plaintiffs face evidentiary disadvantage relative to defendants. The *Twombly* plaintiffs themselves alleged conduct (incumbent local exchange carriers' coordination on entry decisions) whose internal documentation was uniformly within defendants' control; the Court nonetheless treated their evidentiary position as ordinary rather than exceptional, requiring them to plead facts plausibly inconsistent with independent action.[^twombly1] The same is true across the post-*Twombly* § 1 case law: plaintiffs ordinarily face evidentiary asymmetry, and ordinary asymmetry does not suspend the plausibility requirement. To argue that algorithmic-intermediation cases are different, the Note must identify the specific feature that distinguishes them — and the feature must be doctrinally cognizable, not merely a difference of degree.

The feature is the architectural difference between *concealment* and *non-existence in observable form*. In a traditional horizontal price-fixing case, the relevant facts exist in observable form somewhere — in an email, in a witness's memory, in a meeting record — and are merely concealed from plaintiffs by defendants' refusal to share. The plausibility requirement, in such cases, calibrates the threshold for unlocking discovery to extract observable-but-concealed facts. In an algorithmic-intermediation case, by contrast, the relevant facts about the algorithm's objective function, the data-flow architecture, the override rate, and the monitoring intensity often *do not exist in observable form outside* the vendor's computational system. They are not facts that a witness has observed and is refusing to disclose; they are facts that exist only as states of the system and as outputs the system generates internally. The pre-discovery position of plaintiffs in such cases is not "concealed but discoverable"; it is "computational and only system-internally observable." The plausibility threshold, applied without modification, calibrates a discovery-unlocking standard to a fact-set that does not match the standard's underlying assumption.

This is the architectural insight that drives the framework. The framework is not a special pleading rule for a category of cases the substantive antitrust law treats as more important; it is a recalibration of the plausibility threshold to fit the structural-evidentiary economics of cases in which the dispositive facts are computationally rather than testimonially situated. The recalibration is doctrinally modest in the sense that it does not displace *Twombly* or *Iqbal*; it operationalizes their plausibility requirement for a fact-set the analog cases did not foresee. The recalibration is, however, doctrinally non-trivial in the sense that it draws a line — between the algorithmic and the analog — that the existing case law has not yet drawn. The line is defensible on the architectural ground that the algorithmic and the analog produce different evidentiary economics, and the plausibility threshold should track those economics rather than impose a uniform standard that systematically over-screens one category and under-screens the other.

A skeptic might respond that the line is unstable: many traditional cases also involve facts existing only in defendants' systems (corporate accounting records, internal communications encrypted by privilege, etc.), and the plausibility threshold has not historically distinguished such cases. The reply is that those facts, while not directly observable, are reducible to testimony — a witness with knowledge of them can describe them, an internal investigation can surface them, a regulatory inquiry can extract them. Algorithmic objective functions and runtime data flows are reducible to testimony only at the level of abstraction at which abstraction loses doctrinal usefulness. A vendor employee can testify that "the algorithm uses competitor data" or "the algorithm aims at high acceptance rates"; the testimony does not, however, answer the dispositive question of whether the algorithm's coordination function tracks the four-function cartel-manager pattern, because the pattern is a structural feature of the system's input-output behavior under specified counterfactual conditions, not a feature any single witness has observed. The framework's triggers are calibrated to what plaintiffs *can* allege about the system from publicly observable features (vendor marketing, user testimonials, regulatory disclosures, documented industry practices); the merits inquiry is reserved for what the system *actually does*, developed through targeted discovery into the system itself. This is the doctrinally cognizable distinction the framework asks the courts to draw.

### IV.B. The Information Asymmetry Is Designed In

It is worth pausing on the second point. The information asymmetry is not an unfortunate side effect of complex technology; it is intrinsic to the value proposition algorithmic-pricing vendors sell. Each user firm pays the vendor in part *because* the vendor processes information the user firm could not assemble unilaterally, including (in the architecture this Note's framework targets) information about the user firm's competitors. The fact that the user firm cannot fully audit the vendor's data flows is what makes the vendor's recommendations valuable. The fact that competing user firms cannot audit each other's data flows is what makes the coordinated outcome possible without explicit communication. The opacity is a feature, not a bug.

This is significant for *Twombly* analysis because it inverts the assumption underlying plausibility doctrine. *Twombly*'s anxiety about discovery cost is calibrated to a baseline in which the facts plaintiffs need are difficult but obtainable through ordinary investigation; the plausibility requirement protects defendants against fishing expeditions for facts that, the system assumes, plaintiffs could already discover for themselves. In the algorithmic-intermediation context, the assumption fails. The facts that distinguish coordinated conduct from independent parallel conduct are not difficult-but-discoverable; they are unavailable in principle. To require plaintiffs to plead such facts is to require them to do what cannot be done.

### IV.C. *Gibson*'s "Multiple Independent Verticals" Framing as Deadlock-Formalizer

*Gibson* did not introduce the asymmetry; it inherited it. What *Gibson* did was give it doctrinal form. The ordinary-service-contract framing is, on its surface, a descriptive characterization of the alleged conduct: each hotel had its own contract with Cendyn, the algorithm ran on each hotel's data, and no horizontal contract among hotels was alleged. As a description, the framing is unobjectionable. But descriptions do legal work, and this one does the work of converting a fact about the architecture of the alleged conduct (the absence of inter-spoke contracting) into a conclusion about the substantive question (the absence of horizontal agreement).

The conversion would be defensible if the absence of inter-spoke contracting were probative of the absence of horizontal coordination. In analog cases, it often is. In algorithmic-intermediation cases, it is not. The whole point of the cartel-manager account is that horizontal coordination can be achieved without inter-spoke contracting if the intermediary performs the coordination function. *Gibson*'s framing assumes the irrelevance of the cartel-manager account, but it does not engage the account directly. The framing is doctrinally unstable: it relies on a substantive premise (the cartel-manager account does not apply) that the opinion does not defend. This Note's affirmative argument, in part, is that the premise is wrong on the conditions specified in Section V.

### IV.D. California AB 325 § 16756.1 as Comparative Lever

It is useful to compare the federal deadlock to California's response in AB 325. The California legislature, in amending the Cartwright Act effective January 1, 2026, included a provision (§ 16756.1) explicitly relaxing the pleading standard for claims involving "common pricing algorithms" — defined as algorithms used by two or more firms incorporating competitor information.[^81] The provision is a state-level legislative answer to the same diagnostic the Note offers: federal pleading doctrine has produced under-enforcement that, on the legislature's view, requires correction.

The California response is informative in two ways. *First*, it is evidence that the deadlock is real — legislatures do not relax pleading standards in response to imaginary problems, and the bipartisan California legislative coalition that produced AB 325 is not naturally disposed toward antitrust expansion. *Second*, it is evidence that the deadlock can be addressed at the procedural rather than the substantive level: the California response did not categorically ban algorithmic-pricing intermediation (as New York's S.7882 did for residential rent-setting algorithms), did not impose substantive *per se* liability, and did not preempt federal antitrust law. It modified the pleading standard. The federal answer this Note proposes is structurally analogous, except that it operates within existing federal pleading doctrine through judicial elaboration rather than legislative amendment.

The federalism implications are taken up in Section VI.

### IV.E. Why Traditional Plus-Factor Analysis Does Not Solve the Problem

The skeptic's first response is that the deadlock is illusory: plus-factor analysis under *Theatre Enterprises*[^82] and its progeny has always allowed plaintiffs to allege circumstantial markers without alleging the smoking gun, and algorithmic-intermediation cases should fit comfortably within that tradition. The response is not unserious, and Section II.B addressed the analog version. The point worth making here is procedural rather than substantive.

Plus-factor analysis works well when the plus factors are themselves observable to plaintiffs pre-discovery. In analog cases, plaintiffs typically have access to plus-factor evidence (industry meetings, public price-trajectory data, correspondence surfaced through public records or prior litigation, regulatory filings) before they file. The plus factors are the gateway to discovery, and the gateway is open because the plus-factor evidence is observable.

In algorithmic-intermediation cases, the most probative plus factors — override rate, vendor monitoring intensity, acceptance rate, data flow architecture, objective-function specification — are themselves locked behind the same information asymmetry that makes the underlying conduct unobservable. Plaintiffs can plead the user firms' adoption of the vendor; the vendor's marketing claims about acceptance rate; the vendor's user-group meetings; and (where surfaced through investigative journalism, regulatory action, or whistleblower disclosure) some specific design features. They cannot plead the actual override rate, the actual acceptance rate, the actual data flows, or the actual objective function. The plus-factor analysis under *Theatre Enterprises* either over-credits the alleging-side facts (in which case it functionally resembles the trigger-based framework this Note proposes) or under-credits them (in which case it reproduces the deadlock).

The Cartel-Manager Plausibility Framework is, in a sense, the doctrinally honest version of plus-factor analysis adapted to the algorithmic-intermediation context. It identifies the plus-factor pattern that does the actual work in the post-*Gibson* case law — common adoption among rivals, nonpublic data inflow, alignment-predisposing features — and makes that pattern operate transparently rather than through ad hoc plus-factor weighting.

### IV.F. The Hub-and-Spoke Doctrine Cannot Be Stretched

A second skeptic's response is that hub-and-spoke doctrine, properly understood, already reaches the algorithmic-intermediation case. On this view, *Toys "R" Us* and *Apple e-Books* support a "constructive rim" reading under which the spokes' common adoption of the hub's coordination plan, paired with awareness of each other's adoption, suffices for horizontal-agreement findings.[^83] The defense would then be that *Gibson* misread the doctrine and that the Third Circuit, in *Cornish-Adebiyi*, can correct the misreading without any new doctrinal architecture.

The constructive-rim reading is plausible and, on the merits, this Note is sympathetic to it. But two considerations push toward articulation rather than re-interpretation. *First*, the constructive-rim reading still requires plaintiffs to allege awareness — that each spoke knew of the others' compliance — and the evidence of awareness in the algorithmic context is itself partially obscured by the technology. Vendor user-group meetings are evidence of awareness, but the inferential chain requires either explicit allegations of attendance and content (which discovery would be needed to confirm in detail) or allegations sufficient to support an inference of awareness from the vendor's marketing claims. The framework offered in Section V handles awareness through the conjunction of trigger (A) and the plus-factor list, which is a more transparent treatment than constructive-rim re-interpretation. *Second*, doctrinal incrementalism has costs. A circuit-court opinion in *Cornish-Adebiyi* that adopts a constructive-rim reading will leave open the question whether the reading applies to algorithmic-intermediation contexts that do not involve user-group meetings or vendor-marketed acceptance rates. The Cartel-Manager Plausibility Framework answers that question affirmatively (the trigger conjunction governs); the constructive-rim reading leaves it for case-by-case development.

This Note does not insist on its own framework as the only path. If the Third Circuit prefers the constructive-rim path, the diagnostic claim of Section IV is vindicated either way. The framework in Section V is the most defensible articulation of where the law should go; the constructive-rim path is the most modest articulation that would adequately address the deadlock.

### IV.G. Judicial Competence and the Institutional Question

A final point about Section IV's diagnostic before the Note moves to its affirmative proposal. Even if the deadlock is real and the analog vehicles cannot close it, an attentive reader may ask why the appropriate response is judicial elaboration of pleading doctrine rather than legislative or rule-based action. Two institutional alternatives present themselves: Congress could amend the Sherman Act or enact a sectoral statute; the Judicial Conference, through the Civil Rules Advisory Committee, could amend Rule 8 or Rule 12. Either alternative would dispose of the deadlock without asking courts to articulate doctrine the analog cases did not foresee.

The institutional case for judicial elaboration over legislative or rule-based action rests on three considerations.

*First*, the plausibility regime is itself a judicial elaboration of Rule 8(a)'s minimal requirement. The pre-*Twombly* baseline — *Conley v. Gibson*'s "no set of facts" formulation[^conley1] — was substantially relaxed by *Twombly* and *Iqbal* through judicial doctrinal development, not through Rule amendment. The Court's institutional posture toward Rule 8 has been one of common-law-style elaboration calibrated to particular evidentiary contexts: *Twombly*'s anxieties were specifically about the discovery economics of mass-conspiracy cases, not about civil pleading generally, and *Iqbal* extended the framework while preserving the contextual calibration. The framework offered here is the same kind of move — judicial elaboration of the contextual calibration *Twombly*/*Iqbal* expressly invited — applied to an evidentiary context the analog cases did not foresee.

*Second*, the institutional alternatives are poorly suited to the calibration problem. Legislation requires Congress to commit to a textual specification (the conjunctive triggers, the rebuttal mechanism, the implementation-rate-as-plus-factor innovation) that may not survive contact with cases at the boundaries — and that, once committed, is hard to revise. Rule amendment shares this rigidity, with the additional cost of operating across all civil litigation rather than within § 1 doctrine specifically. Both alternatives also raise federalism complications that judicial doctrinal elaboration avoids: a federal sectoral statute on algorithmic pricing would face contested preemption questions vis-à-vis state antitrust statutes, and a Rule amendment to handle one pleading context would invite collateral consequences across unrelated areas of law. The framework operates through the mechanism the substantive antitrust law already uses for handling evidentiary calibration — the contextual application of *Twombly*'s plausibility requirement — and confines its effects to the specific § 1 doctrinal area to which it applies.

*Third*, the Note's framework is more reversible by ordinary judicial means than legislation or Rule amendment would be. If experience reveals that the framework's triggers are over-inclusive (sweeping in too many efficiency-generating uses) or under-inclusive (missing too many genuinely coordinative uses), courts can refine the triggers through ordinary case-by-case adjudication, just as plus-factor doctrine has been refined since *Theatre Enterprises*.[^theatre2] Legislative or rule-based responses lock in their original specification at correspondingly higher revision cost. Where the underlying empirical and economic understanding is still developing — as it is for algorithmic pricing — the institutional flexibility of judicial doctrinal elaboration is a feature, not a deficiency.

The institutional case is not exclusive. Legislation may have appropriate roles where the framework is structurally inadequate (as in narrow categorical contexts where state-level legislatures have already acted, or in adjacent contexts the framework does not reach). The argument is more modest: in the doctrinal space *Gibson* has formalized and that this Note seeks to address, judicial elaboration through the framework offered in Section V is institutionally more appropriate than the legislative or rule-based alternatives. The framework is, in this sense, a court-led response to a court-created problem — *Twombly*/*Iqbal* in interaction with *Gibson*'s reading of § 1 doctrine — and the institutional logic of doctrinal calibration favors the court-led response.

---

## V. Operationalizing the Cartel-Manager Account

This is the heart of the Note. Section V presents the Cartel-Manager Plausibility Framework — its triggers, its plus-factor list, its rebuttal mechanism, its substantive agnosticism, and its application to the cases mapped in Section III. The Section is organized to be self-contained: a court adopting the framework should be able to read Section V alone and have the necessary doctrinal architecture in hand.

### V.A. The Hovenkamp–Leslie Cartel-Manager Account, Recapitulated

A preliminary point about doctrinal architecture before the substantive recap. Section 1 reaches contracts, combinations, and conspiracies in restraint of trade among "persons" within the meaning of the Sherman Act.[^vendor-person] The agreement § 1 reaches in the algorithmic-intermediation context runs *among the user firms*, not among the firms and an algorithm. Algorithms are property; they are not Sherman Act persons.[^algo-property] The framework offered here is consistent with — indeed, depends on — the conventional architecture under which the user firms' conjunctive conduct *is* the agreement, and the vendor (a Sherman Act person) is either a participant in that agreement (as the Justice Department has alleged against RealPage) or a non-participant facilitator through whom the agreement is implemented (the *Interstate Circuit* pattern in which the film distributor never agreed to anything but coordinated the exhibitors' compliance).[^vendor-architecture] This Note adopts the *Interstate Circuit* characterization throughout: the agreement is among user firms, instantiated by their conjunctive trigger-satisfying conduct; the vendor is the implementation mechanism through which the agreement operates. Where the developed record shows that the vendor was an active co-conspirator, conventional § 1 doctrine reaches the vendor as a participating "person" without requiring any innovation; the framework's contribution is to the threshold determination of whether the user-firm agreement has been plausibly alleged, not to the substantive question of whether the vendor is a conspirator.

The 2011 article begins from a pattern that Hovenkamp and Leslie argue antitrust doctrine has incompletely theorized: successful cartels often operate through a coordinating actor or structure whose role is not to compete in the cartelized market but to organize the conduct of those who do.[^84] Their account emphasizes trade associations, common sales agents, centralized management structures, and *Sealy*/*Topco*-type arrangements in which formally vertical or single-entity structures perform cartel functions.[^84a] The doctrinal analogues surveyed above — including *Interstate Circuit*, *Toys "R" Us*, and *Apple e-Books* — show why that functional pattern matters at the pleading stage. The article's contribution is to organize these patterns under a unified analytical category — the *firm as cartel manager* — and to argue that § 1 doctrine should reach the coordinating actor directly, on the same theory under which it reaches the coordinated firms.

Within this category, Hovenkamp and Leslie identify four functions whose conjunction characterizes cartel management.[^84b] The first is *centralized pricing authority* — the cartel manager exercises operative control, formally or effectively, over the prices the cartelized firms charge, whether by setting prices outright, by recommending prices the firms predominantly follow, or by structuring the firms' pricing decisions in ways that produce convergent outcomes. The second is *information aggregation and recommendation distribution* — the manager collects competitively sensitive information from cartel members (cost data, demand data, capacity data, pricing intentions) and uses that information to generate the pricing direction the cartel collectively follows. The third is *compliance monitoring* — the manager tracks whether members are pricing in accordance with the cartel's program, typically through reporting requirements imposed on members or through independent monitoring of market prices. The fourth is *enforcement of discipline* — the manager creates costs for defection, either by imposing direct sanctions (expulsion, fee penalties, contract restrictions) or by structuring the cartel architecture so that defection is unilaterally unprofitable.

Hovenkamp and Leslie's normative argument is that an entity performing these four functions is doing the work of a cartel — its conduct is the cartel — regardless of whether the entity is itself a competitor in the cartelized market.[^84c] The article rejects the proposition that § 1 doctrine should be understood to require, as a structural matter, that the coordinator be one of the coordinated firms. Section 1 reaches "every contract, combination ... or conspiracy" in restraint of trade, and the cartel manager is unambiguously a "person" within the meaning of the statute. The article's doctrinal target is a tendency in some lower-court reasoning to treat the cartel manager as a mere facilitator whose conduct is parasitic on the underlying firm-firm agreement, rather than as a § 1 conspirator in its own right.

Three features of the account matter for this Note's operationalization.

*First*, the four functions are characterizing, not exhaustive. Hovenkamp and Leslie do not argue that an entity performing only some of the functions is not a cartel manager; they argue that an entity performing all four is paradigmatically one. The framework offered here treats the four functions as conjunctive (and the triggers as conjunctive) precisely to maintain the paradigmatic fit. An algorithmic intermediary that performs only one or two of the functions does not raise the cartel-manager pattern, and the framework's triggers will not be satisfied.

*Second*, the account is functionally rather than formally specified. Hovenkamp and Leslie are not asking whether the coordinator labels itself a "cartel manager" or whether the cartelized firms have signed an explicit cartel charter; they are asking whether the structural pattern of the four functions is in operation. This is the right level of analysis for algorithmic intermediation, where the formal labels are uniformly innocuous (the vendor is a "software licensor" or "yield-management partner") and the operative question is what the system does, not what it is called.

*Third*, the account is normatively substantive but doctrinally restrained. Hovenkamp and Leslie do not propose a per se rule for cartel management, do not propose a pleading-stage trigger-and-rebuttal mechanism, and do not propose any specific procedural innovation. Their argument is that existing § 1 doctrine, properly applied, already reaches the cartel manager — and that the analytical category of cartel management is useful for organizing the cases in which the doctrine has so reached. The framework offered here makes a procedural contribution that Hovenkamp and Leslie did not make. It does not, however, displace any element of their substantive analytical structure.

The fit with algorithmic intermediation is functional and conditional, not categorical. Each of the four cartel-manager functions corresponds to a structural feature that algorithmic intermediation *can* but does not necessarily perform. *Centralized pricing authority* corresponds to the user firms' delegation of pricing discretion through autopilot defaults, override friction, or sufficiently strong vendor influence that recommendations are predominantly accepted — which is trigger (C) in the framework. *Information aggregation and recommendation distribution* corresponds to the algorithm's processing of nonpublic, forward-looking, competitively sensitive data from rival users — trigger (B). *Compliance monitoring* corresponds to the vendor's tracking of acceptance and override behavior — a plus factor under (C)(iii) — and to the broader pattern of vendor-mediated awareness. *Enforcement* corresponds to the architectural features that make defection costly — anti-undercut design (C)(vi), commission penalties (C)(ii), market-wide dashboards (C)(v) — supplemented by the inherent enforcement properties of structural over agreement-based coordination. The framework's three triggers, taken together, are the procedural articulation of the four-function fit.

The illustrative counterexamples discipline the framework's reach. A payment processor that touches the prices charged by competing merchants performs none of the four functions: it neither aggregates competitive information for pricing purposes, nor exercises pricing authority, nor monitors price compliance, nor enforces discipline. A market-data vendor that publishes anonymized aggregated indices may aggregate information, but it does not exercise pricing authority and does not monitor compliance — its conduct does not fit. A pricing algorithm that uses only the user firm's own data, however sophisticated, may exercise centralized pricing authority over that user, but it does not aggregate competitive information from rivals and does not coordinate among them — its conduct does not fit. *Mach v. Yardi*'s factual finding (no use of other clients' confidential data) places the *Mach* defendant outside the cartel-manager pattern on this exact ground.[^84d] Each of these counterexamples corresponds to a trigger failure in the framework's procedural architecture, and the procedural architecture is calibrated precisely to track the substantive cartel-manager account. The fit is tight by design.

### V.B. The Three Triggers

The Cartel-Manager Plausibility Framework is triggered by a complaint that plausibly alleges all three of the following.

#### V.B.1. Trigger A: Competitively Significant Common Adoption

The first trigger is competitively significant common adoption of a pricing intermediary among horizontal rivals in a properly pleaded relevant market. Three points unpack the trigger.

*First*, "competitively significant" is a market-share concept tied to the relevant antitrust market the complaint pleads. The framework is not satisfied by a numerical "three or more firms" rule. Two horizontal rivals using a common intermediary do not, without more, present a cartel-manager problem; their conduct should be analyzed under traditional § 1 doctrine. Conversely, three rivals using a common intermediary in a market in which they collectively account for less than 10% of sales do not present a competitively significant problem either. The framework's pleading benefit is reserved for cases in which common adoption involves a sufficient share of the market that the coordination function, if performed, would likely have market effects. Market-by-market analysis is appropriate, with the burden on the complaint to plead share figures plausibly.

A court adopting the framework should articulate anchoring guidance for the competitively-significant inquiry, drawing on the conventional concentration benchmarks that govern adjacent doctrinal areas. Three benchmarks are useful comparators. *Merger-analysis HHI thresholds* under the 2023 Merger Guidelines treat a transaction as presumptively concerning when post-merger HHI exceeds 1,800 with an HHI delta above 100, and as highly concerning above 2,400 HHI with a delta above 200.[^81a] Translated to the algorithmic-intermediation context, common adoption among rivals whose combined share — treated as a notional joint share for purposes of the analogy — produces HHI contributions in or above this range plausibly satisfies competitive significance. *Joint-venture concentration thresholds* under the antitrust treatment of competitor collaborations operate at a similar order of magnitude.[^81b] *Information-exchange precedent*, in cases like *United States v. United States Gypsum*[^81c] and the trade-association line, has treated information sharing among rivals collectively accounting for substantial shares of a properly defined market as the trigger for serious antitrust scrutiny. None of these benchmarks is doctrinally determinative for the framework's trigger (A), but each provides articulable guidance against which a court can calibrate competitive significance in the case before it.

The framework's deliberate refusal to commit to a single numerical threshold reflects a doctrinal principle, not vagueness. Market structures vary enough across the contexts in which algorithmic intermediation operates — multifamily housing differs from hotel rooms, hotel rooms from ride-sharing, ride-sharing from agricultural commodities — that a fixed threshold appropriate to one context may be plainly inappropriate to another. Courts have managed similar variability in merger HHI analysis, in joint-venture review, and in dominance analysis under § 2; they can manage it here. The plausibility burden imposed by trigger (A) is a real one — vague pleadings about "common adoption" without share figures will not satisfy it — but it is not a numerical-threshold burden, and articulating it as if it were would be inconsistent with the structural logic of the substantive antitrust law trigger (A) operationalizes.

*Second*, "horizontal rivals" requires that the user firms be actual competitors in the same antitrust market, not firms in adjacent or unrelated markets. The trigger is not satisfied by, for example, a pricing algorithm used by airlines and by hotel chains, even if the same vendor licenses the software to both, because airlines and hotel chains do not compete in the same antitrust market. The trigger requires within-market common adoption.

*Third*, "properly pleaded relevant market" engages the standard market-definition rigor. A complaint that pleads a vaguely-defined product or geographic market will fail at trigger (A) regardless of how compelling its other allegations are. This is a virtue, not a vice: market definition is the conventional mechanism for ensuring that antitrust scrutiny is calibrated to actual competitive harm, and importing it into the cartel-manager framework prevents the framework from being weaponized against routine common-vendor adoption in markets where the adoption has no plausible competitive consequence.

#### V.B.2. Trigger B: Nonpublic Competitive Data Inflow

The second trigger is the flow of nonpublic, forward-looking, competitively sensitive data from the rival user firms into the intermediary's runtime operation. Each adjective is doing work.

*Nonpublic*: data that the rival user firms have not disclosed publicly. Public data — published price indices, government-released occupancy or rental statistics, advertised list prices — does not raise the same concerns. The Department of Justice's *RealPage* settlement draws the same line.[^85]

*Forward-looking*: data that bears on prospective pricing or competitive strategy, as opposed to historical data that has already been incorporated into past prices. The DOJ–RealPage settlement permits "aged" backward-looking data of at least twelve months' staleness while prohibiting forward-looking inflows.[^86] The forward-looking element is the doctrinally critical one: it is the prospective sharing that creates the coordination opportunity, because it allows the algorithm to recommend prices that anticipate rivals' moves rather than respond to rivals' past behavior.

*Competitively sensitive*: data whose sharing among competitors would, under traditional information-exchange doctrine, raise concern.[^87] The conventional categories — pricing, capacity, demand forecasts, output, costs — are appropriate. Generic operational data (e.g., HR practices, software-usage analytics) is not.

*Inflow into runtime operation*: the data must in fact reach the algorithm's price-recommendation generation, not merely be received and stored by the vendor for some other purpose. The trigger excludes vendors that maintain data silos, that anonymize and aggregate data before incorporation, or that use the data only for capacity-planning or non-pricing purposes. This is consistent with the *Mach v. Yardi* factual finding that the Yardi software did not use other clients' confidential pricing data;[^88] under the framework, that finding would defeat trigger (B) and the framework would not apply to that case.

The trigger is conjunctive: a complaint must plausibly allege all four adjectives, not merely that "data flows" between users and the vendor. This is a meaningful pleading burden, and one designed to filter out cases in which the algorithmic intermediation does not raise cartel-manager concerns.

#### V.B.3. Trigger C: At Least One Alignment-Predisposing Feature

The third trigger is the presence of at least one alignment-predisposing design or use feature. The non-exclusive catalog includes:

(i) *Autopilot defaults* — algorithm-set prices adopted without case-by-case user review.

(ii) *Override friction* — commission penalties, contract restrictions, status loss, or other consequences for user firms that decline to follow the algorithm's recommendations.

(iii) *Active vendor monitoring* of user implementation — the vendor tracks whether users are accepting or overriding recommendations and uses the information operationally.

(iv) *Vendor-organized "user group" meetings* sharing nonpublic data — the vendor convenes user firms in fora at which competitively sensitive information is exchanged, formally or informally.

(v) *Market-wide dashboards* visible to multiple users — the vendor provides a graphical or numerical interface displaying market-level pricing or capacity information drawn from user data.

(vi) *Contractual or design features deterring price decreases* — the algorithm's design or the licensing contract's terms make unilateral price reductions costly or technically difficult.

(vii) *Vendor marketing claims of high acceptance rates* — the vendor's marketing materials advertise to prospective users that existing users follow the algorithm's recommendations at high rates, which (if true) is structural evidence of delegation and (if even alleged) is itself a fact within the public sphere that the user firms are deemed aware of when adopting the system.

The trigger requires only that one of the seven categories be plausibly alleged. The list is non-exclusive — courts should be open to additional features that fit the same functional pattern (centralized authority, monitoring, enforcement). Three further points.

The seven categories are not arbitrary. Each tracks one of three structural features the cartel-manager account treats as functionally definitive. Categories (i) *autopilot defaults* and (ii) *override friction* track the *centralized-pricing-authority-by-delegation* function: they are the operational mechanisms by which user firms surrender pricing discretion to the algorithm, either passively (autopilot) or by costly counter-action (friction). Categories (iii) *active vendor monitoring*, (iv) *vendor-organized user-group meetings*, and (v) *market-wide dashboards visible to multiple users* track the *monitoring* function: they are the operational mechanisms by which the vendor (or, through the vendor, the user community) tracks compliance with the algorithmic recommendation regime. Categories (vi) *contractual or design features deterring price decreases* and (vii) *vendor marketing claims of high acceptance rates* track the *enforcement* function: (vi) is the architectural enforcement mechanism that makes defection costly, and (vii) is the public-knowledge-based mechanism that creates the awareness on which structural enforcement depends (a user firm declining to follow recommendations does so knowing that other firms will follow, and that defection will not be reciprocated). Together the seven categories instantiate the four cartel-manager functions of Section V.A — delegation, information-aggregation-and-recommendation (which is built into trigger (B), not (C)), monitoring, and enforcement — through the operational features that algorithmic intermediation actually exhibits. The catalog is non-exclusive precisely because the same three structural features (delegation, monitoring, enforcement) can manifest through additional operational mechanisms that future cases will surface; courts adopting the framework should be open to such mechanisms when they fit the structural pattern.

Two further points.

First, the trigger explicitly does *not* require plaintiffs to plead the actual override rate or acceptance rate. As Section IV.E noted, those facts are typically unobservable to plaintiffs pre-discovery. Treating implementation rate as a *plus factor* (allegations of vendor marketing claims about acceptance count) rather than as an *element* (proof of actual rates is required) is one of the framework's central procedural innovations.

Second, the seven categories are deliberately heterogeneous in evidentiary requirements. Categories (iv), (v), and (vii) are typically observable to plaintiffs from public sources or industry knowledge. Categories (i), (ii), (iii), and (vi) often require some indirect inference, drawn from vendor marketing materials, customer testimonials, regulatory disclosures, or whistleblower reporting. The framework does not insist that any particular category be present in any particular complaint; the conjunctive structure (one of seven) is calibrated to the realistic evidentiary economics of pleading.

### V.C. The Pleading Shift and Its Rebuttal

Triggering all three elements creates a structured inference that the complaint plausibly alleges § 1 agreement. Several features of that inference deserve precision.

*The inference is pleading-stage only.* It operates only at the motion-to-dismiss stage. It does not affect the evidentiary burden at summary judgment or trial. A complaint that satisfies the framework survives the motion to dismiss; the question whether the plaintiff can prove the alleged conduct, and whether the proven conduct violates § 1, is for later stages.

*The inference is rebuttable.* Defendants may respond at the motion-to-dismiss stage with specific factual showings. The rebuttal is a burden-of-production shift, not a burden-of-persuasion shift; defendants need not prove that no agreement existed, only that the trigger conjunction does not in fact obtain on the pleaded facts. Three rebuttal categories cover the principal cases.

(a) *Data inflow disqualification.* Defendants may show — through the licensing contract, the technical architecture, an audit report, or other materials properly considered at the motion-to-dismiss stage — that the data inflow alleged in trigger (B) does not in fact occur, that the data is fully aged or aggregated before reaching the runtime operation, or that the data is generic operational data rather than competitively sensitive data. *Mach v. Yardi* illustrates this category at the summary-judgment stage; a defendant could, in an appropriate case, advance the same position at the motion-to-dismiss stage with adequate documentary support.

(b) *Pro-competitive justification of the alignment-predisposing feature.* Defendants may show that the trigger-(C) feature alleged in the complaint is, on the pleadings, pro-competitive in its operation. For example, capacity-allocation features in network industries, or coordinated capacity disclosures in regulated infrastructure markets, may be alignment-predisposing in a technical sense but pro-competitive in their substantive effect. The rebuttal is fact-specific; a generic invocation of "yield-management efficiencies" is insufficient.

(c) *Market mis-pleading.* Defendants may show that the relevant market alleged in the complaint is not properly pleaded, or that the user firms named in the complaint do not in fact account for a competitively significant share of that market. This is the conventional market-definition challenge, imported from merger and joint-venture review.

The rebuttal mechanism is doctrinally important because it preserves *Twombly*'s defendant-protective architecture. Plausibility doctrine demands that defendants not be subjected to the discovery cost of cases that fail on the pleadings. The Cartel-Manager Plausibility Framework does not relax this protection; it specifies how the protection operates in a setting where the decisive facts are internal to the vendor. Defendants whose conduct does not in fact involve cartel-manager features can defeat the structured inference at the motion-to-dismiss stage through targeted factual rebuttal. Defendants whose conduct does involve cartel-manager features must answer the complaint and bear the discovery cost — but this is the cost the substantive antitrust law has always assigned to defendants whose conduct gives rise to plausible claims of horizontal coordination. The framework does not change the underlying allocation; it operationalizes it for the algorithmic-intermediation context.

### V.D. Substantive Agnosticism

The Cartel-Manager Plausibility Framework is *substantively agnostic*. It does not commit to *per se*, quick-look, or rule-of-reason review of the alleged conduct on the merits. A case in which the framework is triggered, the rebuttal fails, and the complaint survives the motion to dismiss may proceed under any of the three substantive standards — the question of which standard applies is governed by existing substantive antitrust doctrine and is properly resolved at summary judgment or at trial after the relevant facts have been developed.

This is a deliberate feature, not a defect. The framework's contribution is procedural: unlocking discovery on the conjunction of pleadable triggers. Layering substantive characterization on top of the procedural mechanism would conflate two different doctrinal questions (whether plaintiffs may proceed and what substantive standard governs their proof) and would expose the framework to the criticism that it is *per se* liability through a procedural back door. The substantive agnosticism is the framework's principal defense against that criticism.

Three implications follow. *First*, *Duffy v. Yardi*'s pleading-stage *per se* characterization is not the framework. *Duffy* may be defensible on its own terms as a pleading-stage characterization of the alleged conduct as horizontal price-fixing, but the cartel-manager framework does not require the *per se* characterization. Some algorithmic-intermediation cases will be properly evaluated under *per se* (where the conduct, fully developed, looks like horizontal price-fixing through computational means); others will be properly evaluated under quick-look (where the conduct exhibits structural features sufficient to raise serious anticompetitive concerns but where defendants offer plausible procompetitive justifications); others will be properly evaluated under the full rule of reason (where the conduct's competitive effects are genuinely contested). The framework is compatible with each.

*Second*, the framework does not displace *Leegin*'s rule-of-reason holding for vertical agreements. The framework operates on the *horizontal* aspects of the alleged conduct. A complaint that pleads only a vertical relationship (a single user firm and a vendor) does not trigger the framework, because trigger (A) is not satisfied. The vertical-restraints doctrine continues to govern its proper domain.

*Third*, the framework does not preclude defendants from arguing efficiency justifications under whatever substantive standard applies. The rebuttal mechanism in Section V.C operates on the *triggers*, not on the substantive merits; once the case is in discovery, defendants retain all the substantive defenses (efficiencies, ancillary restraints, output expansion) that the rule of reason or quick-look review allows. The framework is not anti-efficiency; it is pro-discovery on the threshold question whether efficiency analysis is even reached.

### V.E. Theoretical and Empirical Support: The Economic Literature on Algorithmic Collusion

The framework's structural claim is modest: the conjunction of triggers (A), (B), and (C) is more consistent with intermediated coordination than with independent common adoption. That claim is supported by the economic literature on algorithmic collusion, but it does not depend on the literature's strongest forms.

The central experimental reference is Calvano, Calzolari, Denicolò, and Pastorello's 2020 *American Economic Review* article on algorithmic pricing and collusion.[^calvano2] Their Q-learning agents converged on supracompetitive prices in repeated pricing environments without explicit instructions to collude. The doctrinal point is not that any particular pricing vendor replicates Calvano's model. It is that pricing systems with memory, repeated interaction, and observability can produce coordinated outcomes without the analog evidentiary footprint of meetings or direct communications. Brown and MacKay's empirical work on pricing algorithms and Harrington's theoretical work on algorithmic collusion reinforce the same point: rival-observation capacity, memory, monitoring, and commitment mechanisms matter.[^brown-mackay2] Recent surveys synthesize the same lesson for legal readers.[^ittoo-petit]

The framework translates that literature into pleadable legal features. Trigger (A), competitively significant common adoption, corresponds to the scale condition: the algorithmic system must matter in the market. Trigger (B), nonpublic forward-looking competitive data inflow, corresponds to the rival-observation condition. Trigger (C), alignment-predisposing design or use features, corresponds to the memory, monitoring, delegation, and undercut-suppression conditions that make coordinated outcomes plausible. The literature does not prove liability. It supplies the economic reason why the trigger conjunction should unlock discovery.

The Note therefore does not rest on a formal model. A model could show that, under cross-rival data aggregation, delegation, common knowledge, undercut suppression, and joint-profit orientation, an algorithmic intermediary can reproduce cartel-like comparative statics. But that proposition is essentially a sufficiency claim: if those conditions hold, the cartel-manager analogy is plausible. The important legal question is whether plaintiffs should be allowed discovery to test whether the conditions hold in a real system. The framework answers that procedural question.

### V.F. Application: Re-Litigating the Cases Under the Framework

The framework's value is best illustrated by applying it to the existing case law. This Section walks through *Gibson*, *Cornish-Adebiyi*, *Duffy v. Yardi*, *In re RealPage*, and *Mach v. Yardi* and shows what each disposition would look like under the Cartel-Manager Plausibility Framework.

#### V.F.1. *Gibson*

The plaintiffs in *Gibson* alleged that several Las Vegas Strip hotel operators had each licensed Cendyn's GuestRev/GroupRev software, that the software ingested each hotel's nonpublic occupancy and pricing data, and that the resulting recommended prices were higher than the unilateral pre-adoption prices. Under the Cartel-Manager Plausibility Framework:

- *Trigger A* (competitively significant common adoption): plausibly alleged. The Strip hotels collectively account for a substantial share of the relevant market (Las Vegas hotel rooms, properly defined). The plaintiffs' allegations of common adoption among multiple Strip operators satisfy the trigger as a matter of pleading.

- *Trigger B* (nonpublic, forward-looking, competitively sensitive data inflow): plausibly alleged on the pleadings. The plaintiffs alleged that each hotel's occupancy and pricing data was forward-looking and competitively sensitive, and that the data fed into Cendyn's runtime operation.

- *Trigger C* (alignment-predisposing feature): plausibly alleged. The plaintiffs alleged that Cendyn marketed high acceptance rates, that the algorithm provided recommendations users typically followed, and that the software was structured to suppress unilateral price decreases. At least one of categories (i)–(vii) is plausibly alleged.

Under the framework, the structured inference would arise, and the question would shift to rebuttal. Cendyn could move to dismiss with a specific factual showing that the data inflow was either aged or did not occur (rebuttal (a)), or that the relevant market was mis-pleaded (rebuttal (c)). On the *Gibson* record as it reached the Ninth Circuit, neither rebuttal would have succeeded at the motion-to-dismiss stage. The complaint should have survived. Discovery would then have addressed the actual data-flow architecture, the actual override rate, the actual objective function — and the case would have proceeded on the merits.

The framework would not have committed the Ninth Circuit to a finding of liability. It would have committed the court only to allowing discovery on the conjunction of facts the framework treats as sufficient for pleading-stage plausibility. The substantive question — whether, on the developed record, the conduct violated § 1 — would have remained for summary judgment and trial.

A clarifying point about what this re-litigation is doing. The framework is not a charitable re-reading of the *Gibson* complaint as actually filed; it is an articulated standard that future complaints in the Ninth Circuit and elsewhere can satisfy by pleading to the framework's specifications. On the actual *Gibson* pleadings, the Ninth Circuit may or may not have been right that the rim allegations were insufficient — that is a fact-specific question the framework does not foreclose. What the framework provides is a *predictable, articulable architecture* for plaintiffs to plead toward and defendants to rebut. The framework's value in *Gibson*-type cases is prospective: it tells future plaintiffs what specificity their complaints must achieve to survive a motion to dismiss, and it tells future defendants what the rebuttal mechanism allows them to demonstrate. The framework converts an ad hoc post-hoc inquiry (was the rim sufficient?) into a structured ex ante inquiry (do the conjunctive triggers satisfy the framework's specifications?), with corresponding gains in predictability for both sides.

#### V.F.2. *Cornish-Adebiyi*

The pending Third Circuit case, *Cornish-Adebiyi v. Caesars Entertainment*, presents substantially the same factual pattern as *Gibson* in the Atlantic City casino-hotel context. Under the framework, the analysis tracks the *Gibson* analysis in Section V.F.1: the triggers are plausibly alleged, defendants may attempt targeted rebuttal, and the case proceeds if the rebuttal fails. The Third Circuit's adoption of the framework — or of the constructive-rim path discussed in Section IV.F — would be the most consequential algorithmic-pricing development since *Gibson*.

#### V.F.3. *Duffy v. Yardi*

*Duffy v. Yardi*'s pleading-stage *per se* characterization is approximately the substantive characterization the framework would treat as plausibly available, but the framework would arrive at the disposition through articulated triggers rather than judicial discretion. Under the framework:

- *Trigger A*: plausibly alleged. The plaintiffs alleged common adoption of Yardi's RENTmaximizer software among multiple multifamily-property managers in defined urban markets.
- *Trigger B*: plausibly alleged. The plaintiffs alleged that Yardi's software ingested nonpublic, forward-looking pricing and occupancy data from rival users.
- *Trigger C*: plausibly alleged. The plaintiffs alleged Yardi-organized user-group meetings and other alignment-predisposing features.

The framework would be satisfied. The substantive characterization on the merits — whether the conduct, fully developed, is *per se* horizontal price-fixing or rule-of-reason coordination — would be deferred to summary judgment and trial. *Duffy*'s pleading-stage *per se* characterization is, under the framework, an over-commitment at the wrong procedural stage; the framework reaches the same procedural disposition (denial of the motion to dismiss) without the substantive over-commitment.

#### V.F.4. *In re RealPage*

The MDL's denial of the motion to dismiss under a rule-of-reason posture is fully consistent with the framework. The framework would have reached the same disposition through the trigger conjunction and would have provided doctrinal articulation that the MDL court did not have available in 2023. The framework's substantive agnosticism is consistent with the MDL's rule-of-reason posture, while leaving open the possibility that, on a developed record, the substantive standard might shift to quick-look or *per se*.

#### V.F.5. *Mach v. Yardi*

The summary-judgment grant in *Mach v. Yardi* turned on the factual finding that Yardi's software did not in fact use other clients' confidential pricing data.[^89] Under the framework, this finding defeats trigger (B) on the developed record. The framework would, in the appropriate case, allow defendants to raise the same factual showing at the motion-to-dismiss stage if adequately documented; absent adequate documentation, the showing would await discovery and summary judgment. *Mach* illustrates how the framework's rebuttal mechanism preserves the substantive distinction between intermediaries that perform cartel-manager functions and those that do not.

#### V.F.6. Cross-Case Synthesis

Three patterns emerge from the application of the framework to the five cases.

*First*, the framework predicts the procedural disposition the developed case law has — sometimes inconsistently — already half-articulated. *Duffy v. Yardi*'s pleading-stage survival, *In re RealPage*'s rule-of-reason posture, and *NJ AG v. RealPage*'s partial-MTD ruling are all consistent with the framework's prediction that complaints satisfying the conjunctive triggers will survive the motion to dismiss. *Gibson*'s and *Cornish-Adebiyi*'s dismissals are inconsistent with the framework, but the inconsistency tracks the deadlock-formalizing move the Note identifies in Section IV.C — the courts demanded factual specificity at the pleading stage that the trigger conjunction does not require. The framework is not making the case law up; it is describing the procedural pattern that emerges when the case law's disagreements are tested against the cartel-manager structural account.

*Second*, the framework's rebuttal mechanism is *load-bearing*, not ornamental. *Mach v. Yardi*'s factual finding (no use of other clients' confidential pricing data) is the kind of rebuttal showing the framework contemplates at the pleading stage where adequately documented, and at summary judgment where developed through discovery. The framework does not create an inference that survives all factual development; it creates a procedural mechanism that allows the factual development to occur. Defendants whose conduct does not fit the cartel-manager pattern have multiple opportunities to defeat the case — at MTD via documented rebuttal, at MSJ via developed-record disqualification, at trial via merits adjudication. The framework's threshold is the start, not the end, of defendants' procedural protections.

*Third*, the framework's substantive agnosticism allows different cases to develop along different substantive paths once the procedural threshold is crossed. *Duffy v. Yardi*'s *per se* characterization at the merits stage, if it ultimately holds, would be one path; *In re RealPage*'s rule-of-reason posture would be another; a quick-look posture in a future case could be a third. The framework does not commit any of these cases to a particular substantive outcome; it commits them only to the discovery-unlocking step that the analog doctrines, applied to algorithmic intermediation, have systematically denied. This is the framework's discipline — and its modesty.

### V.G. Why the Framework Is *Twombly*-Compatible

A natural objection is that the Cartel-Manager Plausibility Framework circumvents *Twombly* by relaxing the plausibility requirement for a category of cases. The objection has rhetorical force but underestimates the framework's structure.

*Twombly* requires plaintiffs to plead facts that plausibly *suggest* agreement — that is, facts whose joint presence is more consistent with concerted action than with independent parallel conduct.[^90] The framework's defense of *Twombly* compatibility runs through an explicit inference-of-agreement step that an attentive reader will demand.

*Why does the conjunction of triggers (A), (B), and (C) plausibly suggest agreement rather than independent action?* Each trigger, considered in isolation, is consistent with both anticompetitive coordination and pro-competitive independent adoption. Common adoption among rivals (trigger A) might reflect parallel decisions to license efficient yield-management technology. Nonpublic forward-looking competitive data inflow (trigger B) might reflect a vendor business model in which each user firm independently delegates data analysis to a specialist. At least one alignment-predisposing feature (trigger C) might be incidentally present in efficient pricing software whose primary purpose is unilateral optimization. None of the three triggers, on its own, excludes the independent-action inference.

The conjunction does. Under the independent-adoption hypothesis — each user firm independently adopting efficient yield-management software for unilateral profit maximization — one would expect (A) but neither (B) nor (C) at any meaningful incidence rate. Trigger (B) is hard to explain on the independent-adoption hypothesis: rivals would not voluntarily share nonpublic, forward-looking, competitively sensitive information with one another through a common vendor channel if their adoption decisions were truly independent and oriented toward unilateral optimization, because doing so dissipates the informational rents that make their pricing decisions competitive in the first place. Trigger (C) is hard to explain on the independent-adoption hypothesis: efficient yield management does not require autopilot defaults, override friction, vendor monitoring of compliance, vendor-organized user-group meetings sharing nonpublic data, market-wide dashboards visible to multiple users, anti-undercut design features, or vendor marketing of high acceptance rates. These are *coordination-implementing* features, not unilateral-optimization features. Under the intermediated-coordination hypothesis, by contrast, all three triggers are jointly expected and indeed structurally necessary: common adoption is the scope of coordination, data inflow is the mechanism of recommendation generation, and alignment-predisposing features are the operational implementations of delegation, monitoring, and enforcement.

The conjunction of (A), (B), and (C) is, in a strict Bayesian-inferential sense, more consistent with intermediated coordination than with independent adoption. This is the inferential bridge *Twombly* requires the framework to articulate. The empirical and economic literature on algorithmic collusion supports the inferential structure: experimental work by Calvano, Calzolari, Denicolò, and Pastorello demonstrates that Q-learning algorithms with rival-data inputs can converge on supracompetitive equilibria without explicit communication;[^calvano1] empirical work by Brown and MacKay documents that algorithmic-pricing adoption in retail markets is associated with coordinated price trajectories;[^brown-mackay1] theoretical work by Joseph Harrington identifies the structural conditions under which autonomous algorithmic agents can sustain collusive equilibria.[^harrington1] The framework's triggers are calibrated to the structural fingerprint this literature describes; the conjunction is the diagnostic pattern under which intermediated coordination is more plausible than independent adoption.

The framework's compatibility with *Twombly* therefore rests on three reinforcing features. *First*, the inference-of-agreement is articulated explicitly through the conjunction's structural-fingerprint logic, not asserted abstractly. *Second*, the triggers are conjunctive: a complaint failing any of the three does not invoke the framework's pleading shift. *Third*, the rebuttal mechanism preserves defendants' ability to defeat insufficient complaints at the motion-to-dismiss stage through targeted factual showings — including showings that the alignment-predisposing feature alleged is in fact an artifact of efficient yield management rather than coordination.

The framework can be understood, in *Twombly* terms, as articulating the "common sense" baseline that *Iqbal* invoked but did not specify.[^91] *Twombly* held that plausibility is contextual; *Iqbal* tied it to "judicial experience and common sense." The framework provides courts with a principled articulation of what common sense requires in the specific context of algorithmic intermediation, drawing on a coherent theoretical account (the Hovenkamp–Leslie cartel-manager framework) that is widely accepted in antitrust scholarship and supported by the published economic literature on algorithmic collusion. The framework is not a relaxation of plausibility; it is plausibility's elaboration for a context the analog cases did not foresee.

A doctrinal note on "presumption" terminology. Some readers will press whether the framework is really a Federal Rule of Evidence 301 burden-shifting mechanism. It is not.[^fre301] The framework operates at the pleading stage, not the evidentiary stage; the rebuttal mechanism is a burden-of-production shift in the *McDonnell Douglas*[^mcdonnell1] style, not a Rule 301 presumption. Nothing in the framework affects the evidentiary burdens at trial or summary judgment. "Plausibility framework" is the cleaner label because the point is to structure *Twombly* plausibility, not to alter evidentiary burdens.

### V.H. What the Framework Does Not Reach: Merits-Stage Architecture

The framework operates exclusively at the motion-to-dismiss stage. Three downstream procedural questions are bracketed for separate treatment in future scholarship and adjudication.

*Class certification.* Most algorithmic-pricing § 1 actions to date have been brought as putative class actions on behalf of consumers (hotel guests, multifamily-housing tenants) or on behalf of upstream commercial purchasers. The class certification analysis under Rule 23 — predominance of common questions, typicality of the class representative, adequacy of class counsel — proceeds independently of the framework's procedural threshold. Some of the trigger-related questions (whether the data inflow was uniformly forward-looking and competitively sensitive, whether the alignment-predisposing feature operated uniformly across user firms in the relevant market) may bear on Rule 23 analysis, but the framework does not specify the bearing. A plaintiff that survives MTD under the framework still bears the conventional Rule 23 burden at the certification stage; the framework does not relax that burden, and its successful invocation does not establish certifiability.

*Damages*. The framework does not address how supracompetitive overcharges are quantified, how class-wide damages are computed, or how individual-versus-class damages issues interact with the merits inquiry. Standard antitrust damages doctrine — *Hanover Shoe*[^hanover1] for direct purchasers, *Illinois Brick*[^illinois1] for indirect purchasers, *Comcast v. Behrend*[^comcast1] for class-wide damages methodology — continues to govern. Plaintiffs proceeding under the framework face the conventional damages-quantification burden once liability is established.

*Trial-stage substantive review.* The framework's substantive agnosticism (Section V.D) defers to existing doctrine the question whether the alleged conduct is evaluated under *per se*, quick-look, or rule-of-reason review. The trial-stage standard turns on case-specific developed facts, and the framework offers no guidance beyond what the analog doctrines already provide. The Court's recent decisions in *Ohio v. American Express Co.*[^amex1] and *NCAA v. Alston*[^alston1] govern rule-of-reason analysis in technology-mediated and platform contexts; their interaction with algorithmic-intermediation cases is a question the framework leaves for the merits stage and for the cases as they develop.

The framework's deliberate scope — pleading-stage threshold, nothing more — is designed to be modular. A court adopting the framework commits to nothing about how downstream merits-stage adjudication unfolds; the framework's operation is consistent with multiple downstream architectures. This modularity is a virtue from a doctrinal-restraint standpoint and is one of the framework's principal defenses against the criticism that it imports administrative judgment into the merits.

### V.I. Implementation Rate as Plus Factor, Not Element

Implementation rate — the share of recommendations actually accepted by user firms — is highly probative of delegation. But it should not be an element of the prima facie pleading case. The actual rate is internal to the vendor and user firms; requiring plaintiffs to plead it would recreate the deadlock the framework is designed to solve.

The better treatment is to make implementation rate a plus factor within trigger (C). Plaintiffs may rely on vendor marketing claims, customer testimonials, regulatory disclosures, or whistleblower reports suggesting high acceptance. Defendants may rebut with documents showing that recommendations are rarely accepted, that users retain practical discretion, or that the claimed acceptance rate is not tied to the challenged product or market. Discovery then develops the actual rate for merits-stage analysis. This approach credits public-facing vendor representations only for the limited pleading proposition they support: that delegation is plausible enough to investigate.

---

## VI. The Federalism Layer

The state legislative response to algorithmic pricing underscores why a federal pleading framework is needed. In the absence of a stable Sherman Act answer, states and cities have begun to choose among categorical bans, disclosure rules, and targeted antitrust amendments.

### VI.A. Taxonomy of State Responses

The first category is the categorical ban. New York's S.7882, San Francisco's § 37.10C, Philadelphia's amended landlord-tenant ordinance, and similar local measures prohibit specified algorithmic rent-setting practices in residential housing.[^92] These laws solve the discovery-access problem by bypassing antitrust adjudication. That may be defensible in housing markets, but it is necessarily overinclusive from the perspective of federal antitrust: it captures some uses of pricing software that do not involve cartel-manager features.

The second category is disclosure. New York's Algorithmic Pricing Disclosure Act requires businesses using algorithmic personalized pricing to disclose that fact to consumers.[^96] Disclosure rules address opacity, but not the § 1 question whether rivals have coordinated through a common intermediary.

The third category is targeted antitrust amendment. California's AB 325 is the closest analog to the framework offered here. It adds a Cartwright Act prohibition on use or distribution of a common pricing algorithm in a restraint of trade and separately provides that a Cartwright Act complaint need only plead facts making agreement plausible; it need not plead facts tending to exclude independent action.[^97] That choice is revealing. California responded to algorithmic pricing not only by changing substantive state law, but by changing pleading doctrine.

The federal framework is a judicial version of that same procedural instinct, with a narrower trigger set appropriate for federal treble-damages litigation. It does not preempt state experimentation. State antitrust statutes remain valid, and states may regulate algorithmic pricing for housing, consumer-protection, or distributional reasons beyond the Sherman Act. The point is institutional rather than preemptive: when federal courts provide a workable path to discovery in cartel-manager cases, state legislatures have less reason to reach for categorical bans as an antitrust substitute.

---

## VII. Anticipated Objections and Replies

This Section steelmans and answers the strongest objections to the framework. The objections are presented in approximate descending order of doctrinal seriousness.

### VII.A. The ICLE Efficiency Defense

The International Center for Law and Economics has advanced the most coherent defense of the *Gibson* posture and of defendant-protective pleading rules for algorithmic-pricing intermediation more generally.[^101] The defense has four interlocking claims.

*First*, dynamic pricing has well-documented welfare efficiencies — better matching of supply to demand, reduced shortage and surplus, more efficient capacity utilization in capacity-constrained industries.[^102] These efficiencies are realized regardless of whether the dynamic-pricing system is in-house or vendor-mediated. The framework, by treating common adoption of vendor-mediated dynamic pricing as one necessary trigger, threatens to chill efficient innovation.

*Second*, common software adoption alone does not constitute conspiracy; firms commonly adopt the same general-ledger software, the same payroll software, the same email systems, and no one suggests that this raises § 1 concerns. The line that distinguishes cartel-managing software from ordinary general-purpose business software requires more articulation than the framework provides.

*Third*, *Twombly* requires that a complaint exclude not only the bare possibility of independent action but the substantial probability of innocent explanation. The framework's triggers do not exclude innocent explanation: each trigger is consistent with both anticompetitive and pro-competitive behavior. The framework therefore lowers the *Twombly* threshold contrary to Supreme Court authority.

*Fourth*, the framework's chilling effect on innovation is structurally undertheorized. Vendors operating at the frontier of dynamic-pricing technology will rationally avoid the U.S. market or restructure their products to avoid trigger satisfaction, with welfare losses to user firms and (downstream) to consumers.

The replies, in order.

*Reply to (1).* The framework does not target dynamic pricing; it targets the conjunction of common adoption among horizontal rivals, nonpublic forward-looking data inflow, and alignment-predisposing features. A vendor-mediated dynamic-pricing system used by a single firm does not trigger the framework. A vendor-mediated dynamic-pricing system used by multiple firms in a market without rival data inflow (e.g., the *Mach v. Yardi* fact pattern) does not trigger the framework. A vendor-mediated dynamic-pricing system used by multiple firms with rival data inflow but without alignment-predisposing features does not trigger the framework. The framework reaches a narrow class of cases in which the conjunctive pattern matches the cartel-manager account, and it does not chill innovation in dynamic pricing generally.

*Reply to (2).* The line between cartel-managing software and general-purpose business software is precisely what the conjunction of triggers (B) and (C) draws. General-ledger software, payroll software, and email systems do not aggregate competitively sensitive forward-looking data from rival firms and do not have alignment-predisposing features in the price-setting function. Pricing intermediaries that aggregate such data and have such features fit the cartel-manager pattern; pricing intermediaries that do not, do not. The line is articulated, not vague.

*Reply to (3).* The framework does not lower the *Twombly* threshold; it operationalizes it. *Twombly* requires plausibility, not exclusion of innocent explanation; *Matsushita*'s economic-implausibility analysis is a summary-judgment doctrine, not a pleading doctrine.[^103] The conjunction of triggers (A), (B), and (C) renders horizontal coordination plausible, in the *Twombly* sense, against the backdrop of the cartel-manager account. The defendants' rebuttal mechanism preserves their ability to defeat the pleading inference with specific factual showings — which is the *Twombly* protection in operationalized form.

*Reply to (4).* The chilling-effect concern is empirical. The framework's triggers are calibrated to fit the cartel-manager pattern, not to capture all dynamic-pricing technology. Vendors whose products do not perform cartel-manager functions will not be subject to trigger satisfaction. Vendors whose products *do* perform cartel-manager functions face exactly the antitrust scrutiny the substantive law has always assigned to coordination-facilitating conduct. The current case pattern suggests that the framework reaches a relatively narrow class of vendors operating at high market-share concentration in specific industries, not the broader dynamic-pricing technology ecosystem. That empirical claim should be re-tested as more cases develop.

The same answer applies to broader defense-side caution about over-deterring efficient technology adoption. The framework does not substitute administrative judgment for market judgment, does not impose *per se* liability, and does not foreclose efficiency defenses. It asks only whether plaintiffs have pleaded enough, given the cartel-manager pattern, to test the system's actual architecture in discovery. That is a restrained procedural move, not a substantive expansion of § 1.

### VII.B. Hovenkamp's Algorithm-as-Person Concern

Hovenkamp's antitrust-personhood work supplies a useful doctrinal caution: the statutory definition of antitrust "person" likely excludes AI algorithms, even though firms and individuals who use algorithms to achieve illegal ends remain subject to liability.[^104] The concern for algorithmic-pricing doctrine is that courts or commentators might respond to new technology by treating the algorithm itself as the agreeing actor, substituting a computational fiction for the firm-firm agreement § 1 has historically targeted.

The framework offered here is designed to be compatible with Hovenkamp's concern. The framework does not treat the algorithm as a person, does not require an agreement "with" the algorithm, and does not displace the firm-firm agreement requirement. It treats the algorithm as a coordination *mechanism*, in the same sense that Hovenkamp and Leslie's 2011 article treated cartel-managing firms as coordination mechanisms. The agreement, in framework terms, runs between the user firms — they have, through their conjunctive trigger-satisfying conduct, effectively agreed to delegate pricing authority to a common intermediary. The intermediary is the means by which the agreement is implemented; it is not itself a party to the agreement.

The agreement-by-conduct framing is conventional § 1 doctrine. *Interstate Circuit* inferred horizontal agreement from parallel responses to a common signal without any direct firm-firm communication.[^105] *Apple e-Books* inferred horizontal agreement from individually-negotiated agency contracts that, in conjunction, instantiated a coordinated pricing strategy.[^106] The Hovenkamp–Leslie cartel-manager account is the theoretical generalization of this pattern: agreement need not be communicated directly between competing firms; it can be achieved through their conjunctive entrustment of the coordination function to a third party. The framework operationalizes the generalization in the algorithmic-intermediation context, while preserving the firm-firm agreement requirement.

A subsidiary concern Hovenkamp raises is the asymmetry between vendor-as-cartel-manager framings (in which the vendor is unambiguously a Sherman Act "person") and pure-algorithm framings (in which the agreement is alleged to be between user firms via algorithmic interaction without an identifiable third-party coordinator).[^107] The framework engages only the former. A pricing system in which competing firms run algorithms that interact through public market data, without a common third-party intermediary, raises distinct issues that the framework does not address. This is a deliberate scope limitation; the framework is for the cartel-manager case, not for pure tacit-collusion-with-algorithms.

### VII.C. Strike-Suit Risk and Discovery Cost

A familiar objection to any pleading-friendly innovation is that it invites strike suits — boilerplate complaints that meet minimal trigger requirements and force defendants into expensive discovery to extract settlement value. The objection is serious and should be answered seriously.

The framework's design responds to the concern in three ways. *First*, the conjunctive trigger structure raises the pleading bar above what a boilerplate complaint can meet. A complaint must plead a properly defined relevant market, competitively significant rival adoption, nonpublic forward-looking data inflow, and at least one alignment-predisposing feature. Each is non-trivial; the conjunction is meaningful. *Second*, the rebuttal mechanism allows defendants to defeat insufficient complaints at the motion-to-dismiss stage with targeted factual showings, without bearing full discovery cost. *Third*, the substantive agnosticism preserves the existing substantive defenses — efficiencies, ancillary restraints, output expansion — at the merits stage.

The empirical question of how the framework would affect strike-suit incidence in practice is open. The qualitative case pattern in Section III provides a baseline against which later filings can be measured; longitudinal study after the framework's adoption (or after a Third Circuit version of it in *Cornish-Adebiyi*) would clarify the question. The Note's claim is normative, not predictive: the framework is designed to balance the discovery-cost concern against the under-enforcement concern in a way *Twombly* doctrine, applied unmodified to algorithmic intermediation, does not.

### VII.D. The *Trinko* Refusal-to-Deal Ghost

A more subtle objection invokes *Verizon Communications Inc. v. Law Offices of Curtis V. Trinko, LLP*[^108] for the proposition that antitrust doctrine should be cautious about expanding § 1 in ways that effectively impose duties to deal — including, on this view, duties that would constrain firms' choices about which third-party vendors to engage. The objection's force depends on the framing: if the framework is read as discouraging firms from engaging vendor-mediated dynamic pricing, it operates structurally as a soft duty-not-to-deal that *Trinko* and its progeny suggest courts should approach cautiously.

The reply is that *Trinko* is a § 2 case about monopolization and refusal-to-deal doctrine in the Section 2 context.[^109] The framework operates under § 1 and concerns concerted action among competitors, not unilateral refusal-to-deal by a dominant firm. The doctrines have separate domains. Moreover, the framework does not impose a duty (to deal or not to deal); it affects only the procedural threshold for surviving a motion to dismiss in cases alleging concerted-action violations. Firms remain free to engage any vendor they choose; what the framework affects is the litigation posture if the vendor's services produce the cartel-manager pattern. This is a different concern from the *Trinko* concern.

### VII.E. The "Price Exchange" Alternative

The amicus brief filed in *Cornish-Adebiyi* by a group of antitrust law and economics professors proposes an alternative framing under which algorithmic-pricing intermediation is analyzed as an information-exchange violation under § 1, with the relevant question being whether the exchange of competitively sensitive information among rivals (mediated through the vendor) is presumptively illegal under existing information-exchange doctrine.[^110]

The price-exchange framing has substantial overlap with the framework offered here: both target the data-inflow feature; both treat vendor-mediated coordination as the primary harm; both operate within § 1. The principal difference is that the price-exchange framing is *substantive* (treating the conduct as presumptively illegal information exchange), while the framework offered here is *procedural* (treating the conduct as plausibly alleged § 1 agreement, with substantive characterization deferred). The choice between the two framings is a strategic one, and they are not mutually exclusive — a court could adopt the framework offered here for procedural purposes and rely on information-exchange doctrine for substantive characterization at the merits stage.

The Note's preference for the procedural framing reflects three considerations. *First*, the procedural framing avoids the substantive over-commitment that the price-exchange framing risks: a presumptive-illegality posture at the pleading stage is doctrinally aggressive and may be vulnerable to circuit-court reversal in cases with non-trivial efficiency justifications. *Second*, the procedural framing better preserves the *Twombly* architecture: it does not relax plausibility but operationalizes it, and the rebuttal mechanism preserves defendant protections. *Third*, the procedural framing is institutionally more flexible: it accommodates the variation in algorithmic-intermediation contexts (multifamily housing, hotel pricing, ride-sharing, retail) without committing the law to a single substantive characterization across all contexts.

The two framings are, however, *not in conflict, and the doctrinally strongest configuration is their combination.* The Cartel-Manager Plausibility Framework operates at the pleading stage to articulate what plaintiffs must allege to survive a motion to dismiss; information-exchange doctrine — anchored in *United States v. United States Gypsum Co.*, *Maple Flooring Manufacturers Ass'n v. United States*,[^maple-flooring] and the FTC/DOJ Antitrust Guidelines for Collaborations Among Competitors[^collab-guidelines] — operates at the merits stage to characterize the substantive antitrust violation the developed conduct constitutes. The combination is doctrinally coherent: the framework's conjunctive triggers (especially trigger (B)) operationalize what plausibly alleges *information exchange* among rivals through a common intermediary, and the substantive characterization at the merits stage applies the established information-exchange doctrine to evaluate whether the proven exchange amounts to an unreasonable restraint of trade.

The Department of Justice's enforcement playbook in the *RealPage* settlement effectively combines the two: the consent decree's prohibition on forward-looking nonpublic data inflows tracks the framework's trigger (B), and the underlying theory of harm articulated in DOJ's filings rests on information-exchange concerns drawn from *U.S. Gypsum* and the broader trade-association line.[^doj-info1] A court adopting the framework procedurally and information-exchange doctrine substantively would have, at the merits stage, the doctrinal architecture for evaluating whether the conduct the discovery has revealed amounts to a § 1 violation — without committing to *per se* characterization at the pleading stage and without relaxing the substantive doctrine that governs information exchange among rivals.

Both framings can advance, and the doctrinally strongest litigation strategy in *Cornish-Adebiyi* and successor cases combines them. This Note's primary contribution is the procedural framing; the price-exchange framing is a friendly substantive complement, and the combination is the architecture under which both can do their proper work.

### VII.F. The Hovenkamp & Leslie "Doctrine" Misreading

A final objection — sometimes raised in private conversation rather than in writing — is that the framework misappropriates Hovenkamp and Leslie's 2011 article by treating it as doctrinal authority for a new procedural mechanism, when in fact the article was a normative-theoretical piece that did not propose any such doctrine.

The Note acknowledges the concern and responds in two ways. *First*, the Note is explicit, in this Section and throughout, that Hovenkamp and Leslie identified an *account*, not a doctrine, and that what the Note does is *operationalize* the account. The framework's authority does not rest on the article's status as binding precedent (it has none), but on the article's analytical persuasiveness as a description of how the cartel-manager function operates and on the fit between that function and the algorithmic-intermediation pattern. The framework is the Note's contribution, building on Hovenkamp and Leslie's account.

*Second*, the Note's use of the cartel-manager account is consistent with Hovenkamp's own subsequent scholarship in 2025, which engaged the algorithmic-pricing question without (in Hovenkamp's case) proposing a procedural innovation of the kind offered here.[^111] The Note's procedural innovation is its own contribution; the underlying theoretical account is Hovenkamp and Leslie's. The relationship between the two is one of respectful extension, not appropriation.

---

## VIII. Conclusion: The Next Appellate Test

*Cornish-Adebiyi v. Caesars Entertainment* is the next appellate opportunity to test whether *Gibson* becomes the dominant pleading template for algorithmic-pricing cases or remains a narrower Ninth Circuit disposition tied to the complaint and appellate posture before that court. The Third Circuit need not adopt this Note's framework wholesale to improve the doctrine. It need only recognize the core procedural problem: when the alleged coordinating mechanism is a proprietary pricing intermediary, the facts most probative of agreement are often the facts least available before discovery.

One disposition would be express adoption of the Cartel-Manager Plausibility Framework, or a structurally similar trigger-and-rebuttal rule. Under that approach, the court would reverse the dismissal, identify the features that make common algorithmic intermediation plausibly concerted rather than merely parallel, and remand for ordinary litigation on a developed record. That holding would produce a direct tension with *Gibson*, but the important point is narrower: it would make clear that *Twombly* does not require plaintiffs to plead the internal architecture of a proprietary pricing system before they may discover it.

A less ambitious but still consequential disposition would be a constructive-rim reading along the lines discussed in Section IV.F. The court would reverse on the ground that the district court demanded too much specificity in the rim allegation and would articulate that hub-and-spoke doctrine, properly understood, can reach algorithmic-intermediation cases through inference of inter-spoke awareness from vendor user-group meetings, vendor-marketed acceptance rates, and similar features. The disposition would not adopt the Cartel-Manager Plausibility Framework explicitly but would create the doctrinal space for it to develop. It would also narrow *Gibson*'s influence by showing that the absence of direct inter-spoke communication need not be dispositive. In this posture, the framework's role is to provide district courts with articulated guidance for applying the constructive-rim reading consistently — the framework's three triggers operationalize what the constructive-rim reading requires, and district courts can adopt the framework's architecture as the analytical tool that gives the Third Circuit's holding doctrinal traction.

The third possibility is affirmance along *Gibson* lines. That disposition would not end the debate, but it would sharpen it. If two circuits treat algorithmic-pricing complaints as implausible unless plaintiffs plead the very data flows and objective functions that are internal to the vendor, the problem becomes one of institutional design rather than case-specific pleading. The response may then come from other circuits, from Congress, or from state and local legislation. That is precisely the fragmentation a federal pleading framework can avoid.

Whichever disposition the Third Circuit reaches, the framework offered here is the doctrinal architecture under which the question is most coherently asked. *Gibson*'s deadlock is real, the analog doctrines do not close it, and the cartel-manager account — operationalized through three conjunctive triggers, anchoring guidance for the competitively-significant inquiry, a non-exclusive plus-factor list, a rebuttal mechanism, and substantive agnosticism — is the most defensible procedural correction. The framework preserves *Twombly*'s defendant-protective architecture, distinguishes operationalization from substantive innovation, and does not depend on the formal model's strongest assumptions. It is calibrated to do specifically what it claims: unlock discovery on the conjunction of pleadable triggers in cases that fit the cartel-manager pattern, while leaving cases that do not fit the pattern subject to the analog doctrines that already adequately address them.

The substantive antitrust law has not asked, and need not now answer, whether algorithmic intermediation is anticompetitive. That question is for the merits, on a developed record, after discovery. The prior question is procedural: what must plaintiffs allege to be allowed to develop their case? The framework offered here answers that question without creating a new rule of liability. The right question is not whether the algorithm is a cartel manager. It is what plaintiffs must allege to be allowed to find out.

---

## Footnotes

[^pre1]: See *Gibson v. Cendyn Group, LLC*, 148 F.4th 1069, 1076–77 (9th Cir. 2025) (summarizing complaint allegations concerning GuestRev, GroupRev, RevCaster, autopilot functionality, override permissions, nonpublic data inputs, and alleged 90% recommendation acceptance).

[^pre2]: *Gibson*, 148 F.4th at 1074–77.

[^pre3]: See *infra* Sections III.C–D, III.G, V.E.

[^1]: *Gibson*, 148 F.4th at 1074–80, 1087–88.

[^2]: *Gibson v. Cendyn Group, LLC*, No. 25-1109 (U.S. Apr. 20, 2026) (cert. denied).

[^3]: *In re RealPage, Inc., Rental Software Antitrust Litig.* (No. II), MDL No. 3071, 709 F. Supp. 3d 478 (M.D. Tenn. 2023); *Duffy v. Yardi Sys., Inc.*, 758 F. Supp. 3d 1283 (W.D. Wash. 2024); *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 1:23-cv-02536-KMW-EAP, 2024 WL 4356188 (D.N.J. Sept. 30, 2024), appeal docketed, No. 24-3006 (3d Cir. Oct. 29, 2024); *Mach v. Yardi Sys., Inc.*, No. 24CV063117 (Cal. Super. Ct., Alameda Cnty. Oct. 6, 2025).

[^4]: *United States v. RealPage, Inc.*, Final Judgment as to Greystar Management Services, LLC, No. 1:24-cv-00710-WO-JLW, Doc. 172 (M.D.N.C. Mar. 2, 2026); *United States v. RealPage, Inc.*, Proposed Final Judgment as to RealPage, Inc., No. 1:24-cv-00710-WO-JLW, Doc. 159-1 (M.D.N.C. Nov. 24, 2025); *United States v. RealPage, Inc.*, Proposed Final Judgment as to LivCor, LLC, No. 1:24-cv-00710-WO-JLW, Doc. 164-1 (M.D.N.C. Dec. 23, 2025).

[^5]: See, e.g., N.Y. Gen. Bus. Law § 340-b (added by 2025 N.Y. S.7882); Cal. Bus. & Prof. Code §§ 16729, 16756.1 (added by 2025 Cal. AB 325); S.F. Admin. Code § 37.10C; Phila. Code §§ 9-802, 9-813.

[^7]: *Bell Atlantic Corp. v. Twombly*, 550 U.S. 544, 556–57 (2007); *Ashcroft v. Iqbal*, 556 U.S. 662, 678–79 (2009).

[^8]: This descriptive claim is developed in Section IV.

[^9]: *Interstate Circuit, Inc. v. United States*, 306 U.S. 208 (1939); *Toys "R" Us, Inc. v. FTC*, 221 F.3d 928 (7th Cir. 2000); *United States v. Apple, Inc.*, 791 F.3d 290 (2d Cir. 2015).

[^10]: *Theatre Enterprises, Inc. v. Paramount Film Distrib. Corp.*, 346 U.S. 537 (1954).

[^11]: *Matsushita Elec. Indus. Co. v. Zenith Radio Corp.*, 475 U.S. 574 (1986).

[^12]: *Leegin Creative Leather Prods., Inc. v. PSKS, Inc.*, 551 U.S. 877 (2007).

[^13]: Cal. Bus. & Prof. Code §§ 16729, 16756.1; N.Y. Gen. Bus. Law § 340-b.

[^14]: Herbert Hovenkamp & Christopher R. Leslie, *The Firm as Cartel Manager*, 64 Vand. L. Rev. 813 (2011).

[^15]: *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 24-3006 (3d Cir. docketed Oct. 29, 2024) (pending as of May 10, 2026).

[^17]: *Twombly*, 550 U.S. at 556–57; *Iqbal*, 556 U.S. at 678–79.

[^18]: *Twombly*, 550 U.S. at 554.

[^19]: *Id.* at 556.

[^20]: *Iqbal*, 556 U.S. at 679.

[^21]: *Twombly*, 550 U.S. at 559.

[^22]: *Id.* at 555–56.

[^23]: *Iqbal*, 556 U.S. at 679.

[^24]: 346 U.S. 537 (1954).

[^25]: *Id.* at 540–41.

[^26]: The "plus factor" terminology is post-*Theatre Enterprises*, but the doctrinal substance traces to that case. See generally Phillip E. Areeda & Herbert Hovenkamp, *Antitrust Law* ¶¶ 1410–17 (4th ed. 2017 & Supp.).

[^27]: See, e.g., *In re Flat Glass Antitrust Litig.*, 385 F.3d 350, 360 (3d Cir. 2004); *In re Plywood Antitrust Litig.*, 655 F.2d 627, 633–34 (5th Cir. 1981) (collecting plus-factor formulations).

[^28]: *Gibson*, 148 F.4th at 1082–83.

[^29]: 306 U.S. 208 (1939).

[^30]: 221 F.3d 928 (7th Cir. 2000).

[^31]: 791 F.3d 290 (2d Cir. 2015).

[^32]: *Id.* at 314–15.

[^33]: *Toys "R" Us*, 221 F.3d at 935–36.

[^34]: *Interstate Circuit*, 306 U.S. at 226–27.

[^35]: *Gibson*, 148 F.4th at 1076–77, 1084–88.

[^36]: 64 Vand. L. Rev. 813 (2011).

[^37]: *Id.* at 831–37, 837–48.

[^38]: 551 U.S. 877 (2007).

[^39]: *In re RealPage*, 709 F. Supp. 3d at 519–20.

[^40]: 418 U.S. 602 (1974).

[^41]: 988 F.3d 690 (4th Cir. 2021).

[^42]: *Gibson*, 148 F.4th at 1074–77.

[^43]: *Id.* at 1078, 1087–88; *Gibson v. Cendyn Group, LLC*, No. 2:23-cv-00140-MMD-DJA, 2024 WL 2060260, at *8 (D. Nev. May 8, 2024).

[^44]: *Gibson v. Cendyn Group, LLC*, No. 25-1109 (U.S. Apr. 20, 2026) (cert. denied).

[^45]: *Gibson*, 148 F.4th at 1087–88.

[^46]: *Id.* at 1084 & n.8.

[^47]: *Id.* at 1084–87.

[^48]: *Interstate Circuit*, 306 U.S. at 226–27.

[^50]: *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 1:23-cv-02536-KMW-EAP, 2024 WL 4356188 (D.N.J. Sept. 30, 2024), appeal docketed, No. 24-3006 (3d Cir. Oct. 29, 2024).

[^51]: *Id.* at *4–7.

[^52]: Statement of Interest of the United States at 1–3, *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 1:23-cv-02536-KMW-EAP (D.N.J. Mar. 28, 2024), ECF No. 96.

[^53]: Brief for the American Antitrust Institute as *Amicus Curiae* in Support of Plaintiffs-Appellants and Reversal, *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 24-3006 (3d Cir. Jan. 28, 2025); Brief for the Open Markets Institute as *Amicus Curiae* in Support of Plaintiffs-Appellants and Reversal, *id.* (3d Cir. Jan. 29, 2025).

[^54]: Brief for the International Center for Law and Economics as *Amicus Curiae* in Support of Defendants-Appellees and Affirmance, *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 24-3006 (3d Cir. Mar. 31, 2025).

[^55]: Brief of Antitrust Law and Economics Professors as *Amici Curiae* in Support of Plaintiffs-Appellants and Reversal, *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 24-3006 (3d Cir. Feb. 11, 2025).

[^56]: *In re RealPage, Inc., Rental Software Antitrust Litig.* (No. II), MDL No. 3071, 709 F. Supp. 3d 478 (M.D. Tenn. 2023).

[^57]: *Id.* at 510–12, 518–20.

[^58]: *Duffy v. Yardi Sys., Inc.*, 758 F. Supp. 3d 1283 (W.D. Wash. 2024).

[^59]: *Id.* at 1294–1301.

[^60]: *Id.* at 1295–1301.

[^61]: *Id.* at 1299–1301 (clarifying that *per se* posture at MTD does not adjudicate liability, only the substantive standard governing the alleged conduct if proven).

[^62]: Order Granting Defendants' Motion for Summary Judgment at 1, *Mach v. Yardi Sys., Inc.*, No. 24CV063117 (Cal. Super. Ct., Alameda Cnty. Oct. 6, 2025).

[^63]: *Id.* at 2–3, 11–12.

[^64]: Complaint, *Platkin v. RealPage, Inc.*, No. 2:25-cv-03057 (D.N.J. Apr. 23, 2025), ECF No. 1.

[^65]: See, e.g., AvalonBay Communities, Inc., Quarterly Report (Form 10-Q) 21 (May 7, 2026) (describing the March 31, 2026 ruling in the New Jersey RealPage litigation as to AvalonBay).

[^66]: *United States v. RealPage, Inc.*, Final Judgment as to Greystar Management Services, LLC, No. 1:24-cv-00710-WO-JLW, Doc. 172 (M.D.N.C. Mar. 2, 2026); see also Proposed Final Judgment as to Greystar Management Services, LLC, Doc. 152-1 (M.D.N.C. Aug. 8, 2025).

[^67]: *Id.* §§ IV.A, V.A–B, VIII.

[^68]: See Press Release, California Attorney General Rob Bonta, *Attorney General Bonta Announces $7 Million Settlement with Greystar for Participating in an Algorithmic Rent Alignment Scheme* (Nov. 18, 2025) (announcing multistate settlement by coalition of nine attorneys general).

[^69]: *United States v. RealPage, Inc.*, Proposed Final Judgment as to RealPage, Inc., No. 1:24-cv-00710-WO-JLW, Doc. 159-1 (M.D.N.C. Nov. 24, 2025).

[^70]: *Id.* §§ IV.A.1, IV.A.3.

[^71]: *Id.* § V.A–D.

[^72]: *Id.* § VI.B.

[^73]: *Id.* §§ VII.J–K, X.A.

[^75]: See United States et al. v. RealPage, Inc. et al.; Response of the United States to Public Comments, 91 Fed. Reg. 25,373 (May 8, 2026) (stating that the United States would move the court to enter the proposed final judgment); Antitrust Div., U.S. Dep't of Justice, *U.S. and Plaintiff States v. RealPage, Inc.*, https://www.justice.gov/atr/case/us-and-plaintiff-states-v-realpage-inc (last visited May 10, 2026).

[^76]: *United States v. RealPage, Inc.*, Proposed Final Judgment as to LivCor, LLC, No. 1:24-cv-00710-WO-JLW, Doc. 164-1 (M.D.N.C. Dec. 23, 2025).

[^77]: *Id.* §§ IV–VI, IX.

[^78]: A later empirical extension could code the binary outcome (MTD survival vs. dismissal) against the three trigger indicators and the plus-factor indicators, controlling for circuit, year, and case type. The present argument does not rely on that extension.

[^twombly1]: *Twombly*, 550 U.S. at 553–54 (treating the plaintiffs' evidentiary position as not exceptional and applying the conventional plausibility requirement).

[^conley1]: *Conley v. Gibson*, 355 U.S. 41, 45–46 (1957) (the "no set of facts" formulation), abrogated in relevant part by *Twombly*, 550 U.S. 544.

[^theatre2]: See, e.g., *In re Flat Glass Antitrust Litig.*, 385 F.3d 350, 360 (3d Cir. 2004); *In re High Fructose Corn Syrup Antitrust Litig.*, 295 F.3d 651, 661 (7th Cir. 2002) (refining plus-factor analysis through case-by-case adjudication).

[^79]: *Twombly*, 550 U.S. at 556–57.

[^80]: *Id.* at 553–54.

[^81]: Cal. Bus. & Prof. Code § 16756.1 (added by Stats. 2025, ch. 338 (AB 325), eff. Jan. 1, 2026).

[^81a]: U.S. Dep't of Justice & Fed. Trade Comm'n, Merger Guidelines (2023) § 2.1 (HHI thresholds). The HHI translation here is analogical, not direct: the Merger Guidelines govern transactions, not coordination through common intermediaries, and the framework's use of HHI is as a calibration anchor for competitive significance, not as an evidentiary requirement. A complaint need not plead HHI calculations to satisfy trigger (A), but a complaint pleading adoption among rivals whose combined share would produce HHI contributions in the Merger Guidelines' concerning ranges has unambiguously pleaded competitive significance.

[^81b]: See generally Fed. Trade Comm'n & U.S. Dep't of Justice, Antitrust Guidelines for Collaborations Among Competitors (2000); see also *Texaco Inc. v. Dagher*, 547 U.S. 1 (2006) (discussing antitrust treatment of joint ventures).

[^81c]: *United States v. U.S. Gypsum Co.*, 438 U.S. 422 (1978).

[^82]: 346 U.S. 537 (1954).

[^83]: *Toys "R" Us*, 221 F.3d at 935–36; *Apple e-Books*, 791 F.3d at 314–15.

[^84]: Hovenkamp & Leslie, *supra* note 14, at 813–19, 837–51.

[^84a]: *Id.* at 837–48, 849–56, 859–72.

[^84b]: *Id.* at 831–37, 837–48, 849–56. The four-function articulation in the text operationalizes the article's organizational account; it is not a quotation or claim that Hovenkamp and Leslie used this exact list.

[^84c]: *Id.* at 849–56, 859–72.

[^84d]: See *Mach*, order granting summary judgment, *supra* note 62, at 2–3, 11–12.

[^85]: Proposed Final Judgment as to RealPage, *supra* note 69, §§ IV.A–B, IV.D–E.

[^86]: *Id.* § IV.A.3.

[^87]: See *United States v. U.S. Gypsum Co.*, 438 U.S. 422, 441 n.16 (1978); *Maple Flooring Mfrs. Ass'n v. United States*, 268 U.S. 563 (1925); see generally Areeda & Hovenkamp, *supra* note 26, ¶¶ 1435–37.

[^88]: *Mach*, order granting summary judgment, *supra* note 62, at 2–3, 11–12.

[^89]: *Id.*

[^hanover1]: *Hanover Shoe, Inc. v. United Shoe Mach. Corp.*, 392 U.S. 481 (1968).

[^illinois1]: *Illinois Brick Co. v. Illinois*, 431 U.S. 720 (1977).

[^comcast1]: *Comcast Corp. v. Behrend*, 569 U.S. 27 (2013).

[^amex1]: *Ohio v. Am. Express Co.*, 585 U.S. 529 (2018).

[^alston1]: *NCAA v. Alston*, 594 U.S. 69 (2021).

[^90]: *Twombly*, 550 U.S. at 556–57.

[^91]: *Iqbal*, 556 U.S. at 679.

[^92]: N.Y. Gen. Bus. Law § 340-b; S.F. Admin. Code § 37.10C; Phila. Code §§ 9-802, 9-813.

[^96]: N.Y. Gen. Bus. Law § 349-a.

[^97]: Cal. Bus. & Prof. Code §§ 16729, 16756.1.

[^101]: See, e.g., Brief for the International Center for Law and Economics as *Amicus Curiae* in Support of Defendants-Appellees, *Gibson v. Cendyn Group, LLC*, No. 24-3576 (9th Cir. Dec. 26, 2024); Brief for the International Center for Law and Economics as *Amicus Curiae* in Support of Defendants-Appellees and Affirmance, *Cornish-Adebiyi v. Caesars Entertainment, Inc.*, No. 24-3006 (3d Cir. Mar. 31, 2025).

[^102]: See, e.g., Robert Phillips, *Pricing and Revenue Optimization* (2d ed. 2021); Ariel Ezrachi & Maurice E. Stucke, *Virtual Competition* 56–80 (2016) (acknowledging dynamic-pricing efficiencies while distinguishing from coordination harms).

[^103]: *Matsushita*, 475 U.S. at 588–89 (economic-implausibility analysis at summary judgment).

[^104]: Herbert Hovenkamp, *The Power of Antitrust Personhood*, 25 U. Pa. J. Bus. L. 891 (2023); see also *Antitrust and Algorithmic Pricing*, The Regulatory Review (July 12, 2025) (summarizing Hovenkamp's view that antitrust personhood likely excludes AI algorithms while preserving liability for persons who use algorithms to achieve illegal ends).

[^105]: 306 U.S. at 226–27.

[^106]: 791 F.3d at 314–15.

[^107]: Hovenkamp, *supra* note 104, at 891–99.

[^108]: 540 U.S. 398 (2004).

[^109]: *Id.* at 407–11.

[^110]: Brief for Antitrust Law and Economics Professors as *Amici Curiae*, *Cornish-Adebiyi*, *supra* note 55.

[^111]: Herbert Hovenkamp, *Antitrust and eMarkets*, 36 Stan. L. & Pol'y Rev. 147 (2025); Hovenkamp, *Antitrust and Algorithmic Pricing*, *supra* note 104.

[^vendor-person]: 15 U.S.C. § 7 (defining "person" to include corporations); see Areeda & Hovenkamp, *supra* note 26, ¶¶ 1402, 1474 (discussing the Sherman Act "person" requirement).

[^algo-property]: This is conventional doctrine and uncontroversial. Algorithms are property under personhood doctrine; the question of artificial-agent personhood is a separate (and largely speculative) question that the Note brackets. See *infra* Section VII.B.

[^vendor-architecture]: For the participant-in-agreement characterization, see, e.g., the Department of Justice's pleadings in *United States v. RealPage, Inc.*, *supra* note 4. For the *Interstate Circuit*-style coordination-mechanism characterization, see *Interstate Circuit*, 306 U.S. at 226–27 (the film distributor as coordination mechanism without itself being a participant).

[^calvano1]: Emilio Calvano, Giacomo Calzolari, Vincenzo Denicolò & Sergio Pastorello, *Artificial Intelligence, Algorithmic Pricing, and Collusion*, 110 Am. Econ. Rev. 3267 (2020).

[^calvano2]: *Id.*

[^brown-mackay1]: Zach Y. Brown & Alexander MacKay, *Competition in Pricing Algorithms*, 15 Am. Econ. J.: Microeconomics 109 (2023).

[^brown-mackay2]: *Id.*

[^harrington1]: Joseph E. Harrington, Jr., *Developing Competition Law for Collusion by Autonomous Artificial Agents*, 14 J. Competition L. & Econ. 331 (2018); see also more recent Harrington work cited in surveys at *infra* note ittoo-petit.

[^ittoo-petit]: Ashwin Ittoo & Nicolas Petit, *Algorithmic Pricing Agents and Tacit Collusion: A Technological Perspective*, in *L'intelligence artificielle et le droit* 241 (Hervé Jacquemin & Alexandre de Streel eds., 2017); Ariel Ezrachi & Maurice E. Stucke, *Sustainable and Unchallenged Algorithmic Tacit Collusion*, 17 Nw. J. Tech. & Intell. Prop. 217 (2020).

[^fre301]: Fed. R. Evid. 301; see *In re Yamashita*, 327 U.S. 1, 22 n.31 (1946) (Murphy, J., dissenting) (early articulation of the burden-of-production / burden-of-persuasion distinction in presumption analysis); Edward W. Cleary, *Presuming and Pleading: An Essay on Juristic Immaturity*, 12 Stan. L. Rev. 5 (1959) (foundational doctrinal treatment).

[^mcdonnell1]: *McDonnell Douglas Corp. v. Green*, 411 U.S. 792 (1973) (burden-of-production-shifting framework).

[^maple-flooring]: *Maple Flooring Mfrs. Ass'n v. United States*, 268 U.S. 563 (1925).

[^collab-guidelines]: Fed. Trade Comm'n & U.S. Dep't of Justice, *Antitrust Guidelines for Collaborations Among Competitors* § 3.31 (2000) (information-exchange analysis).

[^doj-info1]: See Statement of Interest of the United States at 2, 10–16, *In re RealPage, Inc., Rental Software Antitrust Litig.* (No. II), MDL No. 3071 (M.D. Tenn. Nov. 15, 2023), ECF No. 628 (articulating information-exchange theory in algorithmic-pricing context).

[^calibration1]: See Section III.C (*In re RealPage* MDL); Section III.D (*Duffy v. Yardi*).

