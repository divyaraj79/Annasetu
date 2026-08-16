import { FaShieldAlt, FaClock, FaUsers, FaLeaf } from "react-icons/fa";

const features = [
  {
    icon: <FaLeaf />,
    title: "Reduce Food Waste",
    desc: "Turn surplus meals into hope by ensuring edible food reaches those who need it.",
  },
  {
    icon: <FaClock />,
    title: "Quick Matching",
    desc: "Nearby NGOs receive real-time donation notifications for faster pickup.",
  },
  {
    icon: <FaShieldAlt />,
    title: "Safe & Transparent",
    desc: "Every donation is tracked to ensure accountability and trust.",
  },
  {
    icon: <FaUsers />,
    title: "Community Impact",
    desc: "Restaurants, NGOs and volunteers work together to create lasting change.",
  },
];

export default function Features() {
  return (
    <section className="py-24 bg-white">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-14">

          <p className="text-primary font-semibold uppercase tracking-widest">
            Why Choose Us
          </p>

          <h2 className="text-4xl font-bold mt-3">
            Why AnnaSetu?
          </h2>

          <p className="text-gray-600 mt-5 max-w-2xl mx-auto">
            We bridge the gap between surplus food and people in need using
            technology, compassion and collaboration.
          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">

          {features.map((item, index) => (

            <div
              key={index}
              className="rounded-3xl bg-light p-8 shadow hover:-translate-y-2 hover:shadow-xl transition"
            >

              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center text-3xl text-primary mb-6">
                {item.icon}
              </div>

              <h3 className="font-bold text-xl mb-4">
                {item.title}
              </h3>

              <p className="text-gray-600 leading-7">
                {item.desc}
              </p>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}