import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Heart } from "lucide-react";

const Login = () => {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    // backend later connect
    console.log(formData);
    navigate("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-green-100 px-4">

      <div className="w-full max-w-md bg-white rounded-3xl shadow-xl p-8">

        <div className="text-center mb-8">

          <div className="mx-auto w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center">
            <Heart size={32} fill="white" />
          </div>

          <h1 className="text-3xl font-bold mt-4 text-gray-800">
            Welcome Back
          </h1>

          <p className="text-gray-500 mt-2">
            Login to continue saving food
          </p>

        </div>


        <form onSubmit={handleSubmit} className="space-y-5">

          <div>
            <label className="block text-sm font-medium mb-2">
              Email Address
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              className="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:ring-green-500 outline-none"
              value={formData.email}
              onChange={(e)=>setFormData({
                ...formData,
                email:e.target.value
              })}
              required
            />
          </div>


          <div>

            <label className="block text-sm font-medium mb-2">
              Password
            </label>

            <div className="relative">

              <input
                type={showPassword ? "text":"password"}
                placeholder="Enter password"
                className="w-full px-4 py-3 rounded-xl border focus:ring-2 focus:ring-green-500 outline-none"
                value={formData.password}
                onChange={(e)=>setFormData({
                  ...formData,
                  password:e.target.value
                })}
                required
              />

              <button
                type="button"
                onClick={()=>setShowPassword(!showPassword)}
                className="absolute right-4 top-3 text-gray-500"
              >
                {
                  showPassword 
                  ? <EyeOff size={22}/>
                  : <Eye size={22}/>
                }
              </button>

            </div>

          </div>


          <button
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition"
          >
            Login
          </button>


        </form>


        <p className="text-center mt-6 text-gray-600">
          Don't have an account?{" "}
          <Link
            to="/register"
            className="text-green-600 font-semibold"
          >
            Register
          </Link>
        </p>


      </div>

    </div>
  );
};

export default Login;