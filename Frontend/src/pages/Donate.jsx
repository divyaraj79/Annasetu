import { Link, Navigate } from "react-router-dom";
import { Heart, Utensils } from "lucide-react";

export default function Donate() {
  const user = JSON.parse(localStorage.getItem("user") || "null");

  if (user?.role === "restaurant") {
    return <Navigate to="/dashboard/restaurant" replace />;
  }

  return <main className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100 px-4 py-16">
    <section className="mx-auto max-w-xl rounded-3xl bg-white p-8 text-center shadow-xl">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-600 text-white"><Heart size={32} fill="white" /></div>
      <h1 className="mt-5 text-3xl font-bold text-gray-800">Donate Food</h1>
      <p className="mt-3 text-gray-600">Food donations can be created only from a verified restaurant account. This keeps pickup details and NGO matching secure.</p>
      <div className="mt-7 flex flex-col justify-center gap-3 sm:flex-row">
        {!user && <Link to="/login" className="rounded-xl bg-green-700 px-5 py-3 font-semibold text-white">Login as Restaurant</Link>}
        {!user && <Link to="/register" className="rounded-xl border border-green-700 px-5 py-3 font-semibold text-green-700">Register Restaurant</Link>}
        {user?.role === "ngo" && <Link to="/dashboard/ngo" className="rounded-xl bg-green-700 px-5 py-3 font-semibold text-white">Go to NGO Dashboard</Link>}
        {user?.role === "admin" && <Link to="/dashboard/admin" className="rounded-xl bg-green-700 px-5 py-3 font-semibold text-white">Go to Admin Dashboard</Link>}
      </div>
      <p className="mt-6 flex items-center justify-center gap-2 text-sm text-gray-500"><Utensils size={18} /> Restaurant donations are automatically matched to nearby NGOs.</p>
    </section>
  </main>;
}
