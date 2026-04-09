# Inventaire du manuscrit — Résumé substantiel

Source : scan des chapitres `sources/chapters/` (avril 2026).
Usage : alimenter la rédaction du résumé de 15 pages (`main.tex`).


---

## ⚠️ Statut de vérification (avril 2026)

- **Chapitres 3 (fac-similé + DPO)** : chiffres vérifiés contre `figures/synthetic_generation_cl4health_2025/task_results.csv` et le texte de `sources/chapters/synthetic_generation_cl4health_2025.tex`
- **Chapitre 6 (vie privée)** : chiffres vérifiés contre `sources/chapters/synthetic_generation_improvements.tex` (ATTENTION : ce fichier contient en fait le chapitre Privacy, pas des améliorations DPO)
- **Chapitre 4 (français)** : chiffres vérifiés contre `sources/chapters/french_clinical_application.tex`
- **Chapitre 5 (annotation faible)** : chiffres vérifiés contre `sources/chapters/weak_annotations.tex` et tables dans `figures/multi_weak_supervision/`
- **Correspondance fichiers → chapitres manuscrit** :
  - `synthetic_generation_cl4health_2025.tex` → Ch. Fac-similé + DPO (`chap:synthetic`)
  - `french_clinical_application.tex` → Ch. Application française (`chap:french-application`)
  - `weak_annotations.tex` → Ch. Annotation faible / distillation (`chap:distillation`)
  - `synthetic_generation_improvements.tex` → Ch. **Vie privée** (`chap:privacy`, nom trompeur)
  - `discussion.tex` → Ch. Discussion (`chap:discussion`)

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
- Générateur : Mistral-7B-Instruct-v0.1
- Évaluateur/scoreur : all-distilroberta-v1 (SemScore, similarité sémantique réel vs. synthétique)
- Pipeline : SFT sur seed pseudo-anonymisé (ratios r_sft = 4 % et 6 %) → **2 itérations DPO** (step 0 = SFT, step 1 = DPO-1, step 2 = DPO-2)
- N = 4 candidats générés par séquence de mots-clés à chaque étape

**Tâches d'évaluation aval**
- Classification multilabel CIM-9 à 4 niveaux de granularité : `class-20`, `class-50`, `class-100`, `class-400` (label spaces croissants, distribution en loi de puissance)
- NER clinique
- Métrique : **Micro-F1** (pas macro)

**Résultats principaux (Micro-F1, en %)**

| Dataset | class-20 | class-50 | class-100 | class-400 | NER |
|---|---|---|---|---|---|
| `baseline` (few-shot) | 45,7 | 33,8 | 26,6 | 10,6 | — |
| `D_gold` (réel) | 49,3 | 33,3 | 23,0 | 4,9 | 57,0 |
| `D_gold × 4` (oversampling) | **53,7** | 42,5 | 35,0 | 26,4 | 61,6 |
| `D_0^4%` (SFT) | 49,8 | 38,7 | 32,2 | 24,2 | — |
| `D_0^6%` (SFT) | 49,9 | 38,5 | 31,0 | 23,9 | 59,6 |
| `D_1^4%` (DPO-1) | 50,9 | 41,1 | 33,9 | 26,9 | — |
| `D_1^6%` (DPO-1) | 51,2 | 40,7 | 33,7 | 24,5 | 59,4 |
| `D_2^4%` (DPO-2) | 50,6 | 41,0 | 34,3 | 27,0 | — |
| `D_2^6%` (DPO-2) | 51,7 | 40,7 | 31,9 | 26,5 | 59,4 |
| `D_{0,1,2}^6%` (mixé) | 52,4 | **43,1** | **37,2** | **31,0** | **61,7** |

