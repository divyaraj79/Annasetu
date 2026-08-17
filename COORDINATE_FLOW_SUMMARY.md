# AnnaSetu Coordinate Flow — Executive Summary
**Date**: 2026-08-17 | **Branch**: speed-up | **Status**: Trace Complete

---

## Quick Answers to 14 Questions

| # | Question | Answer |
|---|----------|--------|
| 1 | Where obtained? | Browser Geolocation API OR manual number input (Frontend only) |
| 2 | Source type? | Device location (W3C standard) + user input (NO geocoding) |
| 3 | Which frontend request? | `POST /auth/register` (registration), `POST /donations/` (donations) |
| 4 | Which backend schema? | `RegistrationRequest`, `RestaurantCreate`, `NGOCreate`, `DonationCreate` |
| 5 | NGO persistence? | `RegistrationService` → `NGOService.create()` (coordinates passed through, not geocoded) |
| 6 | Restaurant persistence? | `RegistrationService` → `RestaurantService.create()` (coordinates passed through, not geocoded) |
| 7 | Backend geocoding API? | **NONE EXISTS** — Only TODO comments in 3 service files |
| 8 | Frontend geocoding API? | **NONE EXISTS** — Only browser Geolocation API used |
| 9 | Where NULL? | When not provided by frontend OR in email automation (extraction prompts don't include lat/long) |
| 10 | Where 0 or 0,0? | **NEVER** — No hardcoded defaults found |
| 11 | MatchService._distance_km source? | `Donation.latitude/longitude` + `NGO.latitude/longitude` from database models |
| 12 | Matching triggers? | Website donation: `MatchService.create_nearby_matches()` | Email donation: `MatchingService.create_matches()` (DIFFERENT) |
| 13 | Duplicate matching? | **YES** — 2 implementations with different logic (distance vs urgency scoring) |
| 14 | Min files to modify? | **10-15 files** for complete geocoding solution |

---

## Critical Findings

### 🔴 BLOCKER: Coordinates Not Persisted
- Frontend collects coordinates → Backend ignores them → Database stores NULL
- Three service files have TODO comments for geocoding but zero implementation

### 🔴 BLOCKER: Two Separate Matching Systems
| System | Used By | Distance? | When Coordinates NULL |
|--------|---------|-----------|----------------------|
| **MatchService.create_nearby_matches()** | Website donations | ✓ Yes (Haversine) | Skip silently |
| **MatchingService.create_matches()** → RankingService | Email donations + Email needs | ✗ No (TODO) | Include all |

### 🟡 ISSUE: Automation Never Extracts Coordinates
- Email donations/needs extracted via Groq AI
- Extraction prompts DON'T include latitude/longitude fields
- Result: All email-based records have NULL coordinates by design

### 🟢 GOOD: Haversine Distance Calculation
- `MatchService._distance_km()` implementation is correct
- Uses proper geographic distance formula
- Can be reused once coordinates are available

---

## Data Flow Diagram

```
REGISTRATION (Website)
├─ Frontend: Register.jsx
│  ├─ Input: address (text) + latitude/longitude (geolocation OR manual)
│  └─ Send: POST /auth/register
├─ Backend: RegistrationService
│  ├─ Receive: RegistrationRequest schema
│  ├─ Route: NGOService.create() or RestaurantService.create()
│  └─ TODO: Geocoding not implemented
└─ Database: NGO/Restaurant (coordinates stored as-is or NULL)

DONATION (Website)
├─ Frontend: Dashboard.jsx
│  ├─ Input: pickup_address + latitude/longitude (geolocation OR manual)
│  └─ Send: POST /donations/
├─ Backend: DonationService.create()
│  ├─ Receive: DonationCreate schema
│  ├─ TODO: Geocoding not implemented
│  └─ Trigger: MatchService.create_nearby_matches()
│     └─ Use: Haversine distance (if coordinates available)
└─ Database: Donation (coordinates stored as-is or NULL)

EMAIL DONATION (Automation)
├─ Email: Restaurant sends food donation email
├─ Scheduler: Fetches unread email
├─ Groq AI: Extraction prompt (lat/long NOT in schema)
├─ Backend: AutomationService.create_donation()
│  └─ Trigger: MatchingService.create_matches()
│     └─ Use: RankingService (no distance, only urgency)
└─ Database: Donation (coordinates ALWAYS NULL)

EMAIL NEED (Automation)
├─ Email: NGO sends food need email
├─ Groq AI: Extraction prompt (lat/long NOT in schema)
├─ Backend: AutomationService.create_need()
│  └─ No matching triggered
└─ Database: Need (coordinates ALWAYS NULL)
```

---

## Coordinate Nullification Points

```
Frontend Input
    ↓
 ┌─ Provided (geolocation + manual)
 │  ├─ Website: Sent as-is to backend
 │  └─ Email: Never extracted (prompt doesn't include)
 │
 └─ Not Provided (user skips geolocation, enters empty)
    ├─ Website: Sent as empty/null to backend
    └─ Email: Not in extraction prompt anyway → NULL

Backend Persistence
    ├─ Website: Coordinates passed to service
    │  ├─ TODO: Geocoding not implemented
    │  └─ Store: NULL if frontend didn't provide
    │
    └─ Email: Coordinates never in extraction data
       └─ Store: NULL always

Database
    └─ NGO/Restaurant/Donation tables: latitude/longitude are nullable columns
       ├─ No server_default value
       └─ No constraint preventing NULL
```

---

## Files Modified by Recent Merge (Aug 16, 2026)

**Merged from**: `mahendra-backend` → `speed-up`

**Coordinate-Related Changes**:
- ✓ [Backend/app/schemas/donation.py](Backend/app/schemas/donation.py) — Added lat/long fields
- ✓ [Backend/app/schemas/ngo.py](Backend/app/schemas/ngo.py) — Added lat/long fields
- ✓ [Backend/app/schemas/restaurant.py](Backend/app/schemas/restaurant.py) — Added lat/long fields
- ✓ [Backend/app/services/registration_service.py](Backend/app/services/registration_service.py) — Passes coordinates through
- ✓ [Backend/app/services/donation_service.py](Backend/app/services/donation_service.py) — Geocoding TODO added
- ✓ [Backend/app/services/match_service.py](Backend/app/services/match_service.py) — Complete rewrite with Haversine

**What Was Brought In**:
- ✓ Complete matching logic with distance calculations
- ✗ Geocoding implementation (NOT included, only TODOs)

**What Was NOT Brought In**:
- ✗ Backend geocoding service
- ✗ Frontend address-to-coordinate conversion
- ✗ API endpoint for reverse geocoding

---

## Minimum Files for Implementation

### Scenario A: Backend Geocoding (Aligns with ADR-002 Design)
**Files**: 10
- 3 backend services (restaurant, ngo, donation)
- 4 schemas (auth, restaurant, ngo, donation)
- 2 frontend pages (register, dashboard)
- 1 requirements file

### Scenario B: Fallback Urgency-Based Matching (Quick Unblock)
**Files**: 3
- RankingService: Add distance scoring as option
- MatchingService: Accept optional distance
- Coordinate validation logic

### Scenario C: Hybrid (Distance + Urgency)
**Files**: 5
- Files from Scenario B +
- Match model update (add match_type)
- API response schema update

---

## Recommended Implementation Path

### Phase 1: Immediate (Unblock Matching)
**Goal**: Get matching working without geocoding

1. Modify [Backend/app/services/ranking_service.py](Backend/app/services/ranking_service.py)
   - Implement distance scoring (use Haversine from match_service.py)
   - Fallback to urgency-only when coordinates NULL

2. Update [Backend/app/services/matching_service.py](Backend/app/services/matching_service.py)
   - Call ranking_service with distance when available

3. Test with sample data

**Timeline**: 1-2 hours  
**Risk**: Low (additive only)

### Phase 2: Backend Geocoding (Proper Solution)
**Goal**: Implement ADR-002 design

1. Install `geopy` in [Backend/requirements.txt](Backend/requirements.txt)

2. Create geocoding service (new file: `geocoding_service.py`)

3. Update three service files with geocoding calls

4. Remove lat/long from four schemas

5. Update frontend pages (remove coordinate inputs)

**Timeline**: 4-8 hours  
**Risk**: Medium (breaking API changes)

### Phase 3: Unify Matching (Consistency)
**Goal**: Single matching implementation

1. Deprecate `MatchService.create_nearby_matches()`

2. Move logic to `MatchingService` with optional distance

3. Remove RankingService or consolidate

**Timeline**: 2-4 hours  
**Risk**: Medium (refactoring)

---

## Next Steps (Recommended)

1. **Decision**: Choose implementation scenario (A, B, or C)

2. **Verify**: Run tests against current system to document baseline

3. **Implement Phase 1**: Get matching unblocked immediately (Scenario B)

4. **Plan Phase 2**: Schedule proper geocoding implementation

5. **Document**: Update ADR-002 to reflect actual vs intended behavior

---

## Key Observations

- **Architecture vs Reality Mismatch**: ADR-002 says "Backend geocodes", but frontend is collecting coordinates while backend is ignoring them
- **Incomplete Merge**: Matching infrastructure merged without prerequisite geocoding implementation
- **Two Code Paths**: Website and automation have divergent matching logic (technical debt)
- **Email Blind Spot**: Email automation never extracts coordinates, so email-based records can never match by distance

---

**Full detailed trace available in**: [COORDINATE_FLOW_TRACE.md](./COORDINATE_FLOW_TRACE.md)

**Analysis frozen at**: 2026-08-17 | No code modifications made
