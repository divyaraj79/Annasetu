import { FaFacebook, FaInstagram, FaLinkedin } from "react-icons/fa";

export default function Footer() {
  return (
    <footer className="bg-dark text-white">

      <div className="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-4 gap-10">

        <div>

          <h2 className="text-3xl font-bold text-green-400">
            AnnaSetu
          </h2>

          <p className="text-gray-300 mt-5 leading-7">
            Connecting restaurants, NGOs and communities
            to eliminate food waste.
          </p>

        </div>

        <div>

          <h3 className="font-bold mb-5">
            Quick Links
          </h3>

          <ul className="space-y-3 text-gray-300">

            <li>Home</li>
            <li>About</li>
            <li>Donate</li>
            <li>Contact</li>

          </ul>

        </div>

        <div>

          <h3 className="font-bold mb-5">
            Contact
          </h3>

          <p className="text-gray-300">
            Ahmedabad, Gujarat
          </p>

          <p className="text-gray-300 mt-3">
            support@annasetu.com
          </p>

        </div>

        <div>

          <h3 className="font-bold mb-5">
            Follow Us
          </h3>

          <div className="flex gap-5 text-2xl">

            <FaFacebook />

            <FaInstagram />

            <FaLinkedin />

          </div>

        </div>

      </div>

      <div className="border-t border-gray-700 py-6 text-center text-gray-400">

        © 2026 AnnaSetu. All Rights Reserved.

      </div>

    </footer>
  );
}