**Observations clés**
- Les données synthétiques dépassent largement `D_gold` sur les tâches complexes : class-100 (37,2 vs. 23,0) et surtout class-400 (31,0 vs. 4,9)
- L'oversampling `D_gold × 4` domine class-20 mais est rattrapé sur les tâches plus granulaires par le mix de générations synthétiques
- **Le mélange des 3 générations** (`D_{0,1,2}^6%`) est la meilleure configuration synthétique : l'alignement itératif enrichit la diversité plutôt qu'il ne remplace les générations antérieures
- Anomalie : sur class-100 en 6 %, D_2 dégrade vs D_1 (31,9 vs 33,7) — instabilité signalée
- Les écarts-types sont plus faibles sur synthétique que sur `D_gold` : entraînement plus stable
- Sur NER, à nombre de tokens annotés équivalent, M_gold (57,0) et M_2^6% (56,6) sont quasi identiques

**SemScore à travers les itérations (exemples)**
- `GenMdl{4%}` évalué par `ScoreMdl{4%}` : 67,95 → 71,53 → 72,25 (step 0 → 1 → 2)
- `GenMdl{6%}` évalué par `ScoreMdl{6%}` : 67,26 → 70,78 → 74,37

## Chapitre 4 — Application française (AP-HP, CIM-10) [chiffres vérifiés]

**Contexte**
- Collaboration avec l'AP-HP (Assistance Publique -- Hôpitaux de Paris)
- Travail réalisé par Riccardo Tripodi (master Politecnico di Milano) adaptant le pipeline au contexte français
- Motivation : déployer de petits modèles efficaces pour le codage CIM-10 automatisé dans un contexte de rareté d'annotations et de contraintes RGPD

**Particularités méthodologiques**
- **Aucune dépendance à des documents réels** : le corpus d'amorçage est entièrement synthétique (pas de pseudo-anonymisation comme dans MIMIC)
- Corpus d'amorçage : \num{20000} rapports cliniques synthétiques générés par **MedGemma-27B-IT** à partir d'une base curée mappant codes CIM-10 vers mots-clés français (symptômes, anatomie, traitements, procédures)
- Échantillonnage des codes selon les fréquences hospitalières empiriques
- **Corpus de référence pour le scoring** : rapports cliniques *fictifs* rédigés par des médecins praticiens (pas des documents patients réels). Cliniquement réalistes mais sans information patient
- **Jeu de test d'évaluation** : rapports cliniques réels annotés par des experts, strictement disjoint du reste du pipeline
- Structure à 8 sections standardisées : Motif d'hospitalisation, Antécédents, Mode de vie, Histoire de la maladie, Examen clinique, Examens complémentaires, Évolution, Conclusion
- Longueur moyenne des documents générés : ≈ 800 ± 240 mots

**Pipeline d'entraînement**
- **Générateur** : Qwen3-4B-Instruct (vs. Mistral-7B-Instruct-v0.1 pour MIMIC), choisi pour ses capacités multilingues
- **LoRA** : rang r=32, scale α=64, sur toutes les projections d'attention
- **Stage 1 (SFT)** : ajustement supervisé sur les \num{20000} rapports d'amorçage
- **Stage 2 (DPO)** : **3 itérations** d'optimisation de préférence directe (DPO1, DPO2, DPO3)  
  ⚠️ Différence avec MIMIC qui n'avait que 2 itérations DPO
- **Génération de candidats** : N=4 par prompt de mots-clés, avec mélange de températures (1 × τ=0,2 pour cohérence + 3 × τ ∼ U(0,6 ; 0,9) pour diversité)
- Extraction de mots-clés des références par QuickUMLS

**Scoreur composite**
- Composant 1 : similarité cosinus via BioLORD-2023-M (embeddings médicaux intégrant un graphe de connaissances clinique)
- Composant 2 : Qwen3-30B-A3B-Instruct comme LLM-juge (correction médicale, alignement au contenu de la référence)
- Score final : moyenne simple `S_composite = 0,5 · S_similarity + 0,5 · S_judge`
- Ce scoreur à deux facettes fournit un signal d'entraînement plus riche que le SemScore seul utilisé sur MIMIC

