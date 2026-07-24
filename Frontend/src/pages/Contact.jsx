import { Mail, Phone, MapPin } from "lucide-react";

const Contact = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100 py-16 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800">
            Contact Us
          </h1>

          <p className="text-gray-600 mt-3">
            Have questions? We would love to hear from you.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Form */}
          <div className="bg-white p-8 rounded-3xl shadow-xl">
            <form className="space-y-5">
              <input
                className="input-style"
                placeholder="Your Name"
              />

              <input
                className="input-style"
                placeholder="Email Address"
              />

              <textarea
                className="input-style"
                rows="5"
                placeholder="Your Message"
              />

              <button
                className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* Details */}
          <div className="space-y-5">
            <div className="bg-white p-6 rounded-3xl shadow-lg flex gap-4">
              <MapPin className="text-green-600" />

              <div>
                <h3 className="font-bold">
                  Address
                </h3>

                <p className="text-gray-600">
                  FoodShare Community Center, India
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-3xl shadow-lg flex gap-4">
              <Mail className="text-green-600" />

              <div>
                <h3 className="font-bold">
                  Email
                </h3>

                <p className="text-gray-600">
                  support@foodshare.com
                </p>
              </div>
            </div>

            <div className="bg-white p-6 rounded-3xl shadow-lg flex gap-4">
              <Phone className="text-green-600" />

              <div>
                <h3 className="font-bold">
                  Phone
                </h3>

                <p className="text-gray-600">
                  +91 98765 43210
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Contact;
