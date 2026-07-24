import { FaArrowRight, FaLeaf, FaHandsHelping } from "react-icons/fa";
import { motion } from "framer-motion";

export default function Hero() {
  return (
    <section className="bg-light min-h-[90vh] flex items-center">
      <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-12 items-center">

        {/* Left */}

        <motion.div
          initial={{ opacity: 0, x: -70 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: .8 }}
        >

          <span className="bg-green-100 text-primary px-4 py-2 rounded-full font-semibold inline-block mb-5">
            🌿 Together We Can End Food Waste
          </span>

          <h1 className="text-5xl lg:text-6xl font-extrabold leading-tight text-dark">
            Every Meal
            <span className="text-primary"> Matters.</span>
            <br />
            Every Donation
            <span className="text-accent"> Counts.</span>
          </h1>

          <p className="text-gray-600 mt-6 text-lg leading-8">
            AnnaSetu connects restaurants, NGOs and volunteers
            to rescue surplus food and deliver it safely to people
            who need it the most.
          </p>

          <div className="flex gap-5 mt-10">

            <button className="bg-primary hover:bg-secondary text-white px-7 py-4 rounded-full flex items-center gap-3 transition">
              Donate Food
              <FaArrowRight />
            </button>

            <button className="border-2 border-primary text-primary px-7 py-4 rounded-full hover:bg-primary hover:text-white transition">
              Learn More
            </button>

          </div>

        </motion.div>

        {/* Right */}

        <motion.div
          initial={{ opacity:0,x:70 }}
          animate={{ opacity:1,x:0 }}
          transition={{ duration:.8 }}
          className="relative"
        >

          <div className="bg-gradient-to-br from-green-200 to-green-500 rounded-[40px] p-10 shadow-2xl">

            <img
              src="https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?w=900"
              alt="Food Donation"
              className="rounded-3xl w-full h-[450px] object-cover"
            />

          </div>

          <div className="absolute -left-10 top-8 bg-white shadow-xl rounded-2xl px-5 py-4 flex items-center gap-3">

            <FaHandsHelping className="text-primary text-2xl"/>

            <div>
              <h3 className="font-bold">5200+</h3>
              <p className="text-gray-500 text-sm">
                Meals Saved
              </p>
            </div>

          </div>

          <div className="absolute -right-6 bottom-10 bg-white shadow-xl rounded-2xl px-5 py-4 flex items-center gap-3">

            <FaLeaf className="text-green-600 text-2xl"/>

            <div>
              <h3 className="font-bold">340+</h3>
              <p className="text-gray-500 text-sm">
                NGOs Connected
              </p>
            </div>

          </div>

        </motion.div>

      </div>
    </section>
  );
}