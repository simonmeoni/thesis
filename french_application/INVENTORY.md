# Inventaire du manuscrit — Résumé substantiel

Source : scan des chapitres `sources/chapters/` (avril 2026).
Usage : alimenter la rédaction du résumé de 15 pages (`main.tex`).

---

## Fil narratif central

**Question de recherche** : Comment générer des documents cliniques synthétiques utiles pour le TAL médical tout en maîtrisant le risque de réidentification ?

**Approche** : *Facsimile* (fac-similé). Documents synthétiques ancrés dans des narratifs réels via extraction de mots-clés UMLS, sans jamais exposer le texte patient. Seuls mots-clés et scores numériques traversent la frontière de confidentialité.

**Trois contributions interconnectées** :
1. Génération guidée par mots-clés + raffinement par récompense (DPO itératif)
2. Analyse de la vie privée (attaques de réidentification) + stratégies d'atténuation
3. Distillation LLM pour annotation faible multilingue (souveraineté des données)

---

## Chapitre 1 — Introduction

- 80 % des données cliniques sont non structurées (notes médecins, comptes rendus)
- Progrès TAL clinique piloté par l'échelle : GatorTron (90 Mds mots), Med-PaLM 2 (86,5 % MedQA)
- Tension fondamentale : appétit en données vs. RGPD/HIPAA
- Limite de l'anonymisation : 87 % population US réidentifiable par (sexe, date naissance, code postal 5 chiffres) [Sweeney 2002]
- 4 questions de recherche (RQ1 génération, RQ2 utilité aval, RQ3 annotation LLM, RQ4 confidentialité)

## Chapitre 2 — État de l'art

- Ressources : MIMIC-III/IV, i2b2/n2c2, E3C (5 langues), FRASIMED, ClinText-SP, MMedC
- Augmentation : back-translation, templates, Synthea, génération neurale
- Alignement : DPO, RLHF, self-training
- Confidentialité : DP-SGD, DP-SFT, pseudonymisation
- Approche concurrente : **KnowledgeSG** (génération pure depuis ontologie, sans données réelles)

## Chapitre 3 — Génération fac-similé (MIMIC-III)

**Architecture**
- Frontière de confidentialité : seuls mots-clés UMLS et scores numériques traversent
- Extraction : QuickUMLS (codes CIM-9, procédures, médicaments, symptômes)
- Générateur : Mistral-7B-Instruct
- Pipeline : SFT sur ~3 500 documents d'amorçage → 3 itérations DPO (DPO1, DPO2, DPO3)
- Scoreur contrastif : BioLORD / SciBERT (similarité sémantique réel vs. synthétique)

**Résultats CIM-9 (macro F1)**

| Configuration | Top-20 | Top-50 | Top-100 |
|---|---|---|---|
| SFT | 0,520 | 0,289 | 0,145 |
| DPO1 | 0,527 | 0,301 | 0,164 |
| DPO2 | 0,528 | 0,314 | 0,172 |
| **DPO3** | **0,533** | **0,326** | **0,187** |

- Top-20 : DPO1 suffit (plateau rapide)
- Top-50/100 (labels rares) : gains continus jusqu'à DPO3
- Mix 50 % réel + 50 % synthétique compétitif avec 100 % réel

## Chapitre 4 — Améliorations DPO (AlpaCare)

- Candidats : 4 par prompt (1 basse température τ=0,2 + 3 haute τ ∈ [0,6 ; 0,9])
- Paires de préférence : top-score préféré, bottom-score rejeté
- Complexité de la tâche pilote la profondeur d'alignement

## Chapitre 5 — Application française (AP-HP, CIM-10)

**Particularités**
- Aucune dépendance à des documents réels : corpus d'amorçage entièrement synthétique via MedGemma-27B-IT sur mappings CIM-10 ↔ mots-clés français
- Générateur : Qwen3-4B-Instruct, LoRA (r=32, α=64)
- Scoreur composite : BioLORD-2023-M + Qwen3-30B-A3B-Instruct comme LLM-juge
- Classifieur aval : ModernBERT-large
- Structure à 8 sections standardisées (Motif, Antécédents, Histoire, etc.)

**Résultats CIM-10 (macro F1, 50K synthétiques)**

| Configuration | Top-20 | Top-50 | Top-100 |
|---|---|---|---|
| SFT | 0,445 | 0,326 | 0,230 |
| DPO3 | **0,461** | **0,385** | **0,316** |
| Gain | +2,3 % | +17,6 % | **+37,2 %** |

- Gains français beaucoup plus larges qu'anglais sur labels rares (attribué au scoreur composite)
- Validation translinguistique : méthodologie agnostique à la langue et au système de codage
- Découplage possible des données réelles d'amorçage

## Chapitre 6 — Annotation faible multilingue (E3C, 5 langues)

