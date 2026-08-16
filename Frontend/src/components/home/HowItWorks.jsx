import { FaStore, FaBoxOpen, FaHandsHelping, FaHeart } from "react-icons/fa";

const steps = [
  {
    icon: <FaStore />,
    title: "Restaurant",
    desc: "Restaurants upload surplus food details.",
  },
  {
    icon: <FaBoxOpen />,
    title: "Donation",
    desc: "Food is verified and listed instantly.",
  },
  {
    icon: <FaHandsHelping />,
    title: "NGO Accepts",
    desc: "Nearby NGOs claim the available donation.",
  },
  {
    icon: <FaHeart />,
    title: "People Served",
    desc: "Fresh meals reach people safely and quickly.",
  },
];

export default function HowItWorks() {
  return (
    <section className="py-24 bg-light">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center">

          <h2 className="text-4xl font-bold text-dark">
            How AnnaSetu Works
          </h2>

          <p className="text-gray-600 mt-4">
            A simple process to reduce food waste and feed communities.
          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 mt-16">

          {steps.map((step, i) => (

            <div
              key={i}
              className="bg-white rounded-3xl p-8 shadow-md hover:shadow-xl transition"
            >

              <div className="text-4xl text-primary mb-6">
                {step.icon}
              </div>

              <h3 className="text-xl font-bold mb-3">
                {step.title}
              </h3>

              <p className="text-gray-600">
                {step.desc}
              </p>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}