import { Link } from "react-router-dom";
import { Home, Heart } from "lucide-react";

const NotFound = () => {

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-50 via-white to-green-100 px-4">


      <div className="text-center">


        <div className="mx-auto w-20 h-20 bg-green-600 rounded-full flex items-center justify-center text-white">

          <Heart size={40} fill="white"/>

        </div>



        <h1 className="text-8xl font-bold text-green-600 mt-6">
          404
        </h1>


        <h2 className="text-3xl font-bold text-gray-800 mt-4">
          Page Not Found
        </h2>


        <p className="text-gray-600 mt-3 max-w-md">
          Sorry, the page you are looking for does not exist.
        </p>




        <Link
        to="/"
        className="inline-flex items-center gap-2 mt-8 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl font-semibold transition"
        >

          <Home size={20}/>
          Back To Home

        </Link>



      </div>


    </div>

  );

};


export default NotFound;