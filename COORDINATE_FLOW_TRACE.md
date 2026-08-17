# AnnaSetu Coordinate Flow — Complete Trace Report
**Date**: 2026-08-17  
**Branch**: speed-up  
**Status**: READ-ONLY ANALYSIS (No modifications made)

---

## 1. WHERE LATITUDE AND LONGITUDE ARE OBTAINED IN FRONTEND

### Registration (NGO/Restaurant)
**File**: [Frontend/src/pages/Register.jsx](Frontend/src/pages/Register.jsx)

**Sources**:
- **Browser Geolocation API** (lines 28-34):
  ```javascript
  navigator.geolocation.getCurrentPosition(
    ({ coords }) => setFormData({ 
      ...formData, 
      latitude: coords.latitude, 
      longitude: coords.longitude 
    })
  )
  ```
- **Manual Input** (lines 166-167):
  ```javascript
  <input type="number" step="any" placeholder="Latitude" required />
  <input type="number" step="any" placeholder="Longitude" required />
  ```

**Button**: "Use my current location" (line 169)

**Initial State**: Both default to empty string (line 23-24):
```javascript
const [formData,setFormData] = useState({
  ...
  latitude:"",
  longitude:""
});
```

### Donation Creation (Website)
**File**: [Frontend/src/pages/Dashboard.jsx](Frontend/src/pages/Dashboard.jsx)

**Sources**:
- **Browser Geolocation API** (lines 122-126):
  ```javascript
  navigator.geolocation.getCurrentPosition(
    ({ coords }) => setDonation({ 
      ...donation, 
      latitude: coords.latitude, 
      longitude: coords.longitude 
    })
  )
  ```
- **Manual Input** (lines 96-97 in form):
  ```javascript
  latitude: Number(donation.latitude),
  longitude: Number(donation.longitude),
  ```

**Button**: "Use current pickup location" (line 169)

**Initial State** (lines 13-15):
```javascript
const initialDonation = {
  ...
  latitude: "", longitude: "",
};
```

### Automation/Email Flow
**No coordinate collection** — Extraction prompts don't include latitude/longitude fields.

---

## 2. SOURCE OF COORDINATES

### Frontend
✓ Browser Geolocation API (W3C standard)  
✓ Manual user input (required field)  
✗ No frontend geocoding service found  
✗ No hardcoded defaults of 0 or 0,0

### Automation/Email
✗ No extraction from email  
✗ Not in prompts  
✗ Coordinates never collected for email-based donations/needs

---

## 3. WHICH FRONTEND API REQUEST SENDS THEM TO BACKEND

