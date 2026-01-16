# Notes pour la Discussion de Thèse

## Session de Questions/Réponses - Chapitre par Chapitre

Date: 2026-01-15

---

## CHAPITRE 3 : Synthetic Generation (Reward-based)

### Question 1a : Choix architectural - Facsimile vs Pure Generation

**Contexte :** Tu génères des documents synthétiques à partir de seed documents réels (pseudo-anonymisés) et de keywords UMLS extraits. KnowledgeSG génère depuis zéro sans seed documents.

**Question :** Pourquoi ce choix architectural ? Quel trade-off ? Quel cas d'usage ?

**Réponse :**

**Ton choix "facsimile" (seed documents + keywords) repose sur 4 piliers :**

1. **Gap terrain vs open-source** :
   - Les documents hospitaliers réels ont des caractéristiques sémantiques, structurelles et terminologiques très différentes des datasets publics (MIMIC)
   - Pour entraîner des modèles qui marchent sur le terrain, il faut capter ces patterns spécifiques

2. **Fidélité maximale SANS réidentification directe** :
   - Tu veux que les synthétiques ressemblent au maximum aux vrais documents de l'hôpital (structure narrative, flow clinique)
   - Mais en utilisant **seulement des keywords UMLS** (ontologie médicale), tu garantis qu'**aucune information identifiante** (noms, dates, lieux) ne traverse la frontière privé→public

3. **Approche hybride privacy-by-design** :
   - Contrairement à KnowledgeSG (pure generation), ton approche permet d'**ancrer** les synthétiques dans la réalité terrain
   - Tout en gardant la possibilité d'appliquer DP ou d'autres mécanismes privacy (ce que tu explores au chapitre 4)
   - Tu couvres deux cas : hôpitaux avec peu de données réelles (seed) ET besoin de garanties privacy fortes

4. **Validation empirique sur données françaises de terrain** :
   - Le Chapitre 5 montre que cette approche (distillation, weak supervision) **fonctionne bien** sur des documents français cliniques réels
   - Notamment sur E3C et **Partage (APHP)** : documents synthétiques faits main par des médecins
   - Cela valide que capter les patterns de terrain (via seed documents) n'est pas juste théorique mais **nécessaire pour la généralisation**

---

### Question 1b : Nécessité de l'approche avec du recul

**Question :** Avec du recul, l'approche "facsimile" était-elle vraiment nécessaire ? Aurais-tu pu obtenir des résultats comparables avec pure generation (KnowledgeSG) + bon prompting ?

**Réponse :**

**Pourquoi l'approche seed-based + keywords + RL était nécessaire (et reste pertinente) :**

1. **Contrainte déploiement hospitalier** :
   - Les hôpitaux ne peuvent pas utiliser d'APIs externes (RGPD, souveraineté)
   - Il faut des **petits modèles** (7B-13B) hostables sur infrastructure locale
   - L'approche par keywords + FT permet d'utiliser ces petits modèles avec de bonnes performances

2. **Bootstrap cohérent + self-learning** :
   - Les seed documents réels garantissent un **point de départ ancré dans la réalité terrain**
   - Le reward mechanism (RL/DPO) permet ensuite d'**améliorer avec plus de données synthétiques**
   - C'est un cycle vertueux : seed → génération → scoring → amélioration

3. **Données réelles > prompting few-shot** :
   - Même avec "le meilleur prompt ever", le few-shot sur modèles fermés reste **moins fiable** que du fine-tuning sur vraies données
   - Les vrais documents capturent des patterns subtils (vocabulaire, structure, flow clinique) qu'un prompt ne peut pas encoder

4. **Meilleur contrôle avec RL + FT** :
   - Sur petits modèles, le fine-tuning + reward donne des **garanties de qualité et de contrôle**
   - Tu peux **monitorer, versionner, auditer** le modèle (important pour la sécurité hospitalière)

