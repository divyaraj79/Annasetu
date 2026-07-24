import { FaMapMarkerAlt } from "react-icons/fa";

const campaigns = [
  {
    image:
      "https://images.unsplash.com/photo-1593113598332-cd288d649433?auto=format&fit=crop&w=900&q=80",
    title: "Community Meal Drive",
    place: "Mandsaur",
  },
  {
    image:
      "https://images.unsplash.com/photo-1556911220-bff31c812dba?auto=format&fit=crop&w=900&q=80",
    title: "Restaurant Food Rescue",
    place: "Mandsaur",
  },
  {
    image:
      "https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?auto=format&fit=crop&w=900&q=80",
    title: "Weekend Donation Camp",
    place: "Mandsaur",
  },
];

export default function Campaigns() {
  return (
    <section className="py-24 bg-light">

      <div className="max-w-7xl mx-auto px-6">

        <div className="flex justify-between items-center mb-12">

          <div>

            <p className="text-primary font-semibold uppercase">
              Featured
            </p>

            <h2 className="text-4xl font-bold mt-3">
              Ongoing Campaigns
            </h2>

          </div>

          <button className="bg-primary text-white px-6 py-3 rounded-full">
            View All
          </button>

        </div>

        <div className="grid md:grid-cols-3 gap-8">

          {campaigns.map((item, index) => (

            <div
              key={index}
              className="bg-white rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition"
            >

              <img
                src={item.image}
                alt={item.title}
                className="h-60 w-full object-cover"
              />

              <div className="p-7">

                <h3 className="font-bold text-2xl">
                  {item.title}
                </h3>

                <div className="flex items-center gap-2 text-gray-500 mt-4">

                  <FaMapMarkerAlt />

                  {item.place}

                </div>

                <button className="mt-8 bg-primary text-white px-5 py-3 rounded-full w-full hover:bg-secondary transition">
                  Support Campaign
                </button>

              </div>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}