### Registration Request
**File**: [Frontend/src/pages/Register.jsx](Frontend/src/pages/Register.jsx#L50)

```javascript
await api.post("/auth/register", { 
  ...formData, 
  role, 
  latitude: Number(formData.latitude),     // ← SENT
  longitude: Number(formData.longitude)    // ← SENT
});
```

**Endpoint**: `POST /auth/register`  
**Transport**: axios via [Frontend/src/services/api.js](Frontend/src/services/api.js)

### Donation Creation Request
**File**: [Frontend/src/pages/Dashboard.jsx](Frontend/src/pages/Dashboard.jsx#L96-L97)

```javascript
const payload = {
  ...donation,
  restaurant_id: organization.id,
  quantity: Number(donation.quantity),
  latitude: Number(donation.latitude),     // ← SENT
  longitude: Number(donation.longitude),   // ← SENT
  ...
};
runAction(() => api.post("/donations/", payload), ...)
```

**Endpoint**: `POST /donations/`

---

## 4. WHICH BACKEND SCHEMA RECEIVES THEM

### Registration Schema
**File**: [Backend/app/schemas/auth.py](Backend/app/schemas/auth.py#L14-L15)

```python
class RegistrationRequest(BaseModel):
    ...
    latitude: float | None = None      # ← OPTIONAL, nullable
    longitude: float | None = None     # ← OPTIONAL, nullable
```

### NGO Schema
**File**: [Backend/app/schemas/ngo.py](Backend/app/schemas/ngo.py#L16-L17)

```python
class NGOCreate(BaseModel):
    user_id: UUID
    ngo_name: str
    address: str
    latitude: float | None = None      # ← OPTIONAL
    longitude: float | None = None     # ← OPTIONAL
```

### Restaurant Schema
**File**: [Backend/app/schemas/restaurant.py](Backend/app/schemas/restaurant.py#L15-L16)

```python
class RestaurantCreate(BaseModel):
    user_id: UUID
    restaurant_name: str
    address: str
    latitude: float | None = None      # ← OPTIONAL
    longitude: float | None = None     # ← OPTIONAL
```

### Donation Schema
**File**: [Backend/app/schemas/donation.py](Backend/app/schemas/donation.py#L19-L20)

```python
class DonationCreate(BaseModel):
    ...
    latitude: float | None = None      # ← OPTIONAL
    longitude: float | None = None     # ← OPTIONAL
```

**Key Point**: All schemas make coordinates optional with `= None` default.

---

## 5. WHICH BACKEND SERVICE PERSISTS NGO COORDINATES

### NGO Persistence Flow

**Router**: [Backend/app/routers/auth_router.py](Backend/app/routers/auth_router.py#L26-45)
```python
@router.post("/register", ...)
def register(registration_data: RegistrationRequest, db: Session = Depends(get_db)):
    service = RegistrationService(db)
    return service.register(registration_data)  # ← Passes coordinates
```

**Service**: [Backend/app/services/registration_service.py](Backend/app/services/registration_service.py#L56-68)
```python
if registration_data.role == UserRole.NGO:
    ngo_service.create(
        NGOCreate(
            user_id=user.id,
            ngo_name=registration_data.organization_name,
            address=registration_data.address,
            latitude=registration_data.latitude,         # ← PASSED THROUGH
            longitude=registration_data.longitude,       # ← PASSED THROUGH
        )
    )
```

**NGO Service**: [Backend/app/services/ngo_service.py](Backend/app/services/ngo_service.py#L31-49)
```python
ngo = NGO(
    **ngo_data.model_dump(),      # ← Contains lat/long if provided
    verification_status=VerificationStatus.PENDING
)

# TODO:
# Geocode the address here and automatically populate
# latitude and longitude before saving.

self.db.add(ngo)
self.db.flush()
self.db.refresh(ngo)
```

**Persistence Point**: Coordinates saved as-is (NULL if not provided)

---

## 6. WHICH BACKEND SERVICE PERSISTS RESTAURANT COORDINATES

**Same flow as NGO** (parallel path):

**Router**: [Backend/app/routers/auth_router.py](Backend/app/routers/auth_router.py#L26-45)

**Service**: [Backend/app/services/registration_service.py](Backend/app/services/registration_service.py#L48-58)
```python
if registration_data.role == UserRole.RESTAURANT:
    restaurant_service.create(
        RestaurantCreate(
            user_id=user.id,
            restaurant_name=registration_data.organization_name,
            address=registration_data.address,
            latitude=registration_data.latitude,
            longitude=registration_data.longitude,
        )
    )
```

**Restaurant Service**: [Backend/app/services/restaurant_service.py](Backend/app/services/restaurant_service.py#L34-52)
```python
restaurant = Restaurant(
    **restaurant_data.model_dump(),
    verification_status=VerificationStatus.PENDING
)

# TODO:
# Geocode the address here and automatically populate
# latitude and longitude before saving.

self.db.add(restaurant)
```

---

## 7. DOES BACKEND GEOCODING API/SERVICE EXIST?

### Backend Geocoding Status

**Search Results**:
✗ No `geopy` library in [requirements.txt](Backend/requirements.txt)  
✗ No Google Maps API integration  
✗ No Nominatim/OpenStreetMap API calls  
✗ No address parsing library  
✗ No custom geocoding service

**TODO Comments Found**:

1. [restaurant_service.py](Backend/app/services/restaurant_service.py#L50-L52):
   ```python
   # TODO:
   # Geocode the address here and automatically populate
   # latitude and longitude before saving.
   ```

2. [ngo_service.py](Backend/app/services/ngo_service.py#L47-L49):
   ```python
   # TODO:
   # Geocode the address here and automatically populate
   # latitude and longitude before saving.
   ```

3. [donation_service.py](Backend/app/services/donation_service.py#L77-L78):
   ```python
   # TODO:
   # Geocode pickup_address and automatically
   # populate latitude and longitude.
   ```

4. [ranking_service.py](Backend/app/services/ranking_service.py#L106-L109):
   ```python
   # TODO:
   # Add distance scoring.
   ```

**Conclusion**: Geocoding is PLANNED but UNIMPLEMENTED. Zero actual geocoding logic exists.

---

## 8. DOES FRONTEND GEOCODING API/SERVICE EXIST?

### Frontend Geocoding Status

✓ Browser Geolocation API used (native, not external service)  
✗ No geocoding service (no address → coordinates conversion)  
✗ No map component for address lookup  
✗ No integration with Google Maps, Mapbox, or similar  
✗ No frontend address-to-coordinate conversion

**Files Checked**:
- [Frontend/src/services/api.js](Frontend/src/services/api.js) — Just axios wrapper
- [Frontend/src/pages/Register.jsx](Frontend/src/pages/Register.jsx) — Manual input or device location only
- [Frontend/src/pages/Dashboard.jsx](Frontend/src/pages/Dashboard.jsx) — Manual input or device location only

**Conclusion**: Frontend has NO geocoding. Users must manually enter coordinates or grant browser geolocation permission.

---

## 9. WHERE LATITUDE/LONGITUDE CAN BECOME NULL

### Path 1: Frontend Registration
- User skips browser location → Coordinates remain empty string "" 
- Frontend converts "" to number → `Number("")` = 0, but schema validation should reject
- Actually: Frontend sends empty string directly if not filled
- Backend receives None/null from optional field

### Path 2: Automation/Email
- Extraction prompt doesn't include lat/long fields
- AutomationService.create_donation() creates DonationCreate without coordinates
- Result: Coordinates NOT in payload → **NULL in database**

**File**: [Backend/app/automation/prompts/groq_prompts.py](Backend/app/automation/prompts/groq_prompts.py#L1-L70)
```python
DONATION_EXTRACTION_PROMPT = """
Extract structured donation information from a restaurant email.
Schema:
{
    "title": "",
    "food_category": "",
    "is_vegetarian": true,
    "cooked_at": "",
    "expiry_time": "",
    "pickup_address": "",
    "special_notes": "",
    "items": [...]
}
"""
# ← NO latitude/longitude in schema
```

**File**: [Backend/app/automation/prompts/groq_prompts.py](Backend/app/automation/prompts/groq_prompts.py#L171-L220)
```python
NEED_EXTRACTION_PROMPT = """
Extract structured NGO food need information.
Schema:
{
    "preferred_category": "",
    "vegetarian_only": true,
    "quantity_required": 0,
    "quantity_unit": "",
    "urgency": ""
}
"""
# ← NO latitude/longitude in schema
```

### Path 3: Website Donation Without Coordinates
- User doesn't provide coordinates and geolocation fails
- Frontend sends empty string or 0
- Backend receives None from schema validation
- Result: **NULL in database**

### NULL Nullification Points
1. **RegistrationService.register()** → NGOService/RestaurantService pass-through
2. **DonationService.create()** → Optional schema field not provided
3. **AutomationService.create_donation()** → Extraction prompt doesn't include lat/long
4. **AutomationService.create_need()** → Extraction prompt doesn't include lat/long

---

## 10. WHERE LATITUDE/LONGITUDE CAN BECOME 0 OR 0,0

### Search Results
✗ No hardcoded 0 values found in code  
✗ No database default value of 0  
✗ No service logic that sets coordinates to 0  
✗ No migration that defaults to 0  

### Frontend
- Initial state is `""` (empty string), not 0
- Browser Geolocation API returns valid lat/long or error (not 0)
- Manual input requires number type

### Backend
- Schemas accept `float | None`, not default to 0
- Models define `Column(Float)` with no server_default

**Conclusion**: Coordinates ONLY become NULL, never 0. Frontend and backend don't set default 0,0 values.

---

## 11. WHERE MATCHSERVICE._DISTANCE_KM() GETS ITS COORDINATES

### Website Flow

**File**: [Backend/app/services/donation_service.py](Backend/app/services/donation_service.py#L77-L84)
```python
donation = Donation(
    **donation_data.model_dump(),
    status=DonationStatus.CREATED,
)

# TODO: Geocode pickup_address...

self.db.add(donation)
self.db.flush()

matches = MatchService(self.db).create_nearby_matches(donation)
```

**MatchService.create_nearby_matches()**: [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L101-L145)

```python
def create_nearby_matches(self, donation: Donation) -> list[Match]:
    needs = self.db.query(Need).filter(...).all()
    
    for need in needs:
        ngo = need.ngo
        
        distance_km = self._distance_km(donation, ngo)  # ← CALLED HERE
        if distance_km is None:
            continue  # ← SKIP if NULL
        
        match = Match(
            donation_id=donation.id,
            ngo_id=ngo.id,
            distance_km=distance_km,  # ← STORED
            ...
        )
```

**MatchService._distance_km()**: [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L152-L165)

```python
@staticmethod
def _distance_km(donation: Donation, ngo: NGO) -> float | None:
    coordinates = (
        donation.latitude,        # ← From Donation model (could be NULL)
        donation.longitude,       # ← From Donation model (could be NULL)
        ngo.latitude,             # ← From NGO model (could be NULL)
        ngo.longitude,            # ← From NGO model (could be NULL)
    )
    if any(value is None for value in coordinates):
        return None  # ← Returns None if ANY coordinate is NULL
    
    # Haversine formula
    latitude_1, longitude_1, latitude_2, longitude_2 = map(radians, coordinates)
    ...
    return round(6371 * 2 * asin(sqrt(haversine)), 2)
```

**Data Source**: 
- `donation.latitude` → From `Donation` model → From `DonationCreate` schema → From frontend OR automation (NULL if not provided)
- `ngo.latitude` → From `NGO` model → From `NGOCreate` schema → From registration frontend (NULL if not provided)

**Critical Issue**: All four coordinates must be non-NULL for distance calculation. If ANY is NULL, matching is skipped or fails.

---

## 12. MATCHING TRIGGER POINTS

### Website-Created Donations

**Flow**: Router → Service → Matching

**File**: [Backend/app/routers/donation_router.py](Backend/app/routers/donation_router.py#L17-61)
```python
@router.post("/", response_model=DonationResponse, ...)
def create_donation(
    donation: DonationCreate,
    db: Session = Depends(get_db),
    ...
):
    service = DonationService(db)
    donation = service.create(donation)
    db.commit()
    db.refresh(donation)
    return donation
```

**Service**: [Backend/app/services/donation_service.py](Backend/app/services/donation_service.py#L41-85)
```python
def create(self, donation_data: DonationCreate) -> Donation:
    ...
    donation = Donation(...)
    self.db.add(donation)
    self.db.flush()
    
    matches = MatchService(self.db).create_nearby_matches(donation)  # ← TRIGGERS HERE
    if matches:
        donation.status = DonationStatus.MATCHING
    
    self.db.refresh(donation)
    return donation
```

**Matching Service**: [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L101-L145)
- Uses `_distance_km()` to filter NGOs within range
- Silently skips NGOs without coordinates

### Website-Created Needs

✗ **NO AUTOMATIC MATCHING** — Needs don't trigger matching when created.

**File**: [Backend/app/routers/need_router.py](Backend/app/routers/need_router.py#L17-65)
```python
@router.post("/", response_model=NeedResponse, ...)
def create_need(need: NeedCreate, db: Session = Depends(get_db), ...):
    service = NeedService(db)
    need = service.create(need)
    db.commit()
    db.refresh(need)
    return need  # ← No matching triggered
```

### Email-Created Donations

**Flow**: Scheduler → Executor → AutomationService → Matching

**File**: [Backend/app/automation/scheduler.py](Backend/app/automation/scheduler.py#L113-142)
```python
def _process_unread_emails(self) -> None:
    emails = self.email_service.fetch_unread_emails()
    
    for email in emails:
        try:
            self.executor.execute(email)  # ← EXECUTOR PROCESSES EMAIL
            self.db.commit()
```

**Executor**: [Backend/app/automation/executor.py](Backend/app/automation/executor.py#L30-66)
```python
def execute(self, email: dict) -> AutomationState:
    state: AutomationState = {
        "email": email,
        "services": {...},
    }
    return automation_graph.invoke(state)  # ← LANGGRAPH ROUTES
```

**LangGraph**: [Backend/app/automation/graph.py](Backend/app/automation/graph.py)
- Routes email to donation_creation_node or need_creation_node

**Donation Creation**: [Backend/app/automation/nodes/donation_creation.py](Backend/app/automation/nodes/donation_creation.py#L7-47)
```python
def donation_creation_node(state: AutomationState) -> AutomationState:
    automation = state["services"]["automation"]
    
    created = automation.create_donation(
        restaurant=state["restaurant"],
        donation_data=state["donation_data"],
        donation_items=state["donation_items"],
    )
    state["donation"] = created
    return state
```

**AutomationService.create_donation()**: [Backend/app/automation/automation_service.py](Backend/app/automation/automation_service.py#L41-125)
```python
def create_donation(
    self,
    restaurant: Restaurant,
    donation_data: dict,
    donation_items: list[dict],
):
    ...
    donation = self.donation_service.create(donation_schema)
    
    for item in donation_items:
        self.donation_item_service.create(...)
    
    self.matching_service.create_matches(donation)  # ← TRIGGERS HERE (DIFFERENT MATCHING!)
    self.lifecycle_service.notify_next_match(donation)
    
    return donation
```

**Key Difference**: Uses `MatchingService.create_matches()`, not `MatchService.create_nearby_matches()`

### Email-Created Needs

**Flow**: Similar to email donations

**File**: [Backend/app/automation/automation_service.py](Backend/app/automation/automation_service.py#L130-155)
```python
def create_need(self, ngo: NGO, need_data: dict):
    ...
    need = self.need_service.create(need_schema)
    return need  # ← NO MATCHING TRIGGERED
```

**Triggering Point**: `process_new_need()` is called SEPARATELY

**File**: [Backend/app/automation/automation_service.py](Backend/app/automation/automation_service.py#L157-184)
```python
def process_new_need(self, need: Need):
    """
    Re-run matching for all active donations
    after a new NGO need is created.
    """
    donations = (
        self.db.query(Donation)
        .filter(
            Donation.is_deleted == False,
            Donation.status.in_([
                DonationStatus.MATCHING,
                DonationStatus.UNMATCHED,
            ])
        )
        .all()
    )
    
    for donation in donations:
        self.matching_service.create_matches(donation)  # ← RE-RUNS MATCHING
        self.lifecycle_service.notify_next_match(donation)
```

**When Called**: In graph routing (need to check graph.py for exact trigger)

### Summary of Matching Triggers

| Creation Type | Where Triggered | Service Used | Coordinates Used |
|---|---|---|---|
| Website donation | DonationService.create() | MatchService.create_nearby_matches() | ✓ Haversine distance |
| Website need | NeedService.create() | NONE | N/A |
| Email donation | AutomationService.create_donation() | MatchingService.create_matches() | ✗ NO distance (TODO) |
| Email need | AutomationService.process_new_need() | MatchingService.create_matches() | ✗ NO distance (TODO) |

---

## 13. DUPLICATE/DIVERGENT MATCHING IMPLEMENTATIONS

### Implementation #1: Website Matching

**Service**: [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L101-L145)

**Method**: `MatchService.create_nearby_matches(donation)`

**Coordinates Used**: ✓ **YES** — Haversine distance calculation

**Matching Criteria**:
1. Food category match
2. Vegetarian preference match
3. **Distance (if coordinates available)** ← Silently skips if NULL

**Behavior When Coordinates NULL**:
```python
distance_km = self._distance_km(donation, ngo)
if distance_km is None:
    continue  # ← SILENTLY SKIP NGO
```

**Score Calculation**: [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L166-L170)
```python
quantity_score = min(donation.quantity / 100, 1) * 20
distance_score = max(0, 60 - distance_km) / 60 * 80
return round(quantity_score + distance_score, 2)
```

### Implementation #2: Automation Matching

**Service**: [Backend/app/services/matching_service.py](Backend/app/services/matching_service.py#L26-124)

**Method**: `MatchingService.create_matches(donation)`

**Coordinates Used**: ✗ **NO** — Ranking service doesn't use distance

**Ranking Service**: [Backend/app/services/ranking_service.py](Backend/app/services/ranking_service.py)

**Matching Criteria**:
1. **Food category match** (50 points)
2. **Vegetarian preference match** (30 points)
3. **Urgency level** (10-30 points)
4. **TODO: Distance scoring** (not implemented)

**Score Calculation**: [Backend/app/services/ranking_service.py](Backend/app/services/ranking_service.py#L98-L110)
```python
def _score_need(self, donation: Donation, need: Need) -> float:
    score = 0.0
    
    if donation.food_category == need.preferred_category:
        score += CATEGORY_MATCH_SCORE  # 50
    
    if not need.vegetarian_only or donation.is_vegetarian:
        score += VEGETARIAN_MATCH_SCORE  # 30
    
    score += URGENCY_SCORES.get(need.urgency, 0)  # 10/20/30
    
    # TODO:
    # Add distance scoring.
    
    return score
```

### Key Differences

| Aspect | Website (MatchService) | Automation (MatchingService) |
|--------|---|---|
| **Distance Scoring** | ✓ Haversine | ✗ TODO |
| **Urgency Scoring** | ✗ No | ✓ Yes (10-30 points) |
| **Null Handling** | Skip silently | Include all |
| **Query Pattern** | Category + Vegetarian + Distance | All approved NGOs ranked |
| **Match Creation** | Via create_nearby_matches() | Via MatchingService.create_matches() |

### Root Cause of Duplication

**Two separate code paths**:

1. **Website**: Direct service call to MatchService
2. **Automation**: Calls MatchingService which calls RankingService, then MatchService

**Impact**: 
- Website donations get distance-based matching (when coordinates available)
- Email donations get urgency-based matching (no distance)
- Email needs trigger re-matching of ALL active donations with urgency-based scoring
- Inconsistent matching behavior across two input channels

---

## 14. MINIMUM FILES FOR FUTURE MODIFICATION

### For Backend Geocoding Implementation (Option A)

**Core Geocoding Files** (3 files):

1. [Backend/requirements.txt](Backend/requirements.txt)
   - Add geocoding library (e.g., `geopy`)

2. [Backend/app/services/restaurant_service.py](Backend/app/services/restaurant_service.py#L50-L52)
   - Replace TODO with geocoding call in `create()`
   - Add error handling for invalid addresses
   - Update schema to remove lat/long from RestaurantCreate

3. [Backend/app/services/ngo_service.py](Backend/app/services/ngo_service.py#L47-L49)
   - Replace TODO with geocoding call in `create()`
   - Add error handling for invalid addresses

4. [Backend/app/services/donation_service.py](Backend/app/services/donation_service.py#L77-L78)
   - Replace TODO with geocoding call in `create()`
   - Add error handling for invalid addresses

**Schema Changes** (4 files):

5. [Backend/app/schemas/auth.py](Backend/app/schemas/auth.py#L14-L15)
   - Remove `latitude` and `longitude` fields from RegistrationRequest
   - Keep address field mandatory

6. [Backend/app/schemas/restaurant.py](Backend/app/schemas/restaurant.py#L15-L16)
   - Remove `latitude` and `longitude` from RestaurantCreate

7. [Backend/app/schemas/ngo.py](Backend/app/schemas/ngo.py#L16-L17)
   - Remove `latitude` and `longitude` from NGOCreate

8. [Backend/app/schemas/donation.py](Backend/app/schemas/donation.py#L19-L20)
   - Remove `latitude` and `longitude` from DonationCreate

**Frontend Changes** (2 files):

9. [Frontend/src/pages/Register.jsx](Frontend/src/pages/Register.jsx#L166-L169)
   - Remove latitude/longitude input fields
   - Remove "Use current location" button
   - Keep address field only

10. [Frontend/src/pages/Dashboard.jsx](Frontend/src/pages/Dashboard.jsx#L96-L97)
    - Remove latitude/longitude input fields from donation form
    - Remove "Use current pickup location" button
    - Keep pickup_address field only

**Matching/Distance Files** (already correct, no changes needed):

- [Backend/app/services/match_service.py](Backend/app/services/match_service.py) — `_distance_km()` already works correctly with Haversine

### For Coordinate Validation (Option C - Fallback)

**Additional Files** (2 files):

11. [Backend/app/core/exception_handler.py](Backend/app/core/exception_handler.py)
    - Add custom exception for invalid/missing coordinates
    - Improve error messages

12. [Backend/app/models/donation.py](Backend/app/models/donation.py)
    - Consider adding check constraint to prevent 0,0 coordinates (not found in current code, but defensive measure)

### For Duplicate Matching Resolution

**Files to Reconcile** (3 files):

13. [Backend/app/services/match_service.py](Backend/app/services/match_service.py#L101-L145)
    - Consider deprecating `create_nearby_matches()` or making it consistent with MatchingService

14. [Backend/app/services/matching_service.py](Backend/app/services/matching_service.py#L26-L124)
    - Update to use distance scoring when coordinates available
    - Implement fallback urgency-based scoring when coordinates NULL

15. [Backend/app/services/ranking_service.py](Backend/app/services/ranking_service.py#L106-L109)
    - Implement the TODO "Add distance scoring"
    - Accept optional distance parameter

### Summary Table

| Category | Files | Impact | Priority |
|----------|-------|--------|----------|
| Geocoding Implementation | 3 backend services | Core functionality | HIGH |
| Schema Updates | 4 files | API contract | HIGH |
| Frontend Updates | 2 files | User experience | HIGH |
| Duplicate Matching | 3 files | Consistency | MEDIUM |
| Error Handling | 1 file | Robustness | MEDIUM |
| Database Constraints | 1 file | Data integrity | LOW |

**Total Minimum Files**: 10-15 depending on approach

---

## RECOMMENDED NEXT STEP

### Current State
- ✓ Coordinates collected from frontend (geolocation or manual)
- ✓ Coordinates sent to backend via REST API
- ✗ Coordinates NOT persisted (backend ignores them)
- ✗ Email-created records have NO coordinates
- ✗ Matching broken (relies on NULL coordinates)

### Decision Tree

**IF** implementing backend geocoding:
- Start with [requirements.txt](Backend/requirements.txt) — add `geopy`
- Implement in parallel in all three services (restaurant, ngo, donation)
- Update schemas last (will break API temporarily during migration)

**IF** implementing fallback matching:
- Merge RankingService distance scoring with Haversine logic
- Keep all existing schemas unchanged
- Faster to implement but less consistent

**IF** immediate unblock needed:
- Modify [matching_service.py](Backend/app/services/matching_service.py) to accept all NGOs regardless of coordinates
- Add urgency-based secondary ranking
- Temporary solution until geocoding implemented

### Files to Examine First
1. [Backend/requirements.txt](Backend/requirements.txt) — Confirm no geocoding lib
2. [Backend/app/automation/prompts/groq_prompts.py](Backend/app/automation/prompts/groq_prompts.py) — Confirms no lat/long extraction
3. [Backend/app/services/ranking_service.py](Backend/app/services/ranking_service.py) — Has distance TODO
4. [Frontend/src/pages/Register.jsx](Frontend/src/pages/Register.jsx) — Frontend collects data backend ignores

---

## VERIFICATION CHECKLIST

- [x] Frontend collects coordinates via Geolocation API or manual input
- [x] Frontend sends coordinates via REST API to backend
- [x] Backend schemas accept coordinates as optional fields
- [x] Registration/NGO/Restaurant/Donation services receive coordinates
- [x] Services pass coordinates through but don't persist properly
- [x] No backend geocoding implementation exists
- [x] No frontend geocoding implementation exists
- [x] Coordinates become NULL when not provided
- [x] Coordinates never become 0 or 0,0 (no hardcoded defaults)
- [x] MatchService._distance_km() reads from Donation and NGO models
- [x] Two separate matching implementations (Website vs Automation)
- [x] Automation matching doesn't use distance
- [x] 10-15 files would need modification for complete solution
- [x] Recent merge brought matching infrastructure without geocoding

---

**Analysis Complete** — Ready for implementation planning.