**Tâche aval**
- Classification multilabel CIM-10 par ModernBERT-large
- Top-k ∈ {20, 50, 100} codes les plus fréquents
- 3 tailles de dataset : 10K, 20K, 50K documents synthétiques
- Moyennes de codes/document : 1,52 ± 0,82 (top-20), 2,10 ± 1,14 (top-100)
- Métrique : **macro F1** (différent de MIMIC qui utilise Micro-F1)

**Résultats complets (macro F1)**

| Dataset | Top-k | Step0/SFT | DPO1 | DPO2 | DPO3 | Gain (best vs Step0) |
|---|---|---|---|---|---|---|
| **10K** | 20 | 0,389 | **0,422** | 0,422 | 0,418 | +7,4 % |
| 10K | 50 | 0,250 | 0,294 | 0,302 | **0,317** | +26,9 % |
| 10K | 100 | 0,175 | 0,197 | 0,202 | **0,238** | +36,5 % |
| **20K** | 20 | 0,438 | **0,457** | 0,448 | 0,447 | +2,1 % |
| 20K | 50 | 0,299 | 0,326 | 0,334 | **0,347** | +16,2 % |
| 20K | 100 | 0,195 | 0,230 | 0,210 | **0,285** | **+45,8 %** |
| **50K** | 20 | 0,445 | **0,461** | 0,461 | 0,455 | +2,3 % |
| 50K | 50 | 0,326 | 0,351 | **0,385** | 0,383 | +17,6 % |
| 50K | 100 | 0,230 | 0,268 | 0,300 | **0,316** | +37,2 % |

