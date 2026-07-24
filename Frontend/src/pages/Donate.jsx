import { useState } from "react";
import { Heart, Clock, MapPin, Utensils } from "lucide-react";

const Donate = () => {

  const [formData,setFormData] = useState({
    foodName:"",
    quantity:"",
    foodType:"",
    address:"",
    pickupTime:"",
    expiryTime:"",
    description:""
  });


  const handleSubmit=(e)=>{
    e.preventDefault();

    console.log(formData);

    alert("Food donation submitted successfully ❤️");

  };


  return (

    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-green-100 py-12 px-4">


      <div className="max-w-5xl mx-auto">


        {/* Header */}

        <div className="text-center mb-10">

          <div className="mx-auto w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center">
            <Heart size={32} fill="white"/>
          </div>


          <h1 className="text-4xl font-bold text-gray-800 mt-5">
            Donate Food
          </h1>

          <p className="text-gray-600 mt-2">
            Share extra food and help someone in need
          </p>

        </div>




        <div className="bg-white rounded-3xl shadow-xl p-8">


          <form 
          onSubmit={handleSubmit}
          className="grid md:grid-cols-2 gap-6"
          >


            <div>
              <label className="label">
                Food Name
              </label>

              <input
              className="input-style"
              placeholder="Example: Rice, Curry"
              value={formData.foodName}
              onChange={(e)=>setFormData({
                ...formData,
                foodName:e.target.value
              })}
              required
              />

            </div>




            <div>

              <label className="label">
                Quantity
              </label>

              <input
              className="input-style"
              placeholder="Example: 20 plates"
              value={formData.quantity}
              onChange={(e)=>setFormData({
                ...formData,
                quantity:e.target.value
              })}
              required
              />

            </div>




            <div>

              <label className="label">
                Food Type
              </label>

              <select
              className="input-style"
              value={formData.foodType}
              onChange={(e)=>setFormData({
                ...formData,
                foodType:e.target.value
              })}
              >

                <option>
                  Select Type
                </option>

                <option>
                  Vegetarian
                </option>

                <option>
                  Non Vegetarian
                </option>

                <option>
                  Snacks
                </option>

                <option>
                  Bakery
                </option>

              </select>

            </div>





            <div>

              <label className="label">
                Pickup Address
              </label>


              <div className="relative">

                <MapPin 
                size={18}
                className="absolute left-3 top-3 text-gray-400"
                />

                <input
                className="input-style pl-10"
                placeholder="Enter pickup location"
                value={formData.address}
                onChange={(e)=>setFormData({
                  ...formData,
                  address:e.target.value
                })}
                />

              </div>

            </div>





            <div>

              <label className="label">
                Pickup Time
              </label>


              <div className="relative">

                <Clock
                size={18}
                className="absolute left-3 top-3 text-gray-400"
                />

                <input
                type="time"
                className="input-style pl-10"
                value={formData.pickupTime}
                onChange={(e)=>setFormData({
                  ...formData,
                  pickupTime:e.target.value
                })}
                />

              </div>


            </div>





            <div>

              <label className="label">
                Expiry Time
              </label>


              <input
              type="datetime-local"
              className="input-style"
              value={formData.expiryTime}
              onChange={(e)=>setFormData({
                ...formData,
                expiryTime:e.target.value
              })}
              />

            </div>






            <div className="md:col-span-2">


              <label className="label">
                Description
              </label>


              <textarea
              rows="4"
              className="input-style"
              placeholder="Add details about food..."
              value={formData.description}
              onChange={(e)=>setFormData({
                ...formData,
                description:e.target.value
              })}
              />


            </div>






            <button
            className="md:col-span-2 bg-green-600 hover:bg-green-700 text-white py-4 rounded-xl font-bold text-lg transition flex justify-center items-center gap-2"
            >

              <Utensils size={22}/>
              Submit Food Donation

            </button>



          </form>


        </div>


      </div>


    </div>

  );

};


export default Donate;