# Related work

Source check: 2026-10-22. This is a bounded, nonsystematic literature comparison, not a priority proof. The starting bibliography is Section 11.1 of *The Void: From Zero-Byte Responses to Continuation Control*, https://doi.org/10.5281/zenodo.23070524. Relevant entries from that bibliography are retained below, with verified primary-source links. No paper here is evidence for an inaccessible mechanism in GPT-4.

## System instructions and hierarchy

Eric Wallace, Kai Xiao, Reimar Leike, Lilian Weng, Johannes Heidecke, and Alex Beutel. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. 2024. arXiv:2404.13208. https://arxiv.org/abs/2404.13208

The paper trains privileged-instruction handling and evaluates robustness to conflicting instructions. The present analysis instead measures a provider-successful, zero-byte normal-stop endpoint under non-adversarial system ablations. It does not evaluate that training method or adversarial hierarchy security.

Anthropic. Prompting best practices. Claude Platform documentation, accessed 2026-10-22. https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

The role-prompting guidance describes system instructions as behavior-shaping context. This supports treating request configuration as part of evaluation, not a claim that the present framing is the only way to produce empty output. The earlier `/system-prompts` URL redirects to this page.

## Prompt sensitivity

Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane Suhr. Quantifying Language Models' Sensitivity to Spurious Features in Prompt Design or: How I learned to start worrying about prompt formatting. ICLR, 2024; preprint 2023, arXiv:2310.11324. https://arxiv.org/abs/2310.11324

Yao Lu, Max Bartolo, Alastair Moore, Sebastian Riedel, and Pontus Stenetorp. Fantastically Ordered Prompts and Where to Find Them: Overcoming Few-Shot Prompt Order Sensitivity. Proceedings of ACL, Volume 1: Long Papers, pp. 8086-8098, 2022. https://doi.org/10.18653/v1/2022.acl-long.556

These works establish sensitivity to formatting and example order. The present intervention changes system-instruction content; its principal measured endpoint is empty versus nonempty output with provider termination metadata. The surveyed evaluations do not supply this paper's model-specific ablation table.

## Selective prediction, calibration and refusal

Yonatan Geifman and Ran El-Yaniv. SelectiveNet: A Deep Neural Network with an Integrated Reject Option. Proceedings of the 36th International Conference on Machine Learning, PMLR 97:2151-2159, 2019. https://proceedings.mlr.press/v97/geifman19a.html.

Saurav Kadavath et al. Language Models (Mostly) Know What They Know. 2022. arXiv:2207.05221v4. https://arxiv.org/abs/2207.05221v4

Andy Arditi, Oscar Obeso, Aaquib Syed, Daniel Paleka, Nina Panickssery, Wes Gurnee, and Neel Nanda. Refusal in Language Models Is Mediated by a Single Direction. Advances in Neural Information Processing Systems 37, 2024. https://doi.org/10.52202/079017-4322. Author manuscript: https://arxiv.org/abs/2406.11717

SelectiveNet's reject option is not inherently textual. Kadavath et al. study confidence and self-evaluation, while Arditi et al. intervene on refusal-associated representations. These are important precedents for separating responding from not responding, but not equivalent operational definitions of a successful zero-visible-byte API response. A Void is not presumed to be calibrated abstention, refusal, or intentional withholding. The brief's claim that all abstention in these literatures is expressed in text is not retained.

## EOS and termination

Benjamin Newman, John Hewitt, Percy Liang, and Christopher D. Manning. The EOS Decision and Length Extrapolation. Proceedings of the Third BlackboxNLP Workshop on Analyzing and Interpreting Neural Networks for NLP, pp. 276-291, 2020. https://doi.org/10.18653/v1/2020.blackboxnlp-1.26.

Anthropic. Stop reasons and fallback. Claude Platform documentation, accessed 2026-10-22. https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons

Newman et al. study the consequences of EOS prediction for length extrapolation. Anthropic explicitly documents empty responses with `end_turn`, including a typical small nonzero token usage and tool-history explanations. A claim that no prior literature or documentation recognizes normal empty completion would therefore be false. Those documents do not establish this GPT-4 system-ablation result or its internal cause.

Rayan Pal. Separating Capability from Permission in a Language Model: Prerequisite-Conditioned Native Continuation Control with Frozen Content. Zenodo, 2026. https://doi.org/10.5281/zenodo.22730710

PCCG-2 is the program's engineered native-EOS intervention with frozen non-EOS logits. It is separate from the hosted API observations in this paper. Its intervention does not establish the mechanism of the Matrix's Voids.

## Supported gap

The surveyed research papers do not report the present endpoint-specific system-prompt ablation in GPT-4-0613, with frozen requests, byte counts, provider-normal stops, Near-Void accounting, and accompanying controls. This is a statement about the verified sources above, not a comprehensive negative about all literature. The contribution is the reproducible model-specific interaction in already public evidence, not the discovery of abstention, system-prompt sensitivity, or EOS itself.
