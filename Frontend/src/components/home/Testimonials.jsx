const testimonials = [
  {
    name: "Priya Shah",
    role: "NGO Volunteer",
    text: "AnnaSetu has made food donation simple and reliable. We've been able to serve hundreds of families.",
  },
  {
    name: "Rohit Mehta",
    role: "Restaurant Owner",
    text: "Instead of wasting food every night, we now donate it to nearby NGOs within minutes.",
  },
  {
    name: "Ayesha Khan",
    role: "Volunteer",
    text: "The platform connects everyone beautifully. It's easy to use and creates real impact.",
  },
];

export default function Testimonials() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center mb-14">
          <h2 className="text-4xl font-bold">
            What People Say
          </h2>

          <p className="text-gray-600 mt-4">
            Real stories from our community.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">

          {testimonials.map((item, index) => (

            <div
              key={index}
              className="bg-light rounded-3xl p-8 shadow hover:shadow-xl transition"
            >

              <div className="text-5xl text-primary mb-5">
                ❝
              </div>

              <p className="text-gray-600 leading-8">
                {item.text}
              </p>

              <h3 className="font-bold mt-8 text-xl">
                {item.name}
              </h3>

              <p className="text-primary">
                {item.role}
              </p>

            </div>

          ))}

        </div>

      </div>
    </section>
  );
}