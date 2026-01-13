# Rapport : Intégration Synth-FR dans le Chapitre 3

> Notes de discussion pour l'ajout d'une section sur l'application française de la méthode.

## Source

- **Repository** : https://github.com/3podi/synth_fr
- **Auteur expérimentations** : Riccardo Tripodi (stagiaire APHP)
- **Collaboration** : Assistance Publique – Hôpitaux de Paris (AP-HP)

---

## Contexte

Application de la méthode de génération synthétique (reward-based generation) aux données cliniques françaises de l'APHP. Objectif : valider la généralisation multilingue de l'approche.

### Différences avec MIMIC-III (anglais)

| Aspect | MIMIC-III | APHP (Synth-FR) |
|--------|-----------|-----------------|
| Langue | Anglais | Français |
| Données | Discharge summaries | Rapports médicaux |
| Codes | ICD-9 | ICD-10 |
| Modèle générateur | Mistral-7B | Qwen 4B |
| Évaluateur | all-distilroberta-v1 | BioLORD-2023-M + LLM-as-judge |

---

## Pipeline

Identique à la méthode principale :
1. **SFT** : Fine-tuning supervisé sur seed set pseudo-anonymisé
2. **Generation** : Génération de candidats à partir de keywords cliniques
3. **Scoring** : Évaluation par score composite (voir ci-dessous)
4. **DPO** : Alignement itératif (3 itérations)
5. **Evaluation** : Classification ICD-10 multilabel

---

## Mécanisme de Scoring (Amélioré)

Score composite combinant plusieurs métriques :

### 1. Similarité Sémantique
- Modèle : **BioLORD-2023-M** (SentenceTransformer médical français)
- Méthode : embeddings globaux + fenêtre glissante (128 tokens)

### 2. Score Éducatif (LLM-as-judge)
Critères évalués :
- **Clarté** : grammaire, pas de phrases anglaises, ponctuation
- **Pertinence médicale** : plausibilité clinique, traitements réalistes
- **Absence d'hallucinations** : pas de phrases typiques LLM

### 3. Score de Similarité Médicale (LLM-as-judge)
- Compare le contenu médical entre documents réels et synthétiques
- Échelle 0-1

### 4. BLEU Score
- Sentence-level BLEU avec smoothing

### 5. Keyword Overlap
- Proportion de keywords seed présents dans le texte généré

**Score final** = moyenne cumulative (keyword overlap, educational score, semantic similarity)

---

## Résultats Classification ICD-10

### Dataset 10K

| Top-k | Step0 (baseline) | DPO1 | DPO2 | DPO3 | Gain relatif |
|-------|------------------|------|------|------|--------------|
| 20 | 0.3893 | **0.4223** | 0.4181 | 0.4181 | +7.4% |
| 50 | 0.2498 | 0.2873 | 0.3073 | **0.3171** | +26.9% |
| 100 | 0.1747 | 0.2089 | 0.2282 | **0.2384** | +36.5% |

### Dataset 20K

| Top-k | Step0 (baseline) | DPO1 | DPO2 | DPO3 | Gain relatif |
|-------|------------------|------|------|------|--------------|
| 20 | 0.4129 | 0.4171 | **0.4217** | 0.4198 | +2.1% |
| 50 | 0.2988 | 0.3241 | 0.3389 | **0.3473** | +16.2% |
| 100 | 0.1954 | 0.2432 | 0.2701 | **0.2849** | +45.8% |

### Dataset 50K

| Top-k | Step0 (baseline) | DPO1 | DPO2 | DPO3 | Gain relatif |
|-------|------------------|------|------|------|--------------|
| 20 | 0.4298 | 0.4351 | **0.4396** | 0.4382 | +2.3% |
| 50 | 0.3256 | 0.3512 | 0.3698 | **0.3828** | +17.6% |
| 100 | 0.2302 | 0.2756 | 0.3012 | **0.3159** | +37.2% |

---

## Observations Clés

1. **Gains plus importants pour top-k élevé** : Cohérent avec MIMIC-III
2. **DPO1 souvent suffisant pour top-20** : Rendements décroissants
3. **Amélioration continue jusqu'à DPO3 pour top-100** : Labels rares bénéficient plus
4. **Scaling avec taille dataset** : 50K > 20K > 10K

---

## Comparaison Cross-lingue (MIMIC-III vs APHP)

| Métrique | MIMIC-III (anglais) | APHP (français) |
|----------|---------------------|-----------------|
| Gain top-100 (meilleur) | ~+30-40% | +37-46% |
| Effet DPO itératif | ✓ Confirmé | ✓ Confirmé |
| Rendements décroissants top-20 | ✓ Observé | ✓ Observé |
| Bénéfice labels rares | ✓ Fort | ✓ Fort |

**Conclusion** : Tendances similaires, méthode généralisable.

---

## Ressources Disponibles (HuggingFace)

- Modèle Qwen 4B fine-tuné
- LoRA modules par itération DPO
- Datasets 50K samples par step
- Dataset MedGemma français (300K samples)

---

## TODO

- [ ] **Confirmer taille seed set SFT** : Configs yaml montrent 100 (dev?), valeur production inconnue
- [ ] Obtenir métriques SemScore/BioLORD par itération si disponibles
- [ ] Confirmer ressources computationnelles utilisées

---

## Plan d'Intégration

### Position dans le chapitre
Après Section 7 (AlpaCare), avant Section 8 (Advanced Quality Evaluation)

### Structure proposée

```
\section{Application to French Clinical Data}
\label{sec:french-application}

\subsection{Motivation and Context}
\subsection{Experimental Setup}
\subsection{Enhanced Scoring Mechanism}
\subsection{Results}
\subsection{Cross-lingual Comparison}
\subsection{Discussion}
```

### Acknowledgements
```latex
\section*{Acknowledgements}
This work on French clinical data was conducted in collaboration with
Assistance Publique – Hôpitaux de Paris (AP-HP). We thank Riccardo Tripodi
for implementing and running the experiments on French medical reports.
```

---

## Décisions Prises

1. ✅ Section complète (~1.5-2 pages)
2. ✅ Acknowledgement pour Riccardo Tripodi
3. ✅ Position : après AlpaCare
4. ✅ Comparaison cross-lingue avec MIMIC-III
5. ✅ Discussion sur généralisation multilingue médicale