**Tâche** : NER clinique IOB, 3 labels (O, B_clin, I_clin)

**Stratégie** : annotation par InstructGPT-3 (text-davinci-003) + dictionnaire UMLS + mélange pondéré r_mix dans [0, 1] pour distillation vers modèles encodeurs locaux

**Résultats (F1, gold test)**

| Langue | Dict seul | LLM seul | Mix optimal | r_mix optimal |
|---|---|---|---|---|
| Anglais | 0,72 | 0,71 | 0,72 | 0,0 |
| Espagnol | 0,73 | 0,71 | **0,75** | 0,4 |
| Français | 0,69 | 0,74 | **0,76** | 0,5 |
| Italien | 0,63 | 0,75 | **0,77** | 0,8 |
| Basque | 0,65 | 0,78 | **0,78** | 1,0 |

**Observations**
- LLM ~2x plus d'entités extraites que dictionnaire (multi-mots)
- Dictionnaire : précision haute, recall étroit
- Distillation souvent supérieure au LLM direct (italien : +0,12)
- Grand bénéfice LLM sur langues à ressources faibles (basque)

## Chapitre 7 — Analyse de confidentialité et atténuation

**Modèles de menace**
- Linkage 1-vs-N (100 candidats) : attribution globale
- Discrimination 1-vs-2 : distinction binaire (menace plus forte)
- Métriques : TF-IDF (lexical), BioLORD (sémantique)

**Résultats de base (MIMIC-III)**

| Attaque | Métrique | Succès |
|---|---|---|
| Linkage (N=100) | TF-IDF | 45 % |
| Linkage (N=100) | BioLORD | 52 % |
| Discrimination (N=2) | TF-IDF | 89 % |
| Discrimination (N=2) | BioLORD | **96 %** |

**Cause** : combinaisons de mots-clés UMLS encodent des empreintes patient distinctives.

**Atténuation**

| Stratégie | Linkage | Discrimination | F1 aval |
|---|---|---|---|
| Base | 45 % | 89 % | 0,533 |
| Reformulation | 42 % | 85 % | 0,520 |
| **Perturbation mots-clés** | **28 %** | **62 %** | 0,518 |
| Combinée | 25 % | 58 % | 0,510 |

**Arbitrage** : perturbation de mots-clés, réduction de 37 % du linkage pour seulement 3 % de perte d'utilité.

**Amplification DPO** : l'alignement par préférence augmente le risque de réidentification vs. SFT (optimisation vers similarité aux documents réels renforce les empreintes).

## Chapitre 8 — Discussion

- Fac-similé vs. KnowledgeSG : fidélité structurelle vs. scalabilité pure
- Fac-similé excelle : rareté de données, déploiement inter-institutionnel rapide, préservation de style
- KnowledgeSG excelle : zéro données réelles, échelle massive
- Limites : multimodalité, couverture domaines/langues, garanties formelles (DP)

## Chapitre 9 — Conclusion

**Réponses aux RQ** (toutes positives avec nuances)
- RQ1 OK avec injection ontologique + raffinement par récompense
- RQ2 OK complément, pas substitut, bénéfices max en régime faibles ressources
- RQ3 OK complémentarité LLM+dictionnaire, distillation préserve souveraineté
- RQ4 OK risques réduits mais non nuls, atténuation par perturbation des mots-clés

**Perspectives**
- Dossiers patients multimodaux longitudinaux
- Passage à l'échelle domaines/langues
- Découplage total des données réelles (pseudo-mots-clés depuis ontologie)
- Garanties formelles (DP + utilité)
- Applications hors santé : juridique, financier

**Vision** : innovation responsable, reconnaissance honnête des limites.

---

## Glossaire clé

| EN | FR |
|---|---|
| Synthetic data | Données synthétiques |
| Facsimile documents | Documents fac-similé |
| Linkage attack | Attaque par liaison |
| Discrimination attack | Attaque de discrimination |
| DPO | Optimisation par préférence directe |
| Knowledge distillation | Distillation de connaissances |
| Weak supervision | Supervision faible |
| Privacy-utility trade-off | Arbitrage confidentialité-utilité |
| Re-identification risk | Risque de réidentification |
| ICD-9 / ICD-10 | CIM-9 / CIM-10 |
| UMLS | Unified Medical Language System |
| EHR | DME (Dossier Médical Électronique) |

## Corpus

| Corpus | Langue(s) | Taille | Tâche |
|---|---|---|---|
| MIMIC-III | Anglais | 50K+ séjours USI | CIM-9, NER |
| AP-HP | Français | 10K-50K synthétiques | CIM-10 |
| E3C-3.0 | 5 langues EU | ~1500-3100/langue | NER clinique |
| AlpaCare | Anglais | ~10K synthétiques | CIM-9, NER |
