import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Heart, UserRound, Building2 } from "lucide-react";

const Register = () => {

  const navigate = useNavigate();

  const [role, setRole] = useState("Restaurant");

  const [formData,setFormData] = useState({
    name:"",
    email:"",
    phone:"",
    password:"",
    address:""
  });


  const handleSubmit=(e)=>{
    e.preventDefault();

    console.log({
      ...formData,
      role
    });

    // backend later connect
    navigate("/login");
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
          onClick={()=>setRole("Restaurant")}
          className={`p-4 rounded-2xl border flex flex-col items-center gap-2 transition
          ${
            role==="Restaurant"
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
          onClick={()=>setRole("NGO")}
          className={`p-4 rounded-2xl border flex flex-col items-center gap-2 transition
          ${
            role==="NGO"
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
          placeholder="Password"
          className="input-style"
          value={formData.password}
          onChange={(e)=>setFormData({
            ...formData,
            password:e.target.value
          })}
          required
          />



          <button
          className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition"
          >
            Register as {role}
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