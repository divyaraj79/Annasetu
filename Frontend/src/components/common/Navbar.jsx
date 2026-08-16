import { Link, NavLink } from "react-router-dom";
import { FaHandsHelping } from "react-icons/fa";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 bg-white/90 backdrop-blur shadow-sm">
      <nav className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link
          to="/"
          className="flex items-center gap-2 text-2xl font-bold text-green-700"
        >
          <FaHandsHelping />
          AnnaSetu
        </Link>

        <div className="hidden md:flex gap-8 font-medium">
          <NavLink to="/">Home</NavLink>
          <NavLink to="/about">About</NavLink>
          <NavLink to="/donate">Donate</NavLink>
          <NavLink to="/contact">Contact</NavLink>
        </div>

        <div className="flex gap-3">
          <Link
            to="/login"
            className="border border-green-700 px-4 py-2 rounded-full hover:bg-green-700 hover:text-white transition"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="bg-green-700 text-white px-4 py-2 rounded-full hover:bg-green-800 transition"
          >
            Register
          </Link>
        </div>
      </nav>
    </header>
  );
}