5. **Honnêteté : LLMs modernes changent la donne** :
   - Les modèles avec très long contexte (Gemini 1M, Claude 200k) pourraient permettre des **approches différentes** (ex: in-context learning massif)
   - Mais en 2023-2024, pour des modèles 7B-13B hostables à l'hôpital, l'approche seed-based était le **bon choix**

---

### Question 2a : Avantages du reward mechanism vs SFT

**Contexte :** Tu utilises un scorer privé qui compare synthetic vs real pour aligner via DPO (Direct Preference Optimization).

**Question :** Quel est l'avantage réel de ce reward-based approach par rapport à un simple SFT ? Est-ce que le gain de qualité justifie les coûts (computationnel + privacy risk) ?

**Réponse :**

**Avantages du reward mechanism (DPO) qui justifient les coûts :**

1. **Privacy-by-design via logits seulement** :
   - Le scorer privé retourne **seulement des scores numériques (floats/logits)**, pas les documents réels
   - Cela respecte la **frontière privacy** : aucune donnée textuelle ne traverse de privé → public
   - C'est un signal d'entraînement **safe** car declassifié (seulement des nombres)
   - Tu peux aussi utiliser des **évaluateurs externes** qui évaluent seulement le document généré, sans accès au réel

2. **Signal d'apprentissage fort et prouvé** :
   - Les résultats montrent que DPO améliore significativement la qualité
   - Même sur **données françaises de terrain** (Chapitre 5), le signal d'apprentissage via reward est efficace
   - Ça justifie le coût computationnel

3. **Nuance sur le coût privacy** :
   - **Pas d'identification directe** : les keywords UMLS ne contiennent pas de PII
   - La **ré-identification** (linkage attacks) est un risque **théorique** démontré par des attaques adversariales
   - Le **post-processing** (keyword perturbation) réduit significativement le linkage attack
   - Dans ton contexte (hôpital), il faudrait **investiguer plus** l'application systématique de ce post-processing

**En résumé** : Le gain de qualité + le respect de la frontière privacy (via logits) **justifient** les coûts, surtout si on applique du post-processing pour mitiger la ré-identification.

---

### Question 2b : Refaire l'approche avec du recul ?

**Question :** Si tu devais refaire cette approche aujourd'hui, garderais-tu le reward mechanism tel quel ? Ou changerais-tu quelque chose ?

**Réponse :**

**Si tu devais refaire l'approche aujourd'hui - 3 directions à explorer :**