**Observations clés**
- **Top-20 : DPO1 suffit**, les itérations suivantes plafonnent ou dégradent légèrement
- **Top-50 : optimal entre DPO2 et DPO3**
- **Top-100 : DPO3 est systématiquement le meilleur** (labels rares bénéficient d'un alignement plus profond)
- **Gain maximal : +45,8 %** sur 20K top-100 (pas sur 50K comme indiqué précédemment à tort)
- Même le plus petit dataset (**10K + DPO3**) atteint une performance compétitive → la qualité peut partiellement compenser la quantité
- Scaling cohérent : 50K > 20K > 10K en valeur absolue sur toutes les configurations

**Comparaison inter-lingue (MIMIC ↔ AP-HP)**
- **Gains qualitatifs identiques** : DPO efficace surtout sur tâches complexes, rendements décroissants sur top-20
- **Gains quantitatifs très différents** : français +36-46 % sur top-100 vs. anglais seulement +3-6 %
- Explication principale : scoreur composite (BioLORD + LLM-juge) vs. SemScore seul
- Facteurs secondaires : Qwen3-4B peut répondre mieux au DPO que Mistral-7B, CIM-10 vs. CIM-9

**Conclusion du chapitre**
- Preuve que la méthodologie **transfère à une autre langue, un autre système de codage, un autre contexte hospitalier**
- Preuve qu'il est possible de **découpler totalement l'amorçage des données patient réelles**
- Pistes ouvertes : dossiers patients complets multimodaux, génération longue (sommaires de sortie complets)

## Chapitre 5 — Annotation faible multilingue (E3C, 5 langues) [chiffres vérifiés]

**Source** : `sources/chapters/weak_annotations.tex`, tables dans `figures/multi_weak_supervision/` et `figures/weak_supervision_healthnlp_2023/`. Publié à BioNLP 2023 (volet français) puis étendu multilingue.

**Tâche** : NER clinique IOB, 3 labels (O, B_clin, I_clin), corpus E3C (5 langues : anglais, espagnol, français, italien, basque).

**Sources de supervision comparées**
- **\dict (r_mix = 0)** : annotation par dictionnaire UMLS (précision haute, rappel étroit, favorise les entités mono-mot)
- **\instruct (r_mix = 1)** : annotation par InstructGPT-3 (`text-davinci-003`, déterministe T=0, top_p=0), prompt few-shot à 3 exemples. InstructGPT extrait ~2× plus d'entités que le dictionnaire, notamment des I_clin multi-mots
- **\hybridmodel (r_mix ∈ (0,1))** : mélange pondéré des deux sources

**Protocole**
- Trois couches E3C : S_silver (corpus annoté dict + LLM, entraînement 5-fold CV), S_val (sous-ensemble validé manuellement), S_gold (test)
- Étudiants distillés : modèles encodeurs locaux (monolingues et multilingues) — camembert-base et DrBERT (fr), dbmdz (it), berteus (eu), BSC-LT biomedical-es (es), Bio_ClinicalBERT (en), xlm-roberta-base en contexte multilingue
- Entraînement avec r_mix ∈ [0,1] puis évaluation sur S_gold

**Résultats clés agrégés (moyenne toutes langues, F1)**
- Sur S_silver : distil (r=1) 0,70 vs dict (r=0) 0,67
- Sur S_val : distil 0,61 vs dict 0,70 (peu de données favorise dict stable)
- Sur S_star (S_silver + S_val mixte) : distil 0,73 vs dict 0,71

**Comparaison InstructGPT direct vs modèle distillé sur S_gold**
- Italien : 0,63 (InstructGPT direct) → 0,75 (distillé), gain +0,12
- Français, Basque : distillation bénéfique également
- Anglais, Espagnol : tendance inversée, InstructGPT direct meilleur

**Mélange optimal r_mix (contexte monolingue, meilleur modèle par langue, table `big_table_D`)**

| Langue | Modèle | r_mix_max | F1 (r=1) | F1 (r_max) | F1 (r=0) |
|---|---|---|---|---|---|
| Anglais | Bio_ClinicalBERT | 0,6 | 0,68 | **0,72** | 0,66 |
| Espagnol | BSC-LT biomedical-es | 0,4 | 0,78 | **0,79** | 0,72 |
| Français | camembert-base | 0,5 | 0,74 | **0,76** | 0,75 |
| Italien | dbmdz bert-italian | 0,8 | 0,73 | **0,75** | 0,74 |
| Basque | berteus-base | 1,0 (bord) | 0,54 | **—** | 0,60 |

**Observations**
- Pour 4 langues sur 5, l'optimum se situe dans r_mix ∈ [0,4 ; 0,6] : le mélange des deux supervisions apporte un gain de diversité
- Basque : cas particulier, optimum à r_mix = 1 ; lexique UMLS basque pauvre (63 tokens I_clin dict vs 482 pour InstructGPT sur S_silver), le dictionnaire sous-extrait fortement
- Multilingue (xlm-roberta-base) inférieur au monolingue sauf italien (+0,01 à r_mix = 0,8) : bruit introduit par la multi-langue
- Cas d'étude français détaillé : r_mix = 0,5 donne F1 = 0,76, précision = 0,73, rappel = 0,81, écart précision/rappel réduit. Ratios > 0,5 améliorent la stabilité cross-fold

**Contributions pour le résumé**
1. Annotation faible par LLM (précurseur 2023) comme source de supervision pour la distillation
2. Ratio r_mix explicite pour combiner supervision dictionnaire et LLM, gain net dans 4 langues sur 5
3. Démonstration que la distillation vers un petit modèle encodeur peut dépasser l'inférence LLM directe (italien +0,12)
4. Analyse multilingue montrant les limites des modèles multilingues face aux monolingues en NER clinique
5. Complémentarité précision/rappel entre dict (sous-extraction) et LLM (sur-extraction), base théorique du mélange

## Chapitre 6 — Analyse de confidentialité et atténuation [chiffres corrigés]

**Corpus évalués**
- MIMIC-III avec ratios `r_sft ∈ {4 %, 6 %}` à DPO-2 (natural notes, filtrées > 5 docs/patient)
- AlpaCare à DPO-1 et DP-SFT (medical instructions conversationnelles, filtrage BioLORD k-means)

**Modèles de menace**
- **Attaque par liaison (1-vs-N)** : attribution d'un document synthétique à son patient source parmi N candidats
- **Attaque de discrimination (1-vs-2)** : distinction entre 2 candidats (menace plus forte)
- Métriques : TF-IDF (lexical), embeddings sémantiques (BioLORD / all-distilroberta)

**Résultats de base (baseline, taux de succès en %)**

| Corpus | Liaison TF-IDF | Liaison sémantique | Discrimination TF-IDF | Discrimination sémantique |
|---|---|---|---|---|
| MIMIC-III 4 % DPO-2 | 85,94 | 59,47 | 99,72 | 99,26 |
| MIMIC-III 6 % DPO-2 | **89,72** | 55,74 | **99,95** | 99,29 |
| AlpaCare DPO-1 | 77,88 | **81,99** | 98,38 | **99,89** |

**Observations clés**
- Sur MIMIC-III (notes cliniques naturelles), TF-IDF domine (86-90 %) vs. sémantique (56-59 %) : les patterns lexicaux (terminologie médicale) constituent le vecteur principal de fuite
- Sur AlpaCare (instructions conversationnelles), le sémantique domine (82 %) vs. TF-IDF (78 %) : contenu conversationnel fuit davantage par sémantique
- Les attaques de discrimination sont proches du taux maximal sur toutes les configurations DPO (97-99 %)

**Mitigation 1 — Reformulation standard (rephrasing)**

| Corpus | Liaison TF-IDF | Liaison sémantique | Discrimination TF-IDF | Discrimination sémantique |
|---|---|---|---|---|
| MIMIC-III 4 % DPO-2 | 83,73 (−2,21) | 51,19 (−8,28) | 98,87 (−0,85) | 98,75 (−0,51) |
| MIMIC-III 6 % DPO-2 | 84,99 (−4,73) | 48,43 (−7,31) | 99,73 (−0,22) | 99,23 (−0,06) |
| AlpaCare DPO-1 | 54,38 (−23,50) | 70,28 (−11,71) | 97,38 (−1,00) | 99,86 (−0,03) |

Réductions : 2-5 pp sur MIMIC-III, 12-24 pp sur AlpaCare. Reformulation générique insuffisante sur notes naturelles.

**Mitigation 2 — Perturbation des mots-clés UMLS**

| Corpus | Liaison TF-IDF | Liaison sémantique | Discrimination TF-IDF | Discrimination sémantique |
|---|---|---|---|---|
| MIMIC-III 4 % DPO-2 | 28,91 (**−57,03**) | 30,16 (−29,31) | 91,10 (−8,62) | 97,34 (−1,92) |
| MIMIC-III 6 % DPO-2 | 30,68 (**−59,04**) | 29,63 (−26,11) | 94,61 (−5,34) | 98,74 (−0,55) |
| AlpaCare DPO-1 | 14,41 (**−63,47**) | 44,40 (−37,59) | 86,72 (−11,66) | 99,62 (−0,27) |

Réductions massives du risque de liaison (−57 à −63 pp en TF-IDF). Discrimination reste élevée (86-99 %) car les paires similaires demeurent distinguables, mais l'attribution globale devient difficile.

**Synthèse arbitrage (AlpaCare)**
- DPO + reformulation : liaison −23,5 pp, −2,2 % d'utilité
- DPO + perturbation mots-clés : liaison −63,5 pp, −1,3 % d'utilité

**Amplification DPO** : DP-SFT est intrinsèquement plus privée (liaison ≈ 14 %) que DPO-1 (liaison 78 %) sur AlpaCare. L'alignement par préférence renforce les empreintes patient car il pousse le générateur à maximiser la similarité aux documents réels.

## Chapitre 7 — Discussion

- Fac-similé vs. KnowledgeSG : fidélité structurelle vs. scalabilité pure
- Fac-similé excelle : rareté de données, déploiement inter-institutionnel rapide, préservation de style
- KnowledgeSG excelle : zéro données réelles, échelle massive
- Limites : multimodalité, couverture domaines/langues, garanties formelles (DP)

## Chapitre 8 — Conclusion

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
