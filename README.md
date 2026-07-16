# FitGuide Recommender

FitGuide is my individual university prototype that recommends a short general-wellness exercise routine from a person's goal, fitness level, available equipment, time preference and self-declared movement restrictions. It uses a transparent content-based pipeline: hard compatibility filtering, shared feature vectors, cosine similarity, documented score adjustments, movement-pattern diversification and routine-role assembly.

FitGuide is not a medical device, diagnostic service, physiotherapy tool or substitute for a qualified professional. Anyone with an injury, chronic condition, pregnancy, cardiovascular concern, severe pain or uncertainty should seek appropriate professional advice before exercising. A compatibility score is a relative catalogue-ranking value, not a probability of safety or benefit.

## Implemented features

The backend provides an 80-record synthetic exercise catalogue, typed FastAPI endpoints, restriction and compatibility filters, deterministic scoring, role-based routines, recommendation explanations and temporary anonymous feedback. The React and TypeScript frontend provides a landing disclaimer, accessible questionnaire, loading, results, empty and error states, preference editing, feedback controls, an About page and responsive desktop and mobile layouts.

The catalogue is synthetic and not clinically validated. It contains no patient record or real user history. Feedback remains in temporary server memory and does not retrain the recommender.

## Technology stack

The frontend uses React, TypeScript, Vite, responsive CSS, Vitest and React Testing Library. The backend uses Python, FastAPI, Pydantic, pandas, NumPy and scikit-learn. Data is stored in a local CSV. No authentication, cloud platform, external health API or persistent personal database is required.

## Repository structure

`backend` contains the API, dataset, recommendation engine and backend tests. `frontend` contains the React application and interaction tests. `evaluation` contains the frozen profiles, predefined relevance rules, raw result CSV, JSON summary and written report.

## Backend setup

From the `backend` directory:

```text
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider
PYTHONPATH=. .venv/bin/python -m uvicorn app.main:app --reload
```

The local API runs at `http://127.0.0.1:8000`. Interactive OpenAPI documentation is available at `http://127.0.0.1:8000/docs`.

## Frontend setup

From the `frontend` directory:

```text
pnpm install
pnpm test
pnpm run build
pnpm run dev --host 127.0.0.1
```

The development interface runs at `http://127.0.0.1:5173`. Start the backend before using the live questionnaire.

## API summary

`GET /health` reports status and catalogue size. `GET /metadata` supplies questionnaire vocabularies. `GET /exercises` returns the catalogue with optional category, difficulty and location filters. `POST /recommendations` validates a profile and returns a routine. `GET /recommendations/example` returns a demonstration. `POST /feedback` accepts like, dislike or unsuitable feedback for a valid exercise ID.

## Recommendation method

Movement conflicts, unavailable equipment, incompatible location, excessive difficulty, excessive item duration and exact exercise exclusions are removed before similarity calculation. The final score uses 50% cosine similarity and transparent adjustments for goal, category, body area, intensity, level, duration, location and equipment. A separate routine assembler attempts preparation, main activity, support and recovery roles while limiting repeated categories and movement patterns. Hard filters are never relaxed to fill the list.

## Actual testing

The final backend suite completed 31 tests successfully. It covers dataset integrity, every required movement restriction, equipment, location, level, duration, exact exclusions, ordering, determinism, routine diversity, explanations, empty results, validation and endpoints. The frontend suite completed eight interaction tests successfully, and the TypeScript production build completed. Detailed outputs are stored in `docs/testing.md` and `docs/frontend-testing.md`.

## Known limitations

Exercise labels, movement flags and weights are manually designed. The catalogue is small, synthetic and not professionally validated. The system cannot observe exercise technique, interpret pain, learn from long-term behaviour or assess individual biomechanics. Precision is partly circular because relevance conditions use some of the same catalogue attributes as ranking. Coverage depends on the eight chosen profiles, and local response time cannot predict deployment performance.
