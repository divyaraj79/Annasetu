import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Heart, UserRound, Building2 } from "lucide-react";
import api, { getApiError } from "../services/api";

const Register = () => {

  const navigate = useNavigate();

  const [role, setRole] = useState("restaurant");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [confirmPassword, setConfirmPassword] = useState("");

  const [formData,setFormData] = useState({
    name:"",
    email:"",
    phone:"",
    password:"",
    organization_name:"",
    address:"",
    latitude:"",
    longitude:""
  });

  const useCurrentLocation = () => {
    if (!navigator.geolocation) {
      setError("Your browser does not support location access.");
      return;
    }
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => setFormData({ ...formData, latitude: coords.latitude, longitude: coords.longitude }),
      () => setError("Location access was denied. Enter latitude and longitude manually.")
    );
  };


  const handleSubmit=async (e)=>{
    e.preventDefault();
    setError("");
    setSuccess("");
    if (formData.password !== confirmPassword) {
      setError("Password and confirm password must match.");
      return;
    }
    setIsSubmitting(true);

    try {
      await api.post("/auth/register", { ...formData, role, latitude: Number(formData.latitude), longitude: Number(formData.longitude) });
      setSuccess("Registration completed. You can now log in; donations and needs require admin approval.");
      setTimeout(() => navigate("/login"), 1500);
    } catch (requestError) {
      setError(getApiError(requestError));
    } finally {
      setIsSubmitting(false);
    }
  };


  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-green-100 px-4 py-10">


      <div className="w-full max-w-lg bg-white rounded-3xl shadow-xl p-8">


        <div className="text-center mb-7">


          <div className="mx-auto w-16 h-16 rounded-full bg-green-600 text-white flex items-center justify-center">

            <Heart size={32} fill="white"/>

          </div>


          <h1 className="text-3xl font-bold text-gray-800 mt-4">
            Create Account
          </h1>

          <p className="text-gray-500 mt-2">
            Join us and help reduce food waste
          </p>


        </div>



        {/* Role Selection */}

        <div className="grid grid-cols-2 gap-4 mb-6">


          <button
          type="button"
          onClick={()=>setRole("restaurant")}
          className={`p-4 rounded-2xl border flex flex-col items-center gap-2 transition
          ${
            role==="restaurant"
            ?"border-green-600 bg-green-50 text-green-700"
            :"border-gray-200"
          }`}
          >

            <Building2/>
            <span className="font-semibold">
              Restaurant
            </span>

          </button>



          <button
          type="button"
          onClick={()=>setRole("ngo")}
          className={`p-4 rounded-2xl border flex flex-col items-center gap-2 transition
          ${
            role==="ngo"
            ?"border-green-600 bg-green-50 text-green-700"
            :"border-gray-200"
          }`}
          >

            <UserRound/>
            <span className="font-semibold">
              NGO
            </span>

          </button>


        </div>




        <form onSubmit={handleSubmit} className="space-y-4">


          <input
          type="text"
          placeholder="Full Name"
          className="input-style"
          value={formData.name}
          onChange={(e)=>setFormData({
            ...formData,
            name:e.target.value
          })}
          required
          />

          <input
          type="text"
          placeholder={role === "restaurant" ? "Restaurant Name" : "NGO Name"}
          className="input-style"
          value={formData.organization_name}
          onChange={(e)=>setFormData({ ...formData, organization_name:e.target.value })}
          required
          />

          <div className="grid grid-cols-2 gap-3">
            <input type="number" step="any" placeholder="Latitude" className="input-style" value={formData.latitude} onChange={(event)=>setFormData({ ...formData, latitude:event.target.value })} required />
            <input type="number" step="any" placeholder="Longitude" className="input-style" value={formData.longitude} onChange={(event)=>setFormData({ ...formData, longitude:event.target.value })} required />
          </div>

          <button type="button" onClick={useCurrentLocation} className="w-full rounded-xl border border-green-700 py-2 font-semibold text-green-700">Use my current location</button>



          <input
          type="email"
          placeholder="Email Address"
          className="input-style"
          value={formData.email}
          onChange={(e)=>setFormData({
            ...formData,
            email:e.target.value
          })}
          required
          />



          <input
          type="tel"
          placeholder="Phone Number"
          className="input-style"
          value={formData.phone}
          onChange={(e)=>setFormData({
            ...formData,
            phone:e.target.value
          })}
          required
          />



          <input
          type="text"
          placeholder="Address"
          className="input-style"
          value={formData.address}
          onChange={(e)=>setFormData({
            ...formData,
            address:e.target.value
          })}
          required
          />



          <input
          type="password"
          placeholder="Password (8-20 characters)"
          className="input-style"
          value={formData.password}
          onChange={(e)=>setFormData({
            ...formData,
            password:e.target.value
          })}
          required
          />

          <input
          type="password"
          placeholder="Confirm password"
          className="input-style"
          value={confirmPassword}
          onChange={(event)=>setConfirmPassword(event.target.value)}
          required
          />



          {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          {success && <p className="rounded-lg bg-green-50 p-3 text-sm text-green-700">{success}</p>}

          <button
          disabled={isSubmitting}
          className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition"
          >
            {isSubmitting ? "Submitting..." : `Register as ${role === "restaurant" ? "Restaurant" : "NGO"}`}
          </button>



        </form>




        <p className="text-center mt-6 text-gray-600">

          Already have account?{" "}

          <Link
          to="/login"
          className="text-green-600 font-semibold"
          >
            Login
          </Link>

        </p>



      </div>



    </div>

  );
};


export default Register;
