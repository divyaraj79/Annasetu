import { Heart, Target, Users } from "lucide-react";

const About = () => {

  return (

    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100 py-16 px-4">


      <div className="max-w-6xl mx-auto">


        {/* Hero */}

        <div className="text-center mb-14">

          <div className="mx-auto w-16 h-16 rounded-full bg-green-600 text-white flex items-center justify-center">
            <Heart size={32} fill="white"/>
          </div>


          <h1 className="text-4xl font-bold text-gray-800 mt-5">
            About FoodShare
          </h1>


          <p className="text-gray-600 max-w-2xl mx-auto mt-4">
            We connect restaurants, NGOs and communities to reduce food waste
            and make sure surplus food reaches people who need it.
          </p>

        </div>





        {/* Mission Vision Cards */}

        <div className="grid md:grid-cols-3 gap-6">


          <div className="bg-white p-7 rounded-3xl shadow-lg text-center">

            <Target 
            className="mx-auto text-green-600"
            size={40}
            />

            <h2 className="text-xl font-bold mt-4">
              Our Mission
            </h2>

            <p className="text-gray-600 mt-3">
              To reduce hunger by creating a simple food donation network.
            </p>

          </div>




          <div className="bg-white p-7 rounded-3xl shadow-lg text-center">

            <Heart
            className="mx-auto text-green-600"
            size={40}
            fill="currentColor"
            />

            <h2 className="text-xl font-bold mt-4">
              Our Vision
            </h2>

            <p className="text-gray-600 mt-3">
              A world where no food is wasted and everyone gets access to meals.
            </p>

          </div>





          <div className="bg-white p-7 rounded-3xl shadow-lg text-center">

            <Users
            className="mx-auto text-green-600"
            size={40}
            />

            <h2 className="text-xl font-bold mt-4">
              Our Team
            </h2>

            <p className="text-gray-600 mt-3">
              A passionate team building technology for social impact.
            </p>

          </div>



        </div>





        {/* Impact Section */}

        <div className="mt-12 bg-green-600 text-white rounded-3xl p-10 text-center">

          <h2 className="text-3xl font-bold">
            Making An Impact Together 🌱
          </h2>

          <p className="mt-4 text-green-100">
            Every meal donated is a step towards reducing waste and helping communities.
          </p>


        </div>



      </div>


    </div>

  );
};


export default About;