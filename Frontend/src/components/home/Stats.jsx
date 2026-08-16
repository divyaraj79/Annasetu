import { FaUtensils, FaUsers, FaHandsHelping, FaLeaf } from "react-icons/fa";
import { motion } from "framer-motion";

const stats = [
  {
    icon: <FaUtensils />,
    number: "5,200+",
    title: "Meals Donated",
  },
  {
    icon: <FaUsers />,
    number: "340+",
    title: "Partner NGOs",
  },
  {
    icon: <FaHandsHelping />,
    number: "180+",
    title: "Restaurants",
  },
  {
    icon: <FaLeaf />,
    number: "25+",
    title: "Cities Covered",
  },
];

export default function Stats() {
  return (
    <section className="py-20 bg-white">
      <div className="max-w-7xl mx-auto px-6">

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

          {stats.map((item, index) => (
            <motion.div
              key={index}
              whileHover={{ y: -8 }}
              className="bg-light rounded-3xl shadow-md p-8 text-center"
            >
              <div className="w-16 h-16 rounded-full bg-green-100 text-primary flex items-center justify-center text-3xl mx-auto mb-5">
                {item.icon}
              </div>

              <h2 className="text-4xl font-bold text-primary">
                {item.number}
              </h2>

              <p className="mt-3 text-gray-600">
                {item.title}
              </p>
            </motion.div>
          ))}

        </div>

      </div>
    </section>
  );
}