1. **Approche DP formelle combinée** (basée sur 2 articles) :
   - Combiner les garanties formelles de DP avec ton approche reward-based
   - Références :
     - Privacy-Preserving In-Context Learning with Differentially Private Few-Shot Generation (https://arxiv.org/pdf/2309.11765)
     - ACL 2024 Findings (https://aclanthology.org/2024.findings-acl.916.pdf)
   - DP by-design plutôt que post-processing empirique (keyword perturbation)

2. **Génération DP au niveau des tokens + few-shot ontologique** :
   - Appliquer DP **directement sur les tokens générés** pendant la génération
   - Utiliser du few-shot avec **choix sémantique ou ontologique** (UMLS, SNOMED) pour garantir une **data utility forte**
   - L'idée : DP by-design tout en préservant l'utilité via guidance ontologique

3. **Keywords DP-garantis pour scaler sur gros modèles** :
   - Garantir que les **keywords eux-mêmes sont DP et non réidentifiants** (via DP-SGD, ou autre mécanisme formel)
   - Utiliser ces keywords sur des **modèles plus gros** (GPT-4, Claude Opus) sans risque de ré-identification
   - Ça permettrait de **scaler** (plus de puissance) tout en gardant des garanties privacy fortes

---

### Question 3a : Interprétation des résultats downstream

**Contexte :** Les résultats montrent que les modèles entraînés sur synthetic data ($D_2^{4\%}$, $D_2^{6\%}$) surpassent ceux entraînés sur real data ($D_{gold}$) sur les tâches ICD-9, notamment sur les tâches complexes.

Exemples :
- Top-50 : $D_{gold}$ = 33.3, $D_2^{4\%}$ = 41.0 (+7.7 points)
- Top-100 : $D_{gold}$ = 23.0, $D_2^{4\%}$ = 34.3 (+11.3 points)

**Question :** Comment interprètes-tu ce résultat contre-intuitif ?

**Réponse :**

**Pourquoi le synthetic surpasse le real sur les tâches downstream (ICD-9) :**

1. **Augmentation du volume nécessaire** :
   - Le modèle a **besoin de plus d'exemples** pour apprendre, surtout sur les tâches complexes (Top-50, Top-100, Top-400)
   - Le synthetic fournit **4x plus de documents** que $D_{gold}$ (via N=4 candidates par keyword sequence)
   - Ce volume supplémentaire aide à mieux généraliser

2. **Hétérogénéité suffisante pour les labels rares** :
   - Sur les tâches complexes (Top-100, Top-400), il y a beaucoup de **labels rares** avec peu d'exemples
   - Le synthetic garantit une **diversité suffisante** (via le reward mechanism qui génère plusieurs candidates)
   - Cette hétérogénéité aide à mieux couvrir les combinaisons de labels rares

**En gros :** C'est un **vrai gain** lié au volume + diversité, pas juste un artefact. Le synthetic compense le manque de données réelles annotées.

---

### Question 3b : Cas d'usage réels - Quand utiliser le synthetic ?

**Question :** Dans quels cas d'usage réels recommanderais-tu d'utiliser ton approche vs simplement annoter plus de données réelles ? Où est la frontière ?

**Réponse :**

**Cas d'usage où le synthetic est clairement gagnant :**

1. **Peu de documents annotés disponibles** :
   - Quand tu as <1000 documents annotés, le synthetic permet de **bootstrapper** rapidement
   - Particulièrement pour les **labels rares** (Top-100, Top-400 dans tes expériences)

2. **Main d'œuvre d'annotation coûteuse dans le domaine clinique** :
   - L'annotation médicale nécessite des experts du domaine (coût élevé)
   - Le synthetic permet de **réduire massivement** le besoin en annotation humaine

3. **Besoin de scalabilité rapide** :
   - Nouveau domaine clinique (ex: passer de cardiologie à oncologie)
   - Nouveau cas d'usage (ex: nouvelle tâche NER sur un nouveau type de document)
   - Le synthetic permet de **scaler vite** sans attendre des mois d'annotation

4. **Contraintes de confidentialité** :
   - Hôpitaux qui ne peuvent pas externaliser l'annotation (RGPD)
   - Pas le droit d'envoyer à des annotateurs externes
   - Le synthetic permet de **générer localement** et d'annoter avec des modèles (GPT-4 via API sur synthetic, pas sur real)

**Frontière où le real reste préférable :**
- Si tu as déjà **>10k documents bien annotés** pour ta tâche spécifique, le gain marginal du synthetic diminue

---

---

## CHAPITRE 4 : Privacy Analysis and Mitigation

### Question 1 : Pourquoi faire ce chapitre privacy ?

**Contexte :** Beaucoup de travaux sur la génération de données synthétiques ne font pas d'évaluation rigoureuse des risques de ré-identification.

**Question :** Pourquoi as-tu décidé de faire un chapitre entier sur l'évaluation des risques privacy et les mitigations ?

**Réponse :**

**Pourquoi ce chapitre privacy :**

1. **D'abord une exigence, puis une conviction** :
   - C'était d'abord demandé (reviewers/directeur de thèse)
   - Mais ensuite c'est devenu une **conviction personnelle** que c'était nécessaire pour être honnête scientifiquement

2. **Découverte tardive de la dimensionnalité identification/ré-identification** :
   - Tu as découvert cette problématique **un peu tard** dans le processus de thèse
   - Ça explique pourquoi c'est un chapitre séparé plutôt qu'intégré dès le départ

**Ce qui t'a surpris dans les résultats :**

1. **Le post-processing ne résout PAS tout** :
   - Keyword perturbation réduit drastiquement les linkage attacks (19-63 pp)
   - Mais ça ne suffit pas pour éliminer complètement les risques

2. **Les attaques de discrimination restent très puissantes** :
   - Même après keyword perturbation : 57-95% TF-IDF, 79-99% semantic
   - Il n'y a **pas de signal clair** dans le post-processing pour contrecarrer cette attaque
   - C'est frustrant car tu ne vois pas comment mitiger efficacement

3. **Nuance importante : attaque théorique** :
   - La discrimination attack suppose un adversaire avec des connaissances spécifiques (peut réduire l'espace de recherche à 2 candidats)
   - C'est un scénario théorique mais qui reste **possible** dans la réalité

---

### Question 2 : DPO amplifie les risques de ré-identification

**Contexte :** Un résultat frappant : le reward-based training (DPO) amplifie massivement les risques comparé au simple SFT.

Sur AlpaCare :
- **DP-SFT** : 24.78% TF-IDF, 26.31% semantic (linkage attack)
- **DPO-1** : 77.88% TF-IDF, 81.99% semantic (linkage attack)

**Question :** Comment interprètes-tu ce résultat ? Pourquoi le DPO amplifie autant ? Aurais-tu pu l'anticiper ?

**Réponse :**

**Comment DPO amplifie les risques de ré-identification :**

1. **Risques non anticipés du DPO** :
   - Tu n'avais **pas pris en compte** que le DPO pouvait créer des vulnérabilités privacy
   - Le reward signal (même sous forme de logits/floats uniquement) peut **forcer le modèle** à tendre vers des patterns qui affaiblissent l'aspect privé

2. **Mécanisme de l'amplification** :
   - Le scorer compare synthetic vs real et retourne un score de similarité
   - Le DPO **optimise pour maximiser cette similarité**
   - Du coup, le modèle apprend à reproduire les **patterns patient-spécifiques** (même sans accès direct aux documents réels)
   - Ces patterns sont ceux qui permettent justement la ré-identification

3. **Impossible à anticiper sans expérimentation** :
   - Tu n'aurais **pas pu anticiper** ce problème théoriquement
   - C'est une **découverte empirique** venue des attaques privacy

4. **Mitigation potentielle : bruiter les floats** :
   - Une solution possible : ajouter du **bruit** aux scores (floats) retournés par le scorer privé
   - Ça empêcherait le modèle d'optimiser trop précisément vers les patterns réels
   - C'est une forme de **DP sur les scores** plutôt que sur le texte

---

### Question 3 : Keyword perturbation vs rephrasing - Pourquoi si efficace ?

**Contexte :** Keyword perturbation est dramatiquement plus efficace que le rephrasing standard.

Sur MIMIC-III 6% :
- **Rephrasing** : -4.73 pp (TF-IDF), -7.31 pp (semantic)
- **Keyword perturbation** : -59.04 pp (TF-IDF), -26.11 pp (semantic)

**Question :** Pourquoi la keyword perturbation marche tellement mieux ? Qu'est-ce que ça nous apprend sur la nature de la privacy leakage ?

**Réponse :**

**Pourquoi keyword perturbation >> rephrasing standard :**

1. **Approche localisée et ciblée** :
   - Le rephrasing change **tout le texte** de manière générique
   - La keyword perturbation cible **uniquement les keywords UMLS** (ceux extraits du patient)
   - C'est plus **précis** : on enlève ce qui permet vraiment la ré-identification

2. **Perte sémantique minimale** :
   - Le rephrasing peut **détruire de la sémantique utile** en changeant toute la formulation
   - La keyword perturbation **préserve** la structure narrative, le flow clinique, etc.
   - On ne touche qu'aux **mots-clés cruciaux** issus du patient

3. **Ce que ça nous apprend sur la privacy leakage** :
   - Les **keywords UMLS** (même "non-identifiants" individuellement) sont la source principale de ré-identification
   - C'est leur **combinaison/séquence** qui crée un fingerprint patient-specific
   - En remplaçant ces keywords par des synonymes, on casse ce fingerprint tout en gardant le sens clinique

4. **Pas de contradiction avec l'approche initiale** :
   - Les keywords UMLS sont bien **non-identifiants** (pas de noms, dates, lieux)
   - Mais leur **arrangement** crée un pattern unique au patient
   - D'où le besoin de **perturber** ces keywords pour casser le pattern

---

### Question 4 : Privacy-Utility Tradeoff - Différence MIMIC vs AlpaCare

**Contexte :** Le tradeoff est très différent selon le dataset :

**MIMIC-III** (ICD-9) : -59 pp privacy gain, mais -15 à -20 points F1 sur Top-50/Top-100 (coût significatif)
**AlpaCare** (conversational) : -63 pp privacy gain, seulement -1.3% preference (coût négligeable)

**Question :** Comment interprètes-tu cette différence ? Pourquoi MIMIC souffre plus ? Implications pour le déploiement ?

**Réponse :**

**Pourquoi la différence de tradeoff entre MIMIC et AlpaCare :**

1. **Modèles downstream plus petits sur MIMIC** :
   - Les modèles DeBERTa-base utilisés pour ICD-9 sont **plus petits** et **plus sensibles** à la perte d'information terminologique
   - Quand tu perturbes les keywords, ça retire des **signaux précis** dont ces petits modèles ont besoin

2. **Nature de la tâche** :
   - **MIMIC (ICD-9)** : classification médicale précise, nécessite des **termes médicaux exacts**
   - **AlpaCare (conversational)** : qualité conversationnelle, plus robuste aux synonymes
   - Le keyword perturbation est plus acceptable pour des tâches conversational que pour du coding médical

3. **Tradeoff volume vs perturbation** :
   - Sur les gros top (100/400), le tradeoff est **moins évident** : tu perds beaucoup d'utility
   - **Hypothèse** : avec **plus de volume** de données synthétiques, tu pourrais compenser la perte due à la perturbation
   - Il faudrait explorer : générer 10x ou 20x plus de données avec perturbation vs 4x sans perturbation

4. **Implication pour le déploiement** :
   - Pour des tâches **conversational/QA** : keyword perturbation est un no-brainer (gain privacy massif, coût utility faible)
   - Pour des tâches de **classification précise/coding** : il faut un **tradeoff explicite** volume vs perturbation

---

### Question 5 : Leçon générale du chapitre privacy

**Contexte :** Tu as fait une analyse rigoureuse des risques privacy, découvert que DPO amplifie les risques, proposé des mitigations, mais les discrimination attacks restent très efficaces.

**Question :** Quelle est la leçon générale que tu retires de tout ce chapitre ? Quelle promesse peux-tu (et ne peux-tu PAS) faire sur la privacy ?

**Réponse :**

**Leçon générale du chapitre privacy - Honnêteté sur les limites :**

1. **Il faut accepter le risque résiduel** :
   - Il n'existe PAS de solution parfaite (100% privacy + 100% utility)
   - Toute approche de génération synthétique comportera un **risque résiduel de ré-identification**
   - Il faut être **honnête** sur ces limites plutôt que de promettre une sécurité absolue

2. **Toutes les techniques nécessitent des compromis** :
   - Aucune technique dans la littérature n'est "safe" à 100%
   - Toutes ces techniques nécessitent des **compromis** et sont **adaptées ou non** selon les besoins du data provider
   - Il n'y a pas de solution universelle : chaque contexte requiert une évaluation spécifique

3. **Ce que tu PEUX garantir** :
   - **Pas d'identification directe** : les keywords UMLS ne contiennent pas de PII (noms, dates, lieux, identifiants directs)
   - Aucune donnée textuelle réelle ne traverse la frontière privé → public (seulement des scores numériques)

4. **Ce que tu NE PEUX PAS garantir** :
   - **Ré-identification = risque non nul** : les attaques de linkage et discrimination restent possibles
   - Le post-processing (keyword perturbation) **réduit** massivement le risque mais ne l'**élimine pas**
   - Les discrimination attacks restent très efficaces (57-99%) même après mitigation

5. **Approche adaptable selon le data provider** :
   - Chaque hôpital/institution doit **définir son niveau de risque acceptable**
   - Les mitigations sont **modulables** selon le contexte et les exigences privacy

**Conclusion honnête à un hôpital** : "Mon approche garantit l'absence d'identification directe, mais comporte un risque résiduel de ré-identification qui peut être significativement réduit (mais pas éliminé) via post-processing. Vous devez adapter le niveau de mitigation à votre contexte."

---

---

## CHAPITRE 5 : Knowledge Distillation with LLMs (Weak Supervision)

### Question 1 : Lien avec les chapitres précédents - Le fil rouge

**Contexte :** Chapitres 3-4 = génération de documents synthétiques. Chapitre 5 = distillation de connaissances depuis GPT-3.5 vers petits modèles pour NER.

**Question :** Quel est le lien entre ce chapitre 5 et les chapitres précédents ? Pourquoi ces deux chapitres coexistent dans la même thèse ?

**Réponse :**

**Le fil rouge : Pipeline entièrement synthétique (génération + annotation) :**

1. **Chapitre 3-4 : Génération de documents synthétiques**
   - Tu génères des documents cliniques synthétiques (via reward-based generation)
   - Avec analyse privacy pour garantir qu'ils sont safe à publier

2. **Chapitre 5 : Annotation synthétique (weak supervision)**
   - Tu utilises GPT-3.5 pour **annoter automatiquement** (NER) via distillation
   - Tu montres que ces annotations synthétiques permettent d'entraîner de petits modèles efficaces

3. **Vision finale : Pipeline entièrement automatisé**
   - **Documents synthétiques** (Chap 3) + **Annotations synthétiques** (Chap 5) = Dataset annoté sans intervention humaine massive
   - C'est la **partie automatisable** de la création de datasets médicaux
   - Vision à long terme : un jour, on pourra **faire les deux en même temps** (autre problématique de recherche)

4. **Pourquoi ces deux chapitres coexistent** :
   - Ensemble, ils prouvent qu'on peut **automatiser** la génération ET l'annotation
   - C'est complémentaire : pas seulement générer du texte, mais générer du texte **prêt à l'emploi** (avec labels)

---

### Question 2 : Hybrid supervision (dict + GPT) - Pourquoi mélanger marche mieux ?

**Contexte :** Mélanger les annotations dictionnaire (dict) + GPT-3.5 donne de meilleurs résultats que d'utiliser une seule source. Ratio optimal $r_{mix} \in [0.4, 0.6]$ pour la plupart des langues. Basque exception : $r_{mix} = 1$ (GPT seul) meilleur.

**Question :** Comment interprètes-tu ce résultat ? Pourquoi mélanger deux sources imparfaites donne de meilleurs résultats ?

**Réponse :**

**Pourquoi l'hybride (dict + GPT) marche mieux :**

1. **Complémentarité des deux sources** :
   - **Dict** : capture les termes médicaux **standardisés** présents dans le lexique (UMLS)
   - **GPT** : plus **flexible**, peut capter des expressions rares, multi-word entities, dépendantes du contexte
   - Le mélange donne un **signal plus riche** que chaque source seule

2. **Réduction du bruit par combinaison** :
   - Les erreurs de dict et GPT sont **différentes**
   - En combinant, on obtient un signal plus propre

3. **Basque : exception due aux faibles annotations** :
   - Le dict basque a **très peu de termes** (seulement 63 tokens I_clin vs 482 pour GPT)
   - Donc GPT seul est forcément meilleur car dict n'apporte presque rien
   - **Généralisation** : pour les **langues low-resource** avec très faibles annotations/dict, privilégier GPT seul

4. **Implication pratique** :
   - **Langues bien dotées** (dict riche) : combiner dict + GPT ($r_{mix} \in [0.4, 0.6]$)
   - **Langues low-resource** (dict pauvre) : privilégier GPT ($r_{mix} = 1$)

---

### Question 3 : Distillation vs direct GPT inference

**Contexte :** La distillation (entraîner un petit modèle sur annotations GPT) donne parfois de meilleurs résultats que GPT-3.5 direct.

Résultats :
- **Basque** : GPT direct = 0.63, Distillé = 0.72 (+0.09)
- **Français** : GPT direct = 0.66, Distillé = 0.72 (+0.06)
- **Italien** : GPT direct = 0.63, Distillé = 0.75 (+0.12)
- **Mais Espagnol et Anglais** : GPT direct meilleur que distillé

**Question :** Comment interprètes-tu ces résultats ? Pourquoi le petit modèle peut être meilleur que le gros ?

**Réponse :**

**Pourquoi la distillation surpasse GPT direct (Basque, Français, Italien) :**

1. **Moins de volume d'annotations + dict plus pauvre** :
   - Pour ces langues, le dict est **moins riche** qu'en anglais
   - Le volume d'annotations gold est **limité** (petit test set E3C)
   - La distillation permet au petit modèle de **généraliser mieux** que GPT en few-shot direct

**Pourquoi Espagnol et Anglais montrent le pattern inverse :**

3. **Espagnol : source de données différente (SPACCC)** :
   - Dataset SPACCC a une **distribution d'entités cliniques différente** des autres langues (Pan African Journal, Pubmed)
   - Preprocessing additionnel (removal de phrases, capitalisation) **renforce ces différences**
   - Ça crée un **mismatch** entre les annotations GPT et la distribution réelle

4. **Anglais : dict de très bonne qualité** :
   - Les ressources UMLS pour l'anglais sont **beaucoup plus riches**
   - Le dict capture déjà très bien les entités, GPT n'apporte pas beaucoup plus

---

### Question 4 : Leçon générale du chapitre weak supervision

**Contexte :** Tu as montré que la distillation LLM→petit modèle fonctionne bien, l'hybride (dict + GPT) est souvent meilleur, résultats varient selon langues/ressources.

**Question :** Quelle est la leçon générale ? Cas d'usage ? Limites ? Améliorations futures ?

**Réponse :**

**Leçon générale du chapitre weak supervision :**

**Cas d'usage recommandés :**

1. **Approche pour draft / pré-annotation** :
   - La weak supervision (dict + LLM) est idéale pour **créer un premier jet** d'annotations
   - Les experts peuvent ensuite **valider/corriger** ces pré-annotations (beaucoup plus rapide que d'annoter from scratch)
   - Ça réduit drastiquement le coût et le temps d'annotation humaine

2. **Langues low-resource ou domaines avec peu de dict** :
   - Quand le dict est pauvre (comme Basque), privilégier LLM seul
   - Quand le dict est riche, combiner dict + LLM pour avoir le meilleur des deux

**Améliorations futures :**

3. **Ensembling multi-LLM** :
   - Au lieu d'utiliser **seulement GPT-3.5**, utiliser **plusieurs providers** (GPT, Claude, Gemini, etc.)
   - Faire de l'**ensembling** des annotations de différents LLMs
   - Ça donnerait des annotations **plus robustes** et **réduirait les biais** spécifiques à chaque modèle
   - C'est mentionné dans la section "Future work" du chapitre

**Limites :**
- Petit test set E3C (généralisation limitée)
- Biais introduits par les guidelines E3C (orientées vers UMLS)
- Nécessité de validation humaine pour garantir la qualité

---
