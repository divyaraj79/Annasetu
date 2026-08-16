import { useCallback, useEffect, useMemo, useState } from "react";
import { Navigate, useNavigate, useParams } from "react-router-dom";
import api, { getApiError } from "../services/api";

const categories = ["main_course", "snacks", "dessert", "beverage", "bakery", "other"];
const units = ["kg", "liters", "piece"];
const urgencies = ["low", "medium", "high"];
const matchStatuses = ["interested", "accepted", "rejected", "completed"];

const initialDonation = {
  food_name: "", food_category: "main_course", is_vegetarian: true, quantity: "",
  quantity_unit: "kg", cooked_at: "", expiry_time: "", pickup_address: "", special_notes: "",
  latitude: "", longitude: "",
};
const initialNeed = {
  preferred_category: "main_course", vegetarian_only: false, quantity_required: "",
  quantity_unit: "kg", urgency: "medium",
};

function Select({ value, onChange, options }) {
  return <select className="input-style" value={value} onChange={onChange}>{options.map((option) => <option key={option} value={option}>{option.replaceAll("_", " ")}</option>)}</select>;
}

function Dashboard() {
  const { role } = useParams();
  const navigate = useNavigate();
  const user = useMemo(() => JSON.parse(localStorage.getItem("user") || "null"), []);
  const [organization, setOrganization] = useState(null);
  const [data, setData] = useState({ donations: [], needs: [], matches: [], items: [], restaurants: [], ngos: [], pendingRestaurants: [], pendingNgos: [], users: [] });
  const [donation, setDonation] = useState(initialDonation);
  const [need, setNeed] = useState(initialNeed);
  const [match, setMatch] = useState({ donation_id: "", ngo_id: "" });
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  const loadDashboard = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const requests = [api.get("/donations/"), api.get("/needs/"), api.get("/matches/"), api.get("/restaurants/"), api.get("/ngos/")];
      if (user.role === "restaurant") requests.push(api.get("/donation-items/"));
      if (user.role === "admin") requests.push(api.get("/admin/restaurants/pending"), api.get("/admin/ngos/pending"), api.get("/users/"));
      const responses = await Promise.all(requests);
      const [donations, needs, matches, restaurants, ngos, ...extra] = responses.map((response) => response.data);
      const ownOrganization = user.role === "restaurant"
        ? restaurants.find((entry) => entry.user_id === user.id)
        : user.role === "ngo" ? ngos.find((entry) => entry.user_id === user.id) : null;
      setOrganization(ownOrganization || null);
      setData({
        donations, needs, matches, restaurants, ngos,
        items: user.role === "restaurant" ? extra[0] : [],
        pendingRestaurants: user.role === "admin" ? extra[0] : [],
        pendingNgos: user.role === "admin" ? extra[1] : [],
        users: user.role === "admin" ? extra[2] : [],
      });
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => { loadDashboard(); }, [loadDashboard]);

  if (!user || user.role !== role) return <Navigate to="/login" replace />;

  const ownDonations = user.role === "restaurant" && organization
    ? data.donations.filter((entry) => entry.restaurant_id === organization.id) : data.donations;
  const ownNeeds = user.role === "ngo" && organization
    ? data.needs.filter((entry) => entry.ngo_id === organization.id) : data.needs;
  const relevantMatches = user.role === "restaurant" && organization
    ? data.matches.filter((entry) => ownDonations.some((donationEntry) => donationEntry.id === entry.donation_id))
    : user.role === "ngo" && organization
      ? data.matches.filter((entry) => entry.ngo_id === organization.id) : data.matches;

  const runAction = async (action, successMessage) => {
    setNotice("");
    setError("");
    try {
      await action();
      setNotice(successMessage);
      await loadDashboard();
    } catch (requestError) {
      setError(getApiError(requestError));
    }
  };

  const createDonation = (event) => {
    event.preventDefault();
    if (!organization) return setError("Your restaurant profile is not available yet.");
    const payload = {
      ...donation,
      restaurant_id: organization.id,
      quantity: Number(donation.quantity),
      latitude: Number(donation.latitude),
      longitude: Number(donation.longitude),
      cooked_at: donation.cooked_at ? new Date(donation.cooked_at).toISOString() : null,
      expiry_time: new Date(donation.expiry_time).toISOString(),
    };
    runAction(() => api.post("/donations/", payload), "Donation published successfully.").then(() => setDonation(initialDonation));
  };

  const createNeed = (event) => {
    event.preventDefault();
    if (!organization) return setError("Your NGO profile is not available yet.");
    runAction(() => api.post("/needs/", { ...need, ngo_id: organization.id, quantity_required: Number(need.quantity_required) }), "Food need created successfully.").then(() => setNeed(initialNeed));
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const useDonationLocation = () => {
    if (!navigator.geolocation) {
      setError("Your browser does not support location access.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => setDonation({ ...donation, latitude: coords.latitude, longitude: coords.longitude }),
      () => setError("Location access was denied. Enter pickup coordinates manually.")
    );
  };

  const title = user.role === "restaurant" ? "Restaurant Dashboard" : user.role === "ngo" ? "NGO Dashboard" : "Admin Dashboard";
  return <main className="min-h-screen bg-green-50 p-4 md:p-8">
    <div className="mx-auto max-w-7xl">
      <header className="mb-8 flex flex-wrap items-center justify-between gap-4 rounded-2xl bg-white p-6 shadow-sm">
        <div><p className="text-sm font-semibold text-green-700">AnnaSetu</p><h1 className="text-3xl font-bold text-gray-800">{title}</h1><p className="mt-1 text-gray-600">Signed in as {user.name} ({user.email})</p></div>
        <div className="flex gap-3"><button onClick={loadDashboard} className="rounded-xl border border-green-700 px-4 py-2 text-green-700">Refresh</button><button onClick={logout} className="rounded-xl bg-green-700 px-4 py-2 text-white">Logout</button></div>
      </header>

      {notice && <p className="mb-5 rounded-xl bg-green-100 p-4 text-green-800">{notice}</p>}
      {error && <p className="mb-5 rounded-xl bg-red-50 p-4 text-red-700">{error}</p>}
      {loading ? <p className="text-gray-600">Loading dashboard...</p> : <>
        {user.role !== "admin" && <section className="mb-6 rounded-2xl bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">{user.role === "restaurant" ? "Restaurant" : "NGO"} profile</h2>{organization ? <p className="mt-2 text-gray-600">{organization.restaurant_name || organization.ngo_name} · {organization.address} · Status: <b>{organization.verification_status}</b></p> : <p className="mt-2 text-red-700">Organization profile not found.</p>}</section>}

        {user.role === "restaurant" && <>
          <section className="mb-6 rounded-2xl bg-white p-6 shadow-sm"><h2 className="mb-4 text-xl font-bold">Create food donation</h2><form onSubmit={createDonation} className="grid gap-3 md:grid-cols-2"><input className="input-style" required placeholder="Food name" value={donation.food_name} onChange={(event) => setDonation({ ...donation, food_name: event.target.value })}/><input className="input-style" required type="number" min="1" placeholder="Quantity" value={donation.quantity} onChange={(event) => setDonation({ ...donation, quantity: event.target.value })}/><Select value={donation.food_category} onChange={(event) => setDonation({ ...donation, food_category: event.target.value })} options={categories}/><Select value={donation.quantity_unit} onChange={(event) => setDonation({ ...donation, quantity_unit: event.target.value })} options={units}/><input className="input-style" type="datetime-local" placeholder="Cooked at" value={donation.cooked_at} onChange={(event) => setDonation({ ...donation, cooked_at: event.target.value })}/><input className="input-style" required type="datetime-local" value={donation.expiry_time} onChange={(event) => setDonation({ ...donation, expiry_time: event.target.value })}/><input className="input-style md:col-span-2" required placeholder="Pickup address" value={donation.pickup_address} onChange={(event) => setDonation({ ...donation, pickup_address: event.target.value })}/><input className="input-style" required type="number" step="any" placeholder="Pickup latitude" value={donation.latitude} onChange={(event) => setDonation({ ...donation, latitude: event.target.value })}/><input className="input-style" required type="number" step="any" placeholder="Pickup longitude" value={donation.longitude} onChange={(event) => setDonation({ ...donation, longitude: event.target.value })}/><button type="button" onClick={useDonationLocation} className="rounded-xl border border-green-700 px-4 py-3 font-semibold text-green-700">Use current pickup location</button><input className="input-style" placeholder="Special notes" value={donation.special_notes} onChange={(event) => setDonation({ ...donation, special_notes: event.target.value })}/><label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={donation.is_vegetarian} onChange={(event) => setDonation({ ...donation, is_vegetarian: event.target.checked })}/> Vegetarian food</label><button className="rounded-xl bg-green-700 px-4 py-3 font-semibold text-white">Publish donation</button></form></section>
          <RecordList title="Your donations" records={ownDonations} render={(entry) => <><b>{entry.food_name}</b> · {entry.quantity} {entry.quantity_unit} · {entry.status}<button onClick={() => runAction(() => api.delete(`/donations/${entry.id}`), "Donation deleted.")} className="ml-3 text-sm text-red-700">Delete</button></>}/>
          <RecordList title="Donation items" records={data.items.filter((item) => ownDonations.some((entry) => entry.id === item.donation_id))} render={(entry) => <><b>{entry.food_name}</b> · {entry.quantity} {entry.quantity_unit}</>}/>
          <MatchList matches={relevantMatches} onUpdate={(entry, status) => runAction(() => api.put(`/matches/${entry.id}`, { status, responded_at: new Date().toISOString() }), "Match updated.")}/>
        </>}

        {user.role === "ngo" && <>
          <section className="mb-6 rounded-2xl bg-white p-6 shadow-sm"><h2 className="mb-4 text-xl font-bold">Create food need</h2><form onSubmit={createNeed} className="grid gap-3 md:grid-cols-2"><input className="input-style" required type="number" min="1" placeholder="Quantity required" value={need.quantity_required} onChange={(event) => setNeed({ ...need, quantity_required: event.target.value })}/><Select value={need.preferred_category} onChange={(event) => setNeed({ ...need, preferred_category: event.target.value })} options={categories}/><Select value={need.quantity_unit} onChange={(event) => setNeed({ ...need, quantity_unit: event.target.value })} options={units}/><Select value={need.urgency} onChange={(event) => setNeed({ ...need, urgency: event.target.value })} options={urgencies}/><label className="flex items-center gap-2 text-sm"><input type="checkbox" checked={need.vegetarian_only} onChange={(event) => setNeed({ ...need, vegetarian_only: event.target.checked })}/> Vegetarian only</label><button className="rounded-xl bg-green-700 px-4 py-3 font-semibold text-white">Publish need</button></form></section>
          <RecordList title="Your food needs" records={ownNeeds} render={(entry) => <><b>{entry.preferred_category.replaceAll("_", " ")}</b> · {entry.quantity_required} {entry.quantity_unit} · {entry.urgency}<button onClick={() => runAction(() => api.delete(`/needs/${entry.id}`), "Need deleted.")} className="ml-3 text-sm text-red-700">Delete</button></>}/>
          <RecordList title="Available donations" records={data.donations} render={(entry) => <><b>{entry.food_name}</b> · {entry.quantity} {entry.quantity_unit} · {entry.pickup_address}</>}/>
          <MatchList matches={relevantMatches} onUpdate={(entry, status) => runAction(() => api.put(`/matches/${entry.id}`, { status, responded_at: new Date().toISOString() }), "Match updated.")}/>
        </>}

        {user.role === "admin" && <>
          <section className="mb-6 rounded-2xl bg-white p-6 shadow-sm"><h2 className="mb-4 text-xl font-bold">Create a donation match</h2><form onSubmit={(event) => { event.preventDefault(); runAction(() => api.post("/matches/", match), "Match created."); }} className="grid gap-3 md:grid-cols-3"><select required className="input-style" value={match.donation_id} onChange={(event) => setMatch({ ...match, donation_id: event.target.value })}><option value="">Select donation</option>{data.donations.map((entry) => <option key={entry.id} value={entry.id}>{entry.food_name} ({entry.quantity} {entry.quantity_unit})</option>)}</select><select required className="input-style" value={match.ngo_id} onChange={(event) => setMatch({ ...match, ngo_id: event.target.value })}><option value="">Select NGO</option>{data.ngos.map((entry) => <option key={entry.id} value={entry.id}>{entry.ngo_name}</option>)}</select><button className="rounded-xl bg-green-700 px-4 py-3 font-semibold text-white">Create match</button></form></section>
          <ApprovalList title="Pending restaurants" records={data.pendingRestaurants} nameKey="restaurant_name" onApprove={(entry) => runAction(() => api.post(`/admin/restaurants/${entry.id}/approve`), "Restaurant approved.")} onReject={(entry) => runAction(() => api.post(`/admin/restaurants/${entry.id}/reject`), "Restaurant rejected.")}/>
          <ApprovalList title="Pending NGOs" records={data.pendingNgos} nameKey="ngo_name" onApprove={(entry) => runAction(() => api.post(`/admin/ngos/${entry.id}/approve`), "NGO approved.")} onReject={(entry) => runAction(() => api.post(`/admin/ngos/${entry.id}/reject`), "NGO rejected.")}/>
          <RecordList title="Registered users" records={data.users} render={(entry) => <><b>{entry.name}</b> · {entry.email} · {entry.role}</>}/>
          <RecordList title="All donations" records={data.donations} render={(entry) => <><b>{entry.food_name}</b> · {entry.status}</>}/>
          <RecordList title="All needs" records={data.needs} render={(entry) => <><b>{entry.preferred_category}</b> · {entry.urgency}</>}/>
          <MatchList matches={relevantMatches} onUpdate={(entry, status) => runAction(() => api.put(`/matches/${entry.id}`, { status, responded_at: new Date().toISOString() }), "Match updated.")}/>
        </>}
      </>}
    </div>
  </main>;
}

function RecordList({ title, records, render }) {
  return <section className="mb-6 rounded-2xl bg-white p-6 shadow-sm"><h2 className="mb-4 text-xl font-bold">{title}</h2>{records.length ? <div className="space-y-3">{records.map((entry) => <div key={entry.id} className="rounded-xl border border-gray-100 p-4 text-gray-700">{render(entry)}</div>)}</div> : <p className="text-gray-500">No records yet.</p>}</section>;
}

function MatchList({ matches, onUpdate }) {
  return <RecordList title="Nearby NGO alerts and matches" records={matches} render={(entry) => <div className="flex flex-wrap items-center justify-between gap-3"><span><b>Food match</b> · {entry.status} · {entry.distance_km} km · score {entry.score ?? "-"}<br /><span className="text-sm text-gray-500">{entry.match_reason}</span></span><Select value={entry.status} onChange={(event) => onUpdate(entry, event.target.value)} options={matchStatuses}/></div>}/>;
}

function ApprovalList({ title, records, nameKey, onApprove, onReject }) {
  return <RecordList title={title} records={records} render={(entry) => <div className="flex flex-wrap items-center justify-between gap-3"><span><b>{entry[nameKey]}</b> · {entry.address}</span><span className="flex gap-2"><button onClick={() => onApprove(entry)} className="rounded-lg bg-green-700 px-3 py-2 text-sm text-white">Approve</button><button onClick={() => onReject(entry)} className="rounded-lg bg-red-700 px-3 py-2 text-sm text-white">Reject</button></span></div>}/>;
}

export default Dashboard;
