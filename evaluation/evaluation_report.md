# FitGuide Offline Evaluation Report

## Method

Eight profiles and their relevance conditions were fixed before this evaluation. Seven profiles represent different goals, settings, equipment and restrictions. P08 is deliberately over-constrained and is evaluated for correct empty-result handling rather than Precision@5. All relevance judgements are derived from the synthetic catalogue fields, so the evaluation measures internal prototype behaviour rather than clinical suitability or user benefit.

Constraint satisfaction checks every returned item against movement restrictions, low-impact need, equipment, location, fitness level, item duration and explicit name exclusions. Precision@5 uses each profile's predefined relevance predicate. Coverage is the proportion of the 80-item catalogue appearing at least once. Category, body-area, movement-pattern and routine-role diversity divide distinct values by list length, with body diversity capped at one. Explanation consistency recomputes matched features and verifies the clauses used in the displayed explanation.

Timing used FastAPI TestClient. Each profile received one warm-up request followed by 50 measured requests, giving 400 measurements. This includes validation, filtering, vector construction, ranking, diversification, explanation generation and in-process HTTP handling. It excludes a real network, browser rendering, concurrency, server start-up and deployment overhead.

## Results

| Profile | Returned | Precision@5 | Constraint satisfaction | Goal relevance | Mean response (ms) |
|---|---:|---:|---:|---:|---:|
| P01 | 5 | 100.00% | 100.00% | 100.00% | 5.060 |
| P02 | 5 | 60.00% | 100.00% | 60.00% | 6.377 |
| P03 | 5 | 40.00% | 100.00% | 40.00% | 4.217 |
| P04 | 5 | 80.00% | 100.00% | 100.00% | 5.064 |
| P05 | 5 | 40.00% | 100.00% | 100.00% | 5.261 |
| P06 | 5 | 80.00% | 100.00% | 80.00% | 4.759 |
| P07 | 5 | 60.00% | 100.00% | 60.00% | 6.229 |
| P08 | 0 | Not applicable | 100.00% | Not applicable | 2.201 |

Across 35 returned recommendations, hard-constraint satisfaction was 100.00%. Micro Precision@5 was 0.6571 and macro Precision@5 across the seven non-empty evaluation profiles was 0.6571. Goal relevance was 77.14%. The routines surfaced 27 of 80 catalogue exercises, corresponding to 33.75% coverage.

Mean category diversity was 0.8286, mean body-area diversity was 1.0000, mean movement-pattern diversity was 1.0000, and mean routine-role diversity was 0.8857. Explanation consistency was 100.00%. All 8 profiles produced identical IDs, scores and roles in repeated direct runs.

Across 400 timed in-process requests, mean response time was 4.896 ms, median was 5.037 ms, minimum was 1.948 ms and maximum was 30.277 ms. The measured environment was macOS-26.5.1-arm64-arm-64bit with Python 3.12.13.

## Interpretation and limitations

Constraint satisfaction shows that the implemented rule set behaved consistently for these profiles. It must not be described as clinical safety validation because the rules and catalogue labels are simplified and synthetic. Precision@5 measures agreement with manually defined field predicates that overlap with the ranking features, which makes the result partly circular. Coverage depends strongly on the small profile set, while the diversity ratios represent catalogue variation rather than perceived variety.

No real user judged usefulness, novelty, serendipity, trust or satisfaction. Recall, MRR and NDCG are not reported because there is no independent interaction history, complete relevance set or graded ground truth. Timing is a local in-process prototype measure and cannot predict deployed performance. These results support claims about reproducibility and encoded behaviour